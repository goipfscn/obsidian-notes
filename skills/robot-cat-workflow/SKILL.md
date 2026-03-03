# 机器人猫 - Polymarket 跟单工作流

> 基于 1号博主 + 哆啦(duola) 工具的完整跟单工作流

## 工作流程概述

```
1. 筛选交易员 → 2. 数据分析 → 3. 回测验证 → 4. 启动跟单
```

---

## 步骤 1: 筛选符合1号博主标准的交易员

### 标准
| 指标 | 范围 |
|------|------|
| PnL | $15K - $400K |
| 胜率 | 70% - 90% |
| 交易次数 | 20 - 1000 |
| 活跃仓位 | ≥2 |

### CLI筛选命令
```bash
# 获取排行榜数据 (PnL $15K-$400K)
polymarket data leaderboard --period all --order-by pnl --limit 50 --offset 500
polymarket data leaderboard --period all --order-by pnl --limit 50 --offset 1000
```

---

## 步骤 2: 用 duola 同步分析

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

### 查看分析
```bash
duola leader inspect 别名
```

---

## 步骤 3: 回测验证

```bash
duola backtest 别名 --lookback 30d --fixed-usd 10
```

### 评估指标
- 执行信号数 > 50
- 胜率 ≥ 70%
- PnL > 0
- 专精单一领域

---

## 步骤 4: 启动跟单

### 配置钱包
```bash
printf '%s' '0x你的私钥' | duola autopilot onboard 0x交易员地址 --name 别名 --private-key-stdin
```

### 选择预设方案
```bash
duola follow init 别名 --profile conservative  # 保守: $10/笔
duola follow init 别名 --profile balanced     # 平衡: $25/笔
duola follow init 别名 --profile aggressive  # 激进: $50/笔
```

### 启动
```bash
duola autopilot start 别名 --confirm-live "I UNDERSTAND LIVE TRADING"
```

---

## 自动化脚本

### 批量分析交易员
```python
import subprocess
import json

traders = [
    {"name": "Ronaldo2100", "addr": "0x71Ca04d689bc38c5E4dCDA8A4D743f279c5A3501"},
    # 添加更多...
]

for t in traders:
    # 添加
    subprocess.run(["duola", "leader", "add", t['addr'], "--name", t['name']])
    # 同步
    subprocess.run(["duola", "sync", t['name'], "--limit", "200"])
    # 回测
    result = subprocess.run(["duola", "backtest", t['name'], "--lookback", "30d", "--fixed-usd", "10"], 
                           capture_output=True)
    data = json.loads(result.stdout)
    print(f"{t['name']}: {data['summary']}")
```

---

## 当前验证过的交易员

| 交易员 | 胜率 | PnL (30天) | 专精 | 状态 |
|--------|------|-------------|------|------|
| Ronaldo2100 | 100% | $56.2 | 央行利率 | ✅ 推荐 |

---

## 私钥安全

- 私钥存放在 `~/.duola/secrets/`
- 文件权限 0600
- 只在本地签名，不发往网络

---

## 更新日志

- 2026-03-03: 创建工作流
