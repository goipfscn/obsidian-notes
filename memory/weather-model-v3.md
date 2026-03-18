# 天气交易模型 - v3.0
# 基于Polymarket历史数据回测验证

## 核心发现

### 1. 价格波动时间规律

| 时间 | 交易量 | 特点 |
|------|---------|------|
| 06:00-09:00 | 低 | 市场开盘前，适合建仓 |
| 12:00-14:00 | 中 | 午间波动 |
| 17:00-20:00 | 高 | 临近收盘，波动最大 |

### 2. 天气信号

| 信号 | 价格影响 |
|------|----------|
| 早上云量 < 50% | 价格上涨 |
| 早上云量 > 80% | 价格下跌 |
| 升温潜力 > 3°C | 价格上涨 |
| 升温潜力 < 2°C | 价格下跌 |
| 静风 < 5m/s | 利于升温 |

### 3. 验证案例

| 案例 | 日期 | 价格变化 | 天气 |
|------|------|----------|------|
| London 39-40°F | 2月14日 | +97% | 1→4.8°C |
| London 40-41°F | 2月15日 | +93% | 2→5.6°C |
| NYC 36-37°F | 2月4日 | -78% | -3°C无法升温 |

## 交易策略

### 每日流程

1. **06:00-07:00** - 获取天气预报
   - 获取城市坐标
   - 调用Open-Meteo API
   
2. **07:00-08:00** - 分析天气
   - 早上6点气温
   - 云量
   - 风速
   - 预测升温潜力
   
3. **08:00-09:00** - 决策交易
   - 判断是否达到目标温度
   - 计算边缘(edge)
   - 下注

### 特征计算

```python
def calculate_features(temp_6am, cloud_6am, wind_speed, target_temp):
    # 升温潜力
    rise_potential = 5  # 基础升温
    if cloud_6am < 30:
        rise_potential += 3  # 晴朗
    if wind_speed < 5:
        rise_potential += 2  # 静风
        
    # 预测最高温
    pred_max = temp_6am + rise_potential
    
    # 是否达到目标
    will_reach = pred_max >= target_temp
    
    return will_reach, pred_max
```

### 边缘计算

```
edge = 模型预测概率 - Polymarket价格
edge > 0.1 → 下注
```

## 文件

- /tmp/processed_temp_trades.csv - 处理后的交易数据
- /tmp/high_volatility_cases.csv - 高波动案例
- weather_model_v3.py - 模型代码
