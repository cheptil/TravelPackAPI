#!/usr/bin/env python3
"""
Тестирование API Sixt
Скрипт для выполнения тестовых запросов к API Sixt
"""

import requests
import json
from datetime import datetime, timedelta

def test_sixt_api():
    """Тестирование различных endpoints API Sixt"""
    
    print("=== Тестирование API Sixt ===\n")
    
    # Базовый URL API
    base_url = "https://api.orange.sixt.com/v1"
    
    # 1. Тест поиска станций
    print("1. Тестирование поиска станций...")
    search_url = f"{base_url}/locations"
    search_params = {
        'term': 'Munich',
        'vehicleType': 'car',
        'type': 'station'
    }
    
    try:
        print(f"Запрос: {search_url}")
        print(f"Параметры: {search_params}")
        
        response = requests.get(search_url, params=search_params, timeout=10)
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный ответ! Найдено станций: {len(data) if isinstance(data, list) else 'неизвестно'}")
            print("Первые 3 результата:")
            if isinstance(data, list) and len(data) > 0:
                for i, station in enumerate(data[:3]):
                    print(f"  {i+1}. {station}")
            else:
                print(f"Структура ответа: {type(data)}")
                print(f"Содержимое: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Текст ответа: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        print(f"Текст ответа: {response.text[:500]}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Тест получения деталей станции (если есть ID)
    print("2. Тестирование получения деталей станции...")
    station_id = "S_5252"  # Пример ID из документации
    station_url = f"{base_url}/locations/{station_id}"
    
    try:
        print(f"Запрос: {station_url}")
        
        response = requests.get(station_url, timeout=10)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ!")
            print(f"Детали станции: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Текст ответа: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        print(f"Текст ответа: {response.text[:500]}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Тест поиска предложений аренды
    print("3. Тестирование поиска предложений аренды...")
    offers_url = f"{base_url}/rentaloffers/offers"
    
    # Создаем даты для тестирования (завтра и послезавтра)
    pickup_date = datetime.now() + timedelta(days=1)
    return_date = datetime.now() + timedelta(days=3)
    
    offers_params = {
        'pickupStation': station_id,
        'returnStation': station_id,
        'pickupDate': pickup_date.strftime('%Y-%m-%dT14:00:00'),
        'returnDate': return_date.strftime('%Y-%m-%dT14:00:00'),
        'vehicleType': 'car',
        'currency': 'EUR',
        'isoCountryCode': 'DE'
    }
    
    try:
        print(f"Запрос: {offers_url}")
        print(f"Параметры: {offers_params}")
        
        response = requests.get(offers_url, params=offers_params, timeout=10)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ!")
            print(f"Предложения аренды: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Текст ответа: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        print(f"Текст ответа: {response.text[:500]}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. Тест специального endpoint для управления автомобилем
    print("4. Тестирование специального endpoint управления автомобилем...")
    car_control_url = "https://api.orange.sixt.com/v2/apps/hackatum2022/twingo/blink"
    
    try:
        print(f"Запрос: {car_control_url}")
        
        response = requests.post(car_control_url, timeout=10)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            print("Успешный ответ!")
            print(f"Ответ: {response.text}")
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Текст ответа: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    
    print("\n=== Тестирование завершено ===")

if __name__ == "__main__":
    test_sixt_api()

