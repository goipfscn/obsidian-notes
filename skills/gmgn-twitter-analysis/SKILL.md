# GMGN Twitter 分析获取 Skill

## 用途
通过 GMGN 获取某个 Token 的 Twitter 讨论分析

## 使用方法

### 1. 获取 Token 页面
GMGN URL 格式：
- BSC: `https://gmgn.ai/bsc/token/{address}`
- Solana: `https://gmgn.ai/sol/token/{address}`
- 其他链类似

### 2. 页面结构
页面包含：
- **推特监控** tab - 显示 Twitter 讨论
- **活动** tab - 显示链上交易
- **仓位** tab - 显示持仓
- **持有者** tab - 显示持币地址
- **开发者代币** tab - 显示开发者关联代币

### 3. 关键信息提取

#### Twitter 讨论数据
- 推文内容
- 发布者（@username）
- 发布时间
- 推文链接
- 热度（互动量）

#### Token 基本数据
- 代币名称
- 符号
- CA 地址
- 价格
- 市值
- 流动性
- 24h 成交额
- 持有者数量

#### 开发者信息
- 开发者地址
- 历史创建的代币
- 资金来源

### 4. 自动化获取方法

#### 方法 A：浏览器自动化
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"https://gmgn.ai/bsc/token/{ca_address}")
    page.wait_for_selector(".twitter-monitor")
    # 提取 Twitter 讨论
```

#### 方法 B：API（如有）
待研究

### 5. 在 P小将 系统中的应用

```
GMGN 新 CA 出现
    ↓
获取 Twitter 讨论
    ↓
分析：谁在推这个币
    ↓
匹配 P小将 画像
    ↓
预测买入
```

### 6. 示例数据

**Token:** 凝视深渊，也会被深渊凝视
**CA:** 0xcadc836d41f3f6e69bfc9ef201d77865f2c14444

| 指标 | 值 |
|------|-----|
| 价格 | $0.0000388 |
| 市值 | $3.88K |
| 流动性 | $5.97K |
| 24h成交 | $112.2K |
| 持有者 | 69 |

**Twitter 讨论:**
- @heyibinance - 13小时前

---
- 创建时间：2026-02-26
- 来源：GMGN 页面分析
