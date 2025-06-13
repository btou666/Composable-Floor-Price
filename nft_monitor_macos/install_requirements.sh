#!/bin/bash
# 安装NFT价格监控系统的依赖

echo "安装NFT价格监控系统依赖..."

# 更新系统包
echo "更新系统包..."
sudo apt update

# 安装Python3和pip（如果没有安装）
echo "检查Python3和pip..."
sudo apt install -y python3 python3-pip

# 安装cron服务
echo "安装cron服务..."
sudo apt install -y cron

# 启动cron服务
echo "启动cron服务..."
sudo service cron start

# 安装Python依赖包
echo "安装Python依赖包..."
pip3 install requests beautifulsoup4

echo "依赖安装完成！"
echo ""
echo "接下来的步骤："
echo "1. 编辑 config.json 配置飞书Webhook地址"
echo "2. 运行 ./setup_cron.sh 设置定时任务"
echo "3. 使用 python3 nft_price_monitor.py 测试功能"

