#!/bin/bash
# NFT价格监控定时任务设置脚本

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/nft_price_monitor.py"
CONFIG_FILE="$SCRIPT_DIR/config.json"

echo "设置NFT价格监控定时任务..."

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件 $CONFIG_FILE 不存在"
    exit 1
fi

# 检查Python脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "错误: Python脚本 $PYTHON_SCRIPT 不存在"
    exit 1
fi

# 从配置文件中读取Webhook URL
WEBHOOK_URL=$(python3 -c "import json; config=json.load(open('$CONFIG_FILE')); print(config['webhook_url'])")

if [ "$WEBHOOK_URL" = "YOUR_FEISHU_WEBHOOK_URL_HERE" ]; then
    echo "警告: 请先在 $CONFIG_FILE 中配置正确的飞书Webhook地址"
    echo "当前将以测试模式运行（不发送到飞书群）"
    WEBHOOK_URL=""
fi

# 创建cron任务
# 每天上午9点和下午6点执行
CRON_JOB_1="0 9 * * * cd $SCRIPT_DIR && python3 $PYTHON_SCRIPT $WEBHOOK_URL >> $SCRIPT_DIR/monitor.log 2>&1"
CRON_JOB_2="0 18 * * * cd $SCRIPT_DIR && python3 $PYTHON_SCRIPT $WEBHOOK_URL >> $SCRIPT_DIR/monitor.log 2>&1"

# 添加到crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB_1"; echo "$CRON_JOB_2") | crontab -

echo "定时任务已设置完成！"
echo "任务详情:"
echo "- 每天上午9:00执行价格监控"
echo "- 每天下午18:00执行价格监控"
echo "- 日志文件: $SCRIPT_DIR/monitor.log"
echo ""
echo "查看当前cron任务: crontab -l"
echo "删除cron任务: crontab -r"
echo ""
echo "手动测试: python3 $PYTHON_SCRIPT $WEBHOOK_URL"

