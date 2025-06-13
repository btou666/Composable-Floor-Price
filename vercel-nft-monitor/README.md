# NFT价格监控系统 - Vercel部署版

这是一个部署在Vercel上的NFT价格监控系统，可以自动获取The Composables NFT系列的地板价并发送到飞书群。

## 功能特性

- 🔄 自动获取NFT地板价
- 📱 发送到飞书群聊
- ⏰ 每天定时提醒（上午9点和下午6点，UTC时间）
- 🚀 部署在Vercel Serverless平台
- 🔧 支持手动触发和定时触发

## 项目结构

```
vercel-nft-monitor/
├── api/
│   └── monitor.py          # Serverless Function
├── requirements.txt        # Python依赖
├── vercel.json            # Vercel配置和Cron Jobs
└── README.md              # 说明文档
```

## 部署步骤

### 1. 准备代码

将项目代码上传到GitHub、GitLab或Bitbucket仓库。

### 2. 连接Vercel

1. 访问 [Vercel](https://vercel.com)
2. 使用GitHub/GitLab/Bitbucket账号登录
3. 点击"New Project"
4. 选择您的代码仓库
5. 点击"Deploy"

### 3. 配置环境变量

在Vercel项目设置中添加环境变量：

1. 进入项目Dashboard
2. 点击"Settings"
3. 点击"Environment Variables"
4. 添加以下变量：
   - `FEISHU_WEBHOOK_URL`: 您的飞书机器人Webhook地址

### 4. 获取飞书Webhook地址

1. 在飞书群中添加自定义机器人
2. 设置机器人名称（如：NFT价格监控）
3. 复制生成的Webhook地址
4. 将地址添加到Vercel环境变量中

## 使用方法

### 自动执行

系统会自动在每天上午9点和下午6点（UTC时间）执行价格监控。

### 手动触发

访问您的Vercel部署URL + `/api/monitor` 来手动触发价格监控。

例如：`https://your-project.vercel.app/api/monitor`

### 查看日志

在Vercel Dashboard的"Functions"标签页中可以查看执行日志。

## Cron表达式说明

当前配置的Cron表达式：
- `0 9 * * *` - 每天上午9点（UTC）
- `0 18 * * *` - 每天下午6点（UTC）

如需修改时间，请编辑 `vercel.json` 文件中的 `schedule` 字段。

## 时区说明

Vercel Cron Jobs使用UTC时间。如果您需要其他时区，请相应调整Cron表达式：

- 北京时间（UTC+8）上午9点 = UTC时间凌晨1点 = `0 1 * * *`
- 北京时间（UTC+8）下午6点 = UTC时间上午10点 = `0 10 * * *`

## API响应格式

成功响应：
```json
{
  "status": "success",
  "data": {
    "success": true,
    "floor_price": 0.296,
    "currency": "ETH",
    "source": "Rarible",
    "feishu_sent": true
  },
  "timestamp": "2025-06-13T03:45:00.000Z"
}
```

错误响应：
```json
{
  "status": "error",
  "error": "错误信息",
  "timestamp": "2025-06-13T03:45:00.000Z"
}
```

## 故障排除

### 1. Cron Jobs不执行
- 确认项目已部署到生产环境
- 检查Vercel Dashboard中的Cron Jobs设置
- 查看Functions日志

### 2. 飞书消息发送失败
- 确认环境变量 `FEISHU_WEBHOOK_URL` 已正确设置
- 检查Webhook地址是否有效
- 确认机器人未被移除

### 3. 价格获取失败
- 检查网络连接
- 确认Rarible网站可正常访问
- 查看详细错误日志

## 限制说明

- Vercel免费计划有执行时间和调用次数限制
- Cron Jobs在免费计划中每天最多执行2次
- 函数执行超时时间为10秒（免费计划）

## 升级和维护

要更新系统：
1. 修改代码并推送到Git仓库
2. Vercel会自动重新部署
3. 新的Cron Jobs配置会自动生效

## 技术支持

如遇问题，请检查：
1. Vercel部署状态
2. 环境变量配置
3. 飞书机器人设置
4. 函数执行日志

