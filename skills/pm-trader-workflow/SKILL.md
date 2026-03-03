# Polymarket 交易员分析工作流

> 完整工作流：筛选 → 分析 → 记录

---

## 工作流概述

```
1. CLI筛选交易员 (PnL $15K-$400K)
       ↓
2. duola同步 + 回测
       ↓
3. 1号博主标准筛选
       ↓
4. 图表分析 + 记录
```

---

## 步骤1: CLI筛选交易员

### 安装CLI
```bash
npm install -g polymarket
```

### 筛选PnL $15K-$400K
```bash
polymarket data leaderboard --period all --order-by pnl --limit 50 --offset 500
polymarket data leaderboard --period month --order-by pnl --limit 50
```

### 查看交易历史
```bash
polymarket data activity 0x交易员地址 --limit 50
```

---

## 步骤2: duola分析

### 安装
```bash
npm install -g duola
```

### 添加交易员
```bash
duola leader add 0x交易员地址 --name 别名
```

### 同步数据
```bash
duola sync 别名 --limit 200
```

### 回测验证
```bash
duola backtest 别名 --lookback 30d --fixed-usd 10
```

---

## 步骤3: 1号博主筛选标准

### CLI筛选 (初级)
| 指标 | 范围 |
|------|------|
| PnL | $15K - $400K |
| 胜率 | 70% - 90% |
| 交易次数 | 20 - 1000 |

### duola验证 (二次)
| 指标 | 要求 |
|------|------|
| 执行信号 | ≥ 10 |
| 胜率 | ≥ 70% |
| PnL | > 0 |

### 排除Bot
- ❌ 胜率 > 90%
- ❌ 交易 > 1000次

---

## 步骤4: 图表分析

### 专精领域分布
```
Fed利率决策  ████████████████ 34%
伊朗/地缘   ████████████    30%
泰国选举    █████████      21%
```

### 收益走势图
```
$55K ┤                              █ $51,956
      │
$40K ┤                    █████████
      │                    █ $40,446
$25K ┤          █████████
      │          █ $23,781
$10K ┤████████
      │$11,110
$0   ┼────────────────────────────
      2/15  2/20  2/25  3/02
```

---

## 工具对比

| 工具 | 用途 | 优点 |
|------|------|------|
| polymarket CLI | 筛选交易员 | 稳定，不被封 |
| duola | 回测分析 | 详细数据 |
| Scrapling | 绕过反爬虫 | 可抓网站数据 |
| Polymarket Analytics | 手动查看 | 直观 |

---

## 已验证交易员

### Ronaldo2100 ✅
- 地址: `0x71ca04d689bc38c5e4dcda8a4d743f279c5A3501`
- 胜率: 100%
- 30天PnL: $58.29
- 专精: 央行利率、伊朗、黄金
- 24天内交易: 469笔

---

## 数据保存位置

- 交易员数据: `obsidian/01-收集箱/pm-trader-data/`
- 筛选结果: `obsidian/01-收集箱/pm-1haobo-qualified.json`
- 分析报告: `obsidian/01-收集箱/`

---

## 更新日志

- 2026-03-04: 创建完整工作流skill
