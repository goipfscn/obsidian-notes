# Ed哥策略 - 大金狗筛选模型

## 概述
识别 Solana/BSC 链上具有百倍潜力的 Meme 币

## 核心三要素

### 1. 简单动物题材
- 形象简单易懂
- 可爱、有记忆点
- 例子：Jellybean、Dogwifhat、Penguin

### 2. 主流媒体曝光
- 主流财经媒体报道
- 媒体：鉅亨網、BlockBeats、Decrypt、Coindesk 等
- 搜索关键词："[币名] + meme coin + 新闻/报道"

### 3. 一眼看懂，出圈
- 名字简单好记
- 不需要解释就能懂
- 病毒式传播潜力

## 筛选流程

```
1. 发现新币
   ↓
2. 检查是否符合动物题材
   ↓
3. 搜索主流媒体是否报道
   ↓
4. 判断是否"一眼看懂"
   ↓
5. 三要素都满足 = 大金狗
```

## 判断标准

| 要素 | 是 | 否 |
|------|----|----|
| 动物/简单形象 | ✅ | ❌ |
| 主流媒体报道 | ✅ | ❌ |
| 名字好记 | ✅ | ❌ |

## $Jellybean 案例

| 要素 | 符合 | 说明 |
|------|------|------|
| 简单动物题材 | ✅ | Jellybean 果冻熊，形象简单可爱 |
| 主流媒体曝光 | ✅ | 鉅亨網、BlockBeats 报道 |
| 一眼看懂，出圈 | ✅ | 名字简单，24h 涨 5500% |

## 数据来源

### 链上数据
- Dexscreener
- GMGN
- Pump.fun

### 媒体监测
- Google 搜索
- 中文财经媒体（鉅亨網、BlockBeats）
- 英文媒体（Coindesk、Decrypt）

### Twitter 热度
- agent-reach 搜索
- Twitter 提及量

## 使用方法

### Step 1: 发现新币
用 GMGN 或 Dexscreener 监控新上币种

### Step 2: 三要素检查
1. 动物/简单形象？
2. 主流媒体报道？
3. 名字好记？

### Step 3: 判断
- 3 ✅ = 大金狗，重仓
- 2 ✅ = 观察
- 1 ✅ = 忽略

## 监控命令

```bash
# 查代币数据
curl "https://api.dexscreener.com/latest/dex/tokens/[CA]"

# 查 Twitter 热度
agent-reach search-twitter "[币名]"

# 查媒体报道
agent-reach search "[币名] meme coin 新闻"
```

---
- 创建时间：2026-02-27
- 作者：Ed哥
- 来源：实战总结
