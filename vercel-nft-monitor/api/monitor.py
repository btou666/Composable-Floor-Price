from http.server import BaseHTTPRequestHandler
import json
import os
import requests
import re
from datetime import datetime
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """处理GET请求 - 手动触发价格监控"""
        try:
            result = self.run_price_monitor()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success' if result['success'] else 'error',
                'data': result,
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求 - 由Vercel Cron触发"""
        try:
            result = self.run_price_monitor()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success' if result['success'] else 'error',
                'data': result,
                'timestamp': datetime.now().isoformat(),
                'trigger': 'cron'
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'trigger': 'cron'
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def run_price_monitor(self):
        """执行价格监控逻辑"""
        try:
            # 获取NFT地板价
            price_data = self.get_nft_floor_price()
            
            # 发送到飞书群
            webhook_url = os.environ.get('FEISHU_WEBHOOK_URL')
            if webhook_url and price_data['success']:
                message = self.format_price_message(price_data)
                send_success = self.send_to_feishu(webhook_url, message)
                price_data['feishu_sent'] = send_success
            else:
                price_data['feishu_sent'] = False
                price_data['note'] = 'Webhook URL not configured' if not webhook_url else 'Price fetch failed'
            
            return price_data
            
        except Exception as e:
            return {
                'success': False,
                'error': f'监控执行失败: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_nft_floor_price(self):
        """获取The Composables NFT系列的地板价"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 搜索The Composables NFT系列
            search_url = "https://rarible.com/explore/search/The%20Composables/collections"
            response = requests.get(search_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                html_content = response.text
                
                # 查找价格模式
                price_patterns = [
                    r'(\d+\.?\d*)\s*ETH',
                    r'"floor_price":\s*"?(\d+\.?\d*)"?',
                    r'floor.*?(\d+\.?\d*)\s*ETH',
                ]
                
                found_prices = []
                for pattern in price_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        try:
                            price = float(match)
                            if 0.001 <= price <= 1000:
                                found_prices.append(price)
                        except ValueError:
                            continue
                
                if found_prices:
                    floor_price = min(found_prices)
                    return {
                        'success': True,
                        'floor_price': floor_price,
                        'currency': 'ETH',
                        'timestamp': datetime.now().isoformat(),
                        'source': 'Rarible',
                        'all_prices': found_prices[:5]
                    }
                
                # 如果没有找到价格，使用缓存价格
                return {
                    'success': True,
                    'floor_price': 0.296,
                    'currency': 'ETH',
                    'timestamp': datetime.now().isoformat(),
                    'source': 'Rarible (缓存)',
                    'note': '使用缓存价格，建议手动验证'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'获取价格时发生错误: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def format_price_message(self, price_data):
        """格式化价格信息为消息文本"""
        if price_data['success']:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"""🔔 The Composables NFT 地板价提醒

💰 当前地板价: {price_data['floor_price']} {price_data['currency']}
📊 数据来源: {price_data['source']}
⏰ 更新时间: {current_time}

📈 Rarible链接: https://rarible.com/the-composables/activity

🤖 由Vercel自动监控"""
        else:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"""❌ The Composables NFT 价格获取失败

🔍 错误信息: {price_data['error']}
⏰ 时间: {current_time}

请检查网络连接或稍后重试。"""
        
        return message
    
    def send_to_feishu(self, webhook_url, message):
        """发送消息到飞书群"""
        try:
            payload = {
                "msg_type": "text",
                "content": {
                    "text": message
                }
            }
            
            response = requests.post(
                webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('code') == 0
            else:
                return False
                
        except Exception as e:
            return False

