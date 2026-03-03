# 机器人猫工作流 - 交易员筛选与分析

> 只做分析记录，不启动自动跟单

## 工作流程

```
1. CLI筛选交易员 (PnL $15K-$400K)
       ↓
2. duola同步数据 + 回测
       ↓
3. 筛选符合1号博主标准
       ↓
4. 保存记录
```

---

## 步骤1: CLI筛选交易员

```bash
# 获取PnL $15K-$400K区间的交易员
polymarket data leaderboard --period all --order-by pnl --limit 50 --offset 500
polymarket data leaderboard --period all --order-by pnl --limit 50 --offset 1000
```

---

## 步骤2: duola同步分析

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
duola backtest 别名 --lookback 90d --fixed-usd 10
```

---

## 步骤3: 1号博主筛选标准

| 指标 | 范围 |
|------|------|
| 执行信号数 | ≥ 10 |
| 胜率 | ≥ 70% |
| PnL | > 0 |
| 专精 | 单一领域 |

---

## 步骤4: 保存记录

保存到: `obsidian/01-收集箱/pm-1haobo-qualified.json`

```json
{
  "qualified": [...],
  "tested": [...]
}
```

---

## ⚠️ 注意事项

- ❌ 不启动自动跟单
- ✅ 只分析筛选并记录结果
- ✅ 保存到Obsidian并上传GitHub

---

## 更新日志
- 2026-03-03: 创建
