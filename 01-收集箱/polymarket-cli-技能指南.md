# Polymarket CLI 技能指南

## 简介
Rust 编写的命令行工具，可以从终端操作 Polymarket：
- 浏览市场
- 下单/撤单
- 管理仓位
- JSON 输出供脚本/Agent 使用

## 安装

### 方法1: Homebrew (macOS/Linux)
```bash
brew tap Polymarket/polymarket-cli https://github.com/Polymarket/polymarket-cli
brew install polymarket
```

### 方法2: Shell 脚本
```bash
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
```

### 方法3: 源码编译
```bash
git clone https://github.com/Polymarket/polymarket-cli
cd polymarket-cli
cargo install --path .
```

## 快速开始

### 无需钱包（浏览）
```bash
polymarket markets list --limit 5
polymarket markets search "election"
polymarket events list --tag politics

# 查看具体市场
polymarket markets get will-trump-win-the-2024-election

# JSON 输出（脚本用）
polymarket -o json markets list --limit 3
```

### 需要钱包（交易）
```bash
polymarket setup
# 或
polymarket wallet create
polymarket approve set
```

## 核心命令

### 市场浏览
```bash
# 列出市场
polymarket markets list --limit 10
polymarket markets list --active true --order volume_num

# 搜索市场
polymarket markets search "bitcoin" --limit 5

# 获取单个市场
polymarket markets get 12345

# 查看订单簿
polymarket clob book TOKEN_ID

# 历史价格
polymarket clob price-history TOKEN_ID --interval 1d
```

### 交易操作
```bash
# 下单
polymarket clob market-order --token TOKEN_ID --side buy --amount 5
polymarket clob create-order --token TOKEN_ID --side buy --price 0.45 --size 20

# 撤单
polymarket clob cancel ORDER_ID
polymarket clob cancel-all

# 查仓位
polymarket clob balance --asset-type collateral
polymarket data positions 0xYOUR_ADDRESS
```

### 其他
```bash
# 查看钱包
polymarket wallet show

# 查看订单
polymarket clob orders
polymarket clob trades

# 交互式 Shell
polymarket shell
```

## 输出格式

```bash
# 表格输出（默认）
polymarket markets list --limit 2

# JSON 输出（脚本用）
polymarket -o json markets list --limit 2
```

## 配置

配置文件: `~/.config/polymarket/config.json`
```json
{
  "private_key": "0x...",
  "chain_id": "137",
  "signature_type": "proxy"
}
```

## 自动化交易

### 结合 OpenClaw
1. OpenClaw 读取 Twitter 发现信号
2. 调用 Polymarket CLI 查询市场
3. 判断后自动下单
4. 自动止损/止盈

### 示例流程
```bash
# 1. 读取信号
# (通过 OpenClaw/Twitter)

# 2. 查市场
polymarket -o json markets search "bitcoin"

# 3. 下单
polymarket clob market-order --token TOKEN_ID --side buy --amount 10

# 4. 监控仓位
polymarket data positions 0xYOUR_ADDRESS
```

## 警告
⚠️ 早期软件，请勿使用大额资金。务必在下单前验证交易。

---
- 来源：https://github.com/Polymarket/polymarket-cli
- 整理：小孩
