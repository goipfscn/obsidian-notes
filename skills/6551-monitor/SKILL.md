# 6551 方案 - X + 新闻源监控

## 目标
24h 自动监控 X List + 全网新闻 + 推送到 Discord/Telegram

## 架构

```
Cron (每3小时)
    ↓
获取 List 成员最新推文
    ↓
获取相关新闻源
    ↓
AI 分析筛选
    ↓
推送到 Discord/Telegram
```

## 配置

### List 配置
- 核心关注: 1976167332289577300

### 新闻源
- X/Twitter (via bird)
- 全网搜索 (via agent-reach)

### 监控频率
- 每 3 小时扫描
- 热门关键词实时推送

## 功能

### 1. List 监控
- 读取 List 成员推文
- 过滤关键词（币种、事件）
- 按 2. 新闻互动排序

###扫描
- 关键词：BTC、ETH、Solana、Polymarket、meme
- 新兴趋势检测

### 3. 信号分类
- 🚨 紧急 - 需要立即关注
- 📈 趋势 - 新兴热门
- 💡 观点 - KOL 分享
- 📰 新闻 - 重要事件

### 4. 推送格式

```
🚨 [紧急] [时间] 
标题

📈 [趋势] [时间]
标题

💡 [观点] @username
摘要

📰 [新闻] [时间]
标题
```

## 实现

### Cron 配置
```bash
# 每3小时执行
30 */3 * * * cd /root/.openclaw/workspace && python3 monitor.py
```

### 推送渠道
- Discord (已有)
- Telegram (需配置)

---
- 创建时间：2026-02-26
- 参考：6551 方案
