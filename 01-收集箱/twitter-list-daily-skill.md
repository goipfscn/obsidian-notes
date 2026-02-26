# Twitter List 日报 Skill

## 用途
每天定时读取指定 List 的推文，生成精选总结，推送到 Discord/Telegram

## 配置

### 需要监控的 List
请提供你想监控的 List，我们来配置

### List ID 获取方法
1. 打开 List 页面：https://x.com/i/lists/xxxxx
2. URL 最后的数字就是 List ID

## 触发方式
- Cron：每天早上 9:00 / 晚上 21:00
- 手动触发：说"生成日报"

## 执行流程

### 1. 获取 List 成员推文
```bash
# 获取 List 成员
bird list-members [LIST_ID]

# 获取成员最新推文
bird user-tweets [USERNAME] --limit 10
```

### 2. 筛选标准
- 近 24 小时推文
- 过滤转发（保留原创）
- 按互动排序（点赞+回复+转发）

### 3. 总结格式

```
📊 [List名称] 日报 - YYYY-MM-DD

🔥 热点话题
[从推文中提取的热点]

📈 关键信号
- @username: [推文摘要]
- @username: [推文摘要]

💡 有价值的观点
[精选推文]

---
来源：List名称 | 共X条推文 | 筛选Y条
```

### 4. 推送渠道
- Discord：webhook
- Telegram：bot sendMessage
- GitHub：commit 到仓库

## 示例

```
📊 Polymarket Traders 日报 - 2026-02-26

🔥 热点话题
- $PUMP 热度飙升
- Polymarket 新上热门市场

📈 关键信号
- @DextersSolab: 分享了 copy trading 教程
- @whalewatchalert: $PUNCH 鲸鱼买入提醒

💡 有价值的观点
...

---
来源：Polymarket Traders | 共156条推文 | 筛选8条
```

## 使用方法

### 1. 配置 List
告诉小孩你想监控的 List，他会帮你获取 List ID

### 2. 手动触发
```
每天早上好 → 触发日报生成
```

### 3. 自动触发
配置 cron job 定时执行

---
- 创建时间：2026-02-26
