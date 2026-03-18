#!/usr/bin/env python3
"""
天气交易预测模型 - v2.1
包含yuyu实战经验 + 逆温现象识别
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import requests

# 数据路径
DATA_PATH = "/tmp/weather_history_1year.csv"

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

def load_data():
    """加载天气数据"""
    df = pd.read_csv(DATA_PATH)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

def get_realtime_weather(city):
    """获取实时天气 + 历史同一天实际温度"""
    if city not in CITY_COORDS:
        print(f"未知城市: {city}")
        return None
    
    lat, lon = CITY_COORDS[city]
    
    # 1. 当前实时数据 (Open-Meteo)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m,cloud_cover,surface_pressure',
        'hourly': 'temperature_2m',
        'timezone': 'Asia/Shanghai'
    }
    
    resp = requests.get(url, params=params, timeout=10)
    current = resp.json()['current']
    hourly = resp.json()['hourly']
    
    # 2. 获取今天实际观测温度 (Archive API)
    today = pd.Timestamp.now().strftime('%Y-%m-%d')
    url2 = "https://archive-api.open-meteo.com/v1/archive"
    params2 = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m',
        'start_date': today,
        'end_date': today,
        'timezone': 'Asia/Shanghai'
    }
    
    try:
        resp2 = requests.get(url2, params=params2, timeout=10)
        actual_temps = resp2.json()['hourly']['temperature_2m']
        actual_times = resp2.json()['hourly']['time']
        
        # 找到今天最高温度和出现时间
        max_temp = max(actual_temps)
        max_time = actual_times[actual_temps.index(max_temp)]
        
        # 找到今天最低温度
        min_temp = min(actual_temps)
        min_time = actual_times[actual_temps.index(min_temp)]
        
        has_inversion = max_time.startswith(today + 'T00') or max_time.startswith(today + 'T01') or max_time.startswith(today + 'T02') or max_time.startswith(today + 'T03') or max_time.startswith(today + 'T04') or max_time.startswith(today + 'T05')
        
    except:
        max_temp = None
        max_time = None
        min_temp = None
        min_time = None
        has_inversion = False
    
    # 3. 获取机场METAR数据
    metar = get_metar(city)
    
    return {
        'current': current,
        'today_max': max_temp,
        'today_max_time': max_time,
        'today_min': min_temp,
        'today_min_time': min_time,
        'has_inversion': has_inversion,
        'metar': metar
    }

def get_metar(city):
    """获取机场METAR数据"""
    airports = {
        '上海': ['ZSSS', 'ZSPD'],
        '东京': ['RJTT', 'RJND'],
        '新加坡': ['WSSS'],
        '首尔': ['RKSI', 'RKJK'],
        '香港': ['VHHH'],
        '巴黎': ['LFPG', 'LFPB'],
        '伦敦': ['EGLL', 'EGLC'],
        '纽约': ['KJFK', 'KLAX'],
    }
    
    if city not in airports:
        return None
    
    ids = ','.join(airports[city])
    url = f"https://aviationweather.gov/api/data/metar?ids={ids}&format=json"
    
    try:
        resp = requests.get(url, timeout=5)
        return resp.json()
    except:
        return None

def analyze_city(city):
    """分析城市天气"""
    print(f"\n{'='*60}")
    print(f"城市: {city}")
    print("="*60)
    
    data = get_realtime_weather(city)
    if not data:
        return
    
    current = data['current']
    
    print(f"\n📡 当前天气 ({current['time']}):")
    print(f"  气温: {current['temperature_2m']}°C")
    print(f"  湿度: {current['relative_humidity_2m']}%")
    print(f"  风速: {current['wind_speed_10m']} km/h")
    print(f"  风向: {current['wind_direction_10m']}°")
    print(f"  云量: {current['cloud_cover']}%")
    print(f"  气压: {current['surface_pressure']} hPa")
    print(f"  降水: {current['precipitation']} mm")
    
    # 解析天气
    wind_speed_ms = current['wind_speed_10m'] / 3.6
    wind_dir = current['wind_direction_10m']
    
    # 信号
    is_calm = 1 if wind_speed_ms < 3 else 0
    is_sunny = 1 if current['cloud_cover'] < 20 else 0
    is_warm_dir = 1 if 135 <= wind_dir <= 225 else 0
    is_rain = 1 if current['precipitation'] > 0 else 0
    is_cloudy = 1 if current['cloud_cover'] > 80 else 0
    is_sea_wind = 1 if (90 <= wind_dir <= 180 and current['relative_humidity_2m'] > 70) else 0
    
    hot_signal = is_sunny + is_calm + is_warm_dir
    inversion_signal = is_rain + is_cloudy + is_sea_wind
    
    print(f"\n🌡️ 信号分析:")
    print(f"  高温信号: {hot_signal}/3")
    print(f"    - 静风: {'✓' if is_calm else '✗'}")
    print(f"    - 晴天: {'✓' if is_sunny else '✗'}")
    print(f"    - 暖风: {'✓' if is_warm_dir else '✗'}")
    
    print(f"\n🔄 逆温信号: {inversion_signal}/3")
    print(f"    - 下雨: {'✓' if is_rain else '✗'}")
    print(f"    - 阴天: {'✓' if is_cloudy else '✗'}")
    print(f"    - 海风: {'✓' if is_sea_wind else '✗'}")
    
    if data['today_max']:
        print(f"\n📊 今天实际温度:")
        print(f"  最高: {data['today_max']}°C ({data['today_max_time']})")
        print(f"  最低: {data['today_min']}°C ({data['today_min_time']})")
        
        if data['has_inversion']:
            print(f"\n⚠️  逆温现象！最高温出现在凌晨/早上！")
    
    # 机场数据
    if data['metar']:
        print(f"\n🛫 机场METAR:")
        for m in data['metar'][:2]:
            print(f"  {m.get('icaoId', 'N/A')}: {m.get('temp', 'N/A')}°C, {m.get('wdir', 'N/A')}°/{m.get('wspd', 'N/A')}m/s, {m.get('wxString', 'N/A')}")

def predict_pm(city):
    """预测Polymarket结果"""
    print(f"\n{'='*60}")
    print(f"Polymarket 预测")
    print("="*60)
    
    # 获取PM市场
    import subprocess
    result = subprocess.run(
        ['polymarket', 'markets', 'search', f'{city} March {pd.Timestamp.now().day} temperature', '--limit', '15'],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(result.stdout)
    
    # 简单预测
    data = get_realtime_weather(city)
    if data and data['today_max']:
        print(f"\n🎯 实际预测:")
        print(f"  今天最高: {data['today_max']}°C")
        print(f"  建议关注: {data['today_max']}°C 对应的市场")

def main():
    """主函数"""
    print("天气交易预测模型 v2.1")
    print("="*60)
    print("包含: 逆温现象识别 + yuyu实战经验")
    
    cities = ['上海', '东京', '新加坡', '首尔', '香港', '巴黎', '伦敦', '纽约']
    
    for city in cities:
        try:
            analyze_city(city)
        except Exception as e:
            print(f"{city}: 错误 - {e}")
    
    # 详细分析上海
    print("\n" + "="*60)
    print("上海 Polymarket 市场分析")
    print("="*60)
    predict_pm('上海')

if __name__ == "__main__":
    main()
