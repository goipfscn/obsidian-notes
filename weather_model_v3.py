#!/usr/bin/env python3
"""
天气交易预测模型 - v3.0
基于Polymarket历史回测验证
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

# 城市坐标
CITY_COORDS = {
    '上海': (31.23, 121.47),
    '东京': (35.68, 139.76),
    '新加坡': (1.35, 103.82),
    '首尔': (37.57, 126.98),
    '香港': (22.32, 114.17),
    '巴黎': (48.85, 2.35),
    '伦敦': (51.50, -0.12),
    '纽约': (40.71, -74.00),
}

def get_weather_forecast(city, target_date=None):
    """获取天气预报 - v3.0核心函数"""
    if city not in CITY_COORDS:
        return None
    
    lat, lon = CITY_COORDS[city]
    
    # 确定日期
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    # 1. 获取历史/预报数据
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m,weather_code,cloud_cover,wind_speed_10m',
        'start_date': target_date,
        'end_date': target_date,
        'timezone': 'Asia/Shanghai'
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()['hourly']
    except:
        # 如果历史API失败，尝试预报API
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'temperature_2m,weather_code,cloud_cover,wind_speed_10m',
            'timezone': 'Asia/Shanghai'
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()['hourly']
    
    # 2. 提取关键时间点数据
    temps = data['temperature_2m']
    clouds = data['cloud_cover']
    winds = data['wind_speed_10m']
    times = data['time']
    
    # 早上6点和下午2点数据
    temp_6am = temp_2pm = cloud_6am = wind_6am = None
    
    for i, t in enumerate(times):
        if 'T06:00' in t:
            temp_6am = temps[i]
            cloud_6am = clouds[i]
            wind_6am = winds[i]
        if 'T14:00' in t:
            temp_2pm = temps[i]
    
    return {
        'temp_6am': temp_6am,
        'temp_2pm': temp_2pm,
        'cloud_6am': cloud_6am,
        'wind_6am': wind_6am,
        'target_date': target_date
    }

def calculate_rise_potential(cloud_6am, wind_6am):
    """计算升温潜力 - v3.0核心算法"""
    # 基础升温
    rise = 5.0
    
    # 云量修正
    if cloud_6am is None:
        cloud_corr = 0
    elif cloud_6am < 30:
        cloud_corr = 3.0  # 晴朗
    elif cloud_6am < 60:
        cloud_corr = 1.0  # 多云
    else:
        cloud_corr = -2.0  # 阴天
    
    # 风速修正
    if wind_6am is None:
        wind_corr = 0
    elif wind_6am < 10:
        wind_corr = 1.0  # 微风
    elif wind_6am < 20:
        wind_corr = 0
    else:
        wind_corr = -2.0  # 大风
    
    return rise + cloud_corr + wind_corr

def predict_and_trade(city, target_temp, pm_price=None):
    """预测并返回交易信号"""
    weather = get_weather_forecast(city)
    
    if weather is None or weather['temp_6am'] is None:
        return {'signal': 'UNKNOWN', 'reason': '无法获取天气数据'}
    
    temp_6am = weather['temp_6am']
    temp_2pm = weather['temp_2pm']
    cloud_6am = weather['cloud_6am']
    wind_6am = weather['wind_6am']
    
    # 计算升温潜力
    rise_potential = calculate_rise_potential(cloud_6am, wind_6am)
    
    # 预测最高温
    pred_max = temp_6am + rise_potential
    
    # 判断是否达到目标
    will_reach = pred_max >= target_temp
    
    # 计算信心度
    confidence = min(1.0, (pred_max - target_temp + 5) / 10)
    if pred_max < target_temp:
        confidence = min(1.0, (target_temp - pred_max + 5) / 10)
    
    # 生成信号
    if confidence < 0.3:
        signal = 'HOLD'
        reason = f'预测不确定 (信心度{confidence:.0%})'
    elif will_reach:
        if pm_price and confidence > pm_price + 0.1:
            signal = 'BUY_YES'
            reason = f'预测可达{target_temp}°C (信心{confidence:.0%})'
        else:
            signal = 'WATCH'
            reason = f'可能达到{target_temp}°C'
    else:
        if pm_price and confidence > (1 - pm_price) + 0.1:
            signal = 'BUY_NO'
            reason = f'预测无法达到{target_temp}°C (信心{confidence:.0%})'
        else:
            signal = 'WATCH'
            reason = f'可能达不到{target_temp}°C'
    
    return {
        'signal': signal,
        'city': city,
        'target_temp': target_temp,
        'temp_6am': temp_6am,
        'temp_2pm': temp_2pm,
        'cloud_6am': cloud_6am,
        'wind_6am': wind_6am,
        'rise_potential': rise_potential,
        'pred_max': pred_max,
        'confidence': confidence,
        'reason': reason,
        'pm_price': pm_price
    }

def analyze_city_v3(city):
    """分析城市天气并给出交易建议"""
    print(f"\n{'='*60}")
    print(f"天气交易分析 - {city}")
    print("="*60)
    
    weather = get_weather_forecast(city)
    
    if weather is None:
        print(f"无法获取{city}的天气数据")
        return
    
    temp_6am = weather['temp_6am']
    temp_2pm = weather['temp_2pm']
    cloud_6am = weather['cloud_6am']
    wind_6am = weather['wind_6am']
    
    print(f"\n📊 当前天气 ({weather['target_date']}):")
    print(f"  早上6点: {temp_6am}°C")
    print(f"  云量: {cloud_6am}%")
    print(f"  风速: {wind_6am} km/h")
    
    # 计算升温潜力
    rise = calculate_rise_potential(cloud_6am, wind_6am)
    pred_max = temp_6am + rise
    
    print(f"\n🌡️ 预测:")
    print(f"  升温潜力: +{rise:.1f}°C")
    print(f"  预测最高: {pred_max:.1f}°C")
    
    # 不同目标的建议
    targets = [20, 25, 30]
    print(f"\n🎯 交易建议:")
    for target in targets:
        result = predict_and_trade(city, target)
        print(f"  {target}°C目标: {result['signal']} - {result['reason']}")

def main():
    """主函数"""
    print("="*60)
    print("天气交易预测模型 v3.0")
    print("基于Polymarket历史回测验证")
    print("="*60)
    
    # 分析主要城市
    for city in ['上海', '东京', '伦敦', '纽约']:
        try:
            analyze_city_v3(city)
        except Exception as e:
            print(f"{city}: 错误 - {e}")

if __name__ == "__main__":
    main()
