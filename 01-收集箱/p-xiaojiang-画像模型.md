# P小将 画像模型框架

## 目标
建立 P小将 的买入喜好模型，预测他们会买什么

## 数据来源

### 1. GMGN 数据
- 地址
- 追踪的 CA
- 历史交易记录
- 持仓变化

### 2. Twitter 数据
- 发推内容
- 讨论的代币
- 互动话题

### 3. 链上数据
- 买入/卖出时间
- 买入金额
- 持仓周期
- 止盈/止损

## 画像模型结构

```yaml
p_xiaojiang:
  # 基础信息
  username: "@bboybtc"
  twitter: "@bboybtc"
  chain: "BSC"
  gmgn_address: "0xbf004bff64725914ee36d03b87d6965b0ced4903"

  # 画像标签
  preferences:
    # 市值偏好
    market_cap:
      - "5位"      # $10k-$99k
      - "6位"      # $100k-$999k
    
    # 叙事偏好
    narrative:
      - "meme"
      - "degen"
    
    # 买入时机
    timing:
      - "新币上线即买"
      - "等Twitter讨论"
    
    # 持仓周期
    holding_period:
      - "短线"  # < 24h
      - "中线"  # 1-7天
    
    # 止盈习惯
    take_profit:
      - "2x"
      - "5x"

  # 行为模式
  behavior:
    decision_source: "GMGN + Twitter"
    risk_level: "高"
    max_position_size: "$500"

  # 历史数据
  history:
    tracked_tokens: []
    total_trades: 0
    win_rate: 0
```

## 更新流程

```
1. 获取新数据
   - GMGN 追踪的 CA
   - Twitter 讨论
   - 链上交易

2. 提取特征
   - 市值
   - 叙事
   - 时机

3. 更新画像
   - 打新标签
   - 调整权重

4. 预测验证
   - 新币来了 → 预测
   - 实际买了 → 更新模型
```

## 预测模型

### 输入
- 新币特征（市值、叙事、热度、Twitter讨论）

### 输出
- 预测：会买 / 不会买
- 置信度：0-100%

### 算法
- 规则匹配（基于画像标签）
- 相似度计算
- 机器学习（可选）

## 使用示例

### 啊锋 (Ah Feng)

```yaml
username: "@bboybtc"
preferences:
  market_cap: ["5位", "6位"]  # 从追踪的14个CA推断
  narrative: ["meme", "degen"]
  timing: ["等Twitter讨论", "看GMGN"]
  holding_period: ["短线"]
  take_profit: ["2x", "3x"]

behavior:
  decision_source: "GMGN + Twitter分析"
  risk_level: "高"
```

### 预测例子

新币 A:
- 市值: 6位
- 叙事: meme
- Twitter: @heyibinance 在推

→ 匹配啊锋画像 → 预测: 会买

---
- 创建时间：2026-02-26
