# Polymarket 交易员分析工作流

> 完整工作流：筛选 → 分析 → 记录

---

## 工作流概述

```
1. CLI筛选交易员 (PnL $15K-$400K)
       ↓
2. Scrapling + Cookie 获取详细数据
       ↓
3. 1号博主标准验证
       ↓
4. 图表分析 + 记录

(备用) duola回测验证
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

## 步骤3: 1号博主筛选标准

### Scrapling验证 (详细数据)
| 指标 | 要求 |
|------|------|
| PnL | $15K - $400K |
| 胜率 | 70% - 95% |
| 交易次数 | 20 - 1000 |

### 排除Bot
- ❌ 胜率 > 95% (确定是Bot)
- ⚠️ 胜率90-95% 需要人工判断
- ❌ 交易 > 1000次

---

## 步骤4: 生成深度分析报告

### 获取交易历史
```bash
polymarket data activity 0x交易员地址 --limit 30
```

### 分析内容
- 核心数据 (PnL, Win Rate)
- 专精领域分布
- 最近30笔交易记录
- 交易特点分析
- 适合跟单评分

### 输出格式
保存到: `obsidian/01-收集箱/交易员名-深度分析.md`

### 安装
```bash
pip install scrapling --break-system-packages
```

### 使用Cookie抓取
```bash
scrapling extract fetch "https://hashdive.com/tradera/0x交易员地址" /tmp/output.html --extra-headers "Cookie: auth_session=你的auth_session;pm_sticky=polygun" --wait 3000
```

### 获取Cookie
1. 打开 https://polymarketanalytics.com 并登录
2. 使用Cookie-Editor插件导出cookie
3. 或者用F12 → Console: `console.log(document.cookie)`

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
- **PnL: $174,851** (Scrapling数据)
- **Win Rate: 92.9%** (Scrapling数据)
- Volume: $135,758
- 专精: 央行利率、伊朗、黄金
- 状态: ✅ 符合1号博主标准

---

## 数据保存位置

- 交易员数据: `obsidian/01-收集箱/pm-trader-data/`
- 筛选结果: `obsidian/01-收集箱/pm-1haobo-qualified.json`
- 分析报告: `obsidian/01-收集箱/`

---

## 备用: duola回测验证

当Scrapling无法获取数据时使用：

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

### 回测
```bash
duola backtest 别名 --lookback 30d --fixed-usd 10
```

---

## 更新日志

- 2026-03-04: 创建完整工作流skill
