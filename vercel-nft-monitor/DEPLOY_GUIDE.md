# Vercel部署指南

## 快速部署步骤

### 1. 下载项目文件
下载 `vercel-nft-monitor.zip` 并解压到本地。

### 2. 上传到Git仓库
1. 在GitHub/GitLab/Bitbucket创建新仓库
2. 将解压后的文件上传到仓库

### 3. 连接Vercel
1. 访问 https://vercel.com
2. 使用Git账号登录
3. 点击"New Project"
4. 选择您的仓库
5. 点击"Deploy"

### 4. 配置环境变量
1. 进入Vercel项目Dashboard
2. 点击"Settings" → "Environment Variables"
3. 添加变量：
   - Name: `FEISHU_WEBHOOK_URL`
   - Value: 您的飞书机器人Webhook地址

### 5. 获取飞书Webhook
1. 在飞书群中添加自定义机器人
2. 复制Webhook地址
3. 粘贴到Vercel环境变量中

### 6. 测试部署
访问 `https://your-project.vercel.app/api/monitor` 测试功能。

## 时区调整

默认配置为UTC时间：
- 上午9点 UTC = 北京时间下午5点
- 下午6点 UTC = 北京时间凌晨2点

如需调整为北京时间，修改 `vercel.json`：
```json
{
  "crons": [
    {
      "path": "/api/monitor",
      "schedule": "0 1 * * *"
    },
    {
      "path": "/api/monitor", 
      "schedule": "0 10 * * *"
    }
  ]
}
```

这样设置后：
- 北京时间上午9点执行
- 北京时间下午6点执行

