# NFT价格监控系统

自动获取The Composables NFT系列的地板价并发送到飞书群的监控系统。

## 功能特性

- 🔄 自动获取NFT地板价
- 📱 发送到飞书群聊
- ⏰ 每天定时提醒（上午9点和下午6点）
- 📊 价格历史记录
- 🛡️ 错误处理和重试机制

## 快速开始

### 1. 在飞书群中添加自定义机器人

1. 打开飞书群聊
2. 点击群设置 → 群机器人 → 添加机器人 → 自定义机器人
3. 设置机器人名称（如：NFT价格监控）
4. 复制生成的Webhook地址

### 2. 配置系统

编辑 `config.json` 文件，将 `YOUR_FEISHU_WEBHOOK_URL_HERE` 替换为你的Webhook地址：

```json
{
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxx",
  "nft_collection": "The Composables",
  "notification_times": [
    "09:00",
    "18:00"
  ],
  "timezone": "Asia/Shanghai"
}
```

### 3. 设置定时任务

运行设置脚本：

```bash
./setup_cron.sh
```

这将自动创建每天上午9点和下午6点的定时任务。

### 4. 手动测试

测试价格获取功能：

```bash
python3 nft_price_monitor.py
```

测试发送到飞书群：

```bash
python3 nft_price_monitor.py "你的Webhook地址"
```

## 文件说明

- `nft_price_monitor.py` - 主要的价格监控脚本
- `config.json` - 配置文件
- `setup_cron.sh` - 定时任务设置脚本
- `monitor.log` - 运行日志文件（自动生成）

## 管理定时任务

查看当前定时任务：
```bash
crontab -l
```

删除所有定时任务：
```bash
crontab -r
```

查看运行日志：
```bash
tail -f monitor.log
```

## 消息格式

系统会发送如下格式的消息到飞书群：

```
🔔 The Composables NFT 地板价提醒

💰 当前地板价: 0.296 ETH
📊 数据来源: Rarible
⏰ 更新时间: 2025-06-12 09:00:00

📈 Rarible链接: https://rarible.com/the-composables/activity
```

## 故障排除

### 价格获取失败
- 检查网络连接
- 确认Rarible网站可正常访问
- 查看 `monitor.log` 日志文件

### 飞书消息发送失败
- 确认Webhook地址正确
- 检查机器人是否被移除
- 确认群聊权限设置

### 定时任务不执行
- 确认cron服务运行中：`sudo service cron status`
- 检查cron任务：`crontab -l`
- 查看系统日志：`sudo tail -f /var/log/syslog | grep CRON`

## 自定义配置

### 修改提醒时间

编辑 `config.json` 中的 `notification_times` 数组：

```json
"notification_times": [
  "08:30",
  "12:00", 
  "20:00"
]
```

然后重新运行 `./setup_cron.sh`

### 添加安全设置

在飞书机器人设置中，可以添加：
- 自定义关键词
- IP白名单
- 签名校验

## 技术支持

如遇问题，请检查：
1. Python环境（需要Python 3.6+）
2. 必要的Python包：requests, beautifulsoup4
3. 网络连接和防火墙设置
4. 飞书机器人权限和配置

## 更新日志

- v1.0.0 - 初始版本，支持基本的价格监控和飞书通知功能

