#!/usr/bin/env python3
"""
Тестовый скрипт для Foursquare Places API
"""

import requests
import json

def test_foursquare_api():
    """Тестирует Foursquare Places API"""
    
    # URL для Place Search API
    url = "https://api.foursquare.com/v3/places/search"
    
    # Параметры запроса
    params = {
        "query": "coffee",
        "ll": "55.7558,37.6176",  # Координаты Москвы
        "radius": 1000,  # Радиус поиска в метрах
        "limit": 5  # Ограничение количества результатов
    }
    
    # Заголовки (без API ключа для тестирования)
    headers = {
        "Accept": "application/json"
    }
    
    print("=== Тестирование Foursquare Places API ===")
    print(f"URL: {url}")
    print(f"Параметры: {params}")
    print(f"Заголовки: {headers}")
    print()
    
    try:
        # Выполняем запрос
        print("Выполняю запрос...")
        response = requests.get(url, params=params, headers=headers)
        
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print()
        
        # Пытаемся получить JSON ответ
        try:
            data = response.json()
            print("Ответ API:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Ответ не является валидным JSON:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

def test_with_demo_key():
    """Тестирует API с демо ключом (если доступен)"""
    
    # Некоторые API предоставляют демо ключи
    demo_keys = [
        "demo",
        "test", 
        "sample",
        "public"
    ]
    
    url = "https://api.foursquare.com/v3/places/search"
    params = {
        "query": "coffee",
        "ll": "55.7558,37.6176",
        "limit": 3
    }
    
    print("\n=== Тестирование с демо ключами ===")
    
    for demo_key in demo_keys:
        headers = {
            "Accept": "application/json",
            "Authorization": demo_key
        }
        
        print(f"\nПробую демо ключ: {demo_key}")
        
        try:
            response = requests.get(url, params=params, headers=headers)
            print(f"Статус код: {response.status_code}")
            
            if response.status_code != 401:  # Если не ошибка авторизации
                try:
                    data = response.json()
                    print("Успешный ответ:")
                    print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")
                    break
                except:
                    print("Ответ:", response.text[:200])
            else:
                print("Ошибка авторизации")
                
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    test_foursquare_api()
    test_with_demo_key()

