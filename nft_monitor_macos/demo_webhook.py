#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示如何使用NFT价格监控系统
"""

from nft_price_monitor import NFTPriceMonitor

def demo_with_webhook():
    """
    演示如何使用真实的Webhook地址
    """
    print("=== NFT价格监控系统演示 ===\n")
    
    # 这里需要替换为真实的飞书Webhook地址
    webhook_url = "YOUR_FEISHU_WEBHOOK_URL_HERE"
    
    print("请按照以下步骤设置：")
    print("1. 在飞书群中添加自定义机器人")
    print("2. 复制Webhook地址")
    print("3. 将地址替换到config.json或直接传入脚本")
    print()
    
    if webhook_url == "YOUR_FEISHU_WEBHOOK_URL_HERE":
        print("⚠️  当前使用演示模式（未配置Webhook地址）")
        webhook_url = None
    else:
        print(f"✅ 使用Webhook地址: {webhook_url[:50]}...")
    
    # 创建监控器实例
    monitor = NFTPriceMonitor(webhook_url)
    
    # 执行价格监控
    print("\n--- 开始价格监控 ---")
    result = monitor.run_monitor()
    
    print("\n--- 监控结果 ---")
    if result['success']:
        print(f"✅ 成功获取价格: {result['floor_price']} {result['currency']}")
        print(f"📊 数据来源: {result['source']}")
        if webhook_url:
            print("📱 消息已发送到飞书群")
        else:
            print("📱 演示模式：消息未发送到飞书群")
    else:
        print(f"❌ 获取价格失败: {result['error']}")
    
    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    demo_with_webhook()

