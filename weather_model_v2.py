#!/usr/bin/env python3
"""
天气交易预测模型 - v2.0
包含yuyu实战经验特征
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
import json
import os

# 数据路径
DATA_PATH = "/tmp/weather_history_1year.csv"
OUTPUT_DIR = "/root/.openclaw/workspace"

def load_data():
    """加载天气数据"""
    df = pd.read_csv(DATA_PATH)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

def extract_features(df, hour=13):
    """
    提取特征
    
    基础特征:
    - temp: 气温
    - humidity: 湿度
    - wind_speed: 风速
    - wind_dir: 风向
    - cloud_cover: 云量
    - pressure: 气压
    - month: 月份
    
    yuyu特征:
    - is_calm: 静风 (<3m/s)
    - is_sunny: 晴天 (<20%云)
    - is_warm_dir: 暖风 (135-225°)
    - is_rain: 下雨 (有降水)
    - is_sea_wind: 海风 (180-270°+高湿度)
    - is_cloudy: 阴天 (>80%云)
    - is_inversion: 逆温条件 (下雨+阴天+海风)
    """
    
    # 筛选时间点
    data = df[df['datetime'].dt.hour == hour].copy()
    data['date'] = pd.to_datetime(data['datetime'].dt.date)
    data['month'] = data['datetime'].dt.month
    
    # 获取当天最高温
    daily_max = df.groupby([df['datetime'].dt.date, 'city'])['temp'].max().reset_index()
    daily_max.columns = ['date', 'city', 'max_temp']
    data['date'] = data['date'].dt.date
    data = data.merge(daily_max, on=['date', 'city'], how='inner')
    
    # === 基础特征 ===
    data['is_calm'] = (data['wind_speed'] < 3).astype(int)
    data['is_sunny'] = (data['cloud_cover'] < 20).astype(int)
    data['is_warm_dir'] = ((data['wind_dir'] >= 135) & (data['wind_dir'] <= 225)).astype(int)
    
    # === yuyu实战特征 ===
    # 下雨
    data['is_rain'] = (data['precipitation'] > 0).astype(int) if 'precipitation' in data.columns else 0
    
    # 海风 (东南风+高湿度)
    data['is_sea_wind'] = ((data['wind_dir'] >= 180) & 
                           (data['wind_dir'] <= 270) & 
                           (data['humidity'] > 70)).astype(int)
    
    # 阴天
    data['is_cloudy'] = (data['cloud_cover'] > 80).astype(int)
    
    # 逆温条件 (下雨+阴天+海风) - 晚间可能升温
    data['is_inversion'] = (data['is_rain'] & data['is_cloudy'] & data['is_sea_wind']).astype(int)
    
    # 综合信号
    data['hot_signal'] = data['is_sunny'] + data['is_calm'] + data['is_warm_dir']
    data['inversion_signal'] = data['is_rain'] + data['is_cloudy'] + data['is_sea_wind']
    
    return data

def train_regressor(data, features):
    """训练预测最高温的回归模型"""
    X = data[features]
    y = data['max_temp']
    
    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=6,
        random_state=42
    )
    
    # 交叉验证
    scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
    print(f"交叉验证 MAE: {-scores.mean():.2f}°C (±{scores.std():.2f})")
    
    # 训练
    model.fit(X, y)
    
    # 预测
    data['pred_max'] = model.predict(X)
    data['error'] = data['pred_max'] - data['max_temp']
    
    print(f"训练集 MAE: {abs(data['error']).mean():.2f}°C")
    
    return model, data

def analyze_city(city, hour=13):
    """分析单个城市"""
    print(f"\n{'='*60}")
    print(f"城市: {city}, 时间点: {hour}:00")
    print("="*60)
    
    df = load_data()
    city_data = df[df['city'] == city].copy()
    
    data = extract_features(city_data, hour)
    
    # 特征列表
    features = [
        'temp', 'humidity', 'wind_speed', 'wind_dir', 
        'cloud_cover', 'pressure', 'month',
        'is_calm', 'is_sunny', 'is_warm_dir',
        'is_rain', 'is_sea_wind', 'is_cloudy', 'is_inversion'
    ]
    
    # 训练模型
    model, data = train_regressor(data, features)
    
    # 特征重要性
    importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n特征重要性:")
    for _, row in importance.head(10).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    return model, data, importance

def predict_today(city, hour=13):
    """预测今天的温度"""
    # 获取当前天气数据
    city_coords = {
        '上海': (31.23, 121.47),
        '东京': (35.68, 139.76),
        '新加坡': (1.35, 103.82),
        '首尔': (37.57, 126.98),
        '香港': (22.32, 114.17),
        '巴黎': (48.85, 2.35),
        '伦敦': (51.50, -0.12),
        '纽约': (40.71, -74.00),
    }
    
    if city not in city_coords:
        print(f"未知城市: {city}")
        return
    
    lat, lon = city_coords[city]
    
    # 调用Open-Meteo API
    import requests
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m,cloud_cover,surface_pressure',
        'timezone': 'Asia/Shanghai'
    }
    
    resp = requests.get(url, params=params)
    current = resp.json()['current']
    
    # 准备特征
    now = pd.Timestamp.now()
    features = {
        'temp': current['temperature_2m'],
        'humidity': current['relative_humidity_2m'],
        'wind_speed': current['wind_speed_10m'] / 3.6,  # km/h -> m/s
        'wind_dir': current['wind_direction_10m'],
        'cloud_cover': current['cloud_cover'],
        'pressure': current['surface_pressure'],
        'month': now.month,
        'is_calm': 1 if current['wind_speed_10m']/3.6 < 3 else 0,
        'is_sunny': 1 if current['cloud_cover'] < 20 else 0,
        'is_warm_dir': 1 if 135 <= current['wind_direction_10m'] <= 225 else 0,
        'is_rain': 1 if current['precipitation'] > 0 else 0,
        'is_sea_wind': 1 if (180 <= current['wind_direction_10m'] <= 270 and current['relative_humidity_2m'] > 70) else 0,
        'is_cloudy': 1 if current['cloud_cover'] > 80 else 0,
        'is_inversion': 0,  # 需要综合判断
    }
    
    # 判断逆温
    features['is_inversion'] = int(features['is_rain'] and features['is_cloudy'] and features['is_sea_wind'])
    
    print(f"\n当前天气 ({city}):")
    print(f"  气温: {features['temp']}°C")
    print(f"  云量: {features['cloud_cover']}%")
    print(f"  风速: {features['wind_speed']:.1f} m/s")
    print(f"  风向: {features['wind_dir']}°")
    print(f"  湿度: {features['humidity']}%")
    print(f"  降水: {current['precipitation']} mm")
    print(f"\n信号:")
    print(f"  高温信号: {features['is_sunny'] + features['is_calm'] + features['is_warm_dir']}/3")
    print(f"  逆温信号: {features['is_inversion']}")
    
    return features

def main():
    """主函数"""
    print("天气交易预测模型 v2.0")
    print("="*60)
    
    # 分析主要城市
    cities = ['上海', '东京', '新加坡', '首尔', '香港', '巴黎', '伦敦', '纽约']
    
    for city in cities:
        try:
            analyze_city(city, hour=13)
        except Exception as e:
            print(f"{city}: 错误 - {e}")
    
    # 预测今天
    print("\n" + "="*60)
    print("今日预测")
    print("="*60)
    predict_today('上海')

if __name__ == "__main__":
    main()
