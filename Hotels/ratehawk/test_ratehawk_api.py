#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации работы с RateHawk API
Поскольку у нас нет реального API ключа, создадим симуляцию запроса
"""

import requests
import json
from datetime import datetime, timedelta

def simulate_ratehawk_api_request():
    """
    Симуляция запроса к RateHawk API для поиска отелей по координатам
    """
    
    # API endpoint для поиска по географическим координатам
    url = "https://api.worldota.net/api/b2b/v3/search/serp/geo/"
    
    # Пример данных запроса (координаты Берлина)
    request_data = {
        "checkin": "2025-10-22",
        "checkout": "2025-10-25", 
        "residency": "gb",
        "language": "en",
        "guests": [
            {
                "adults": 2,
                "children": []
            }
        ],
        "longitude": 13.38886,
        "latitude": 52.517036,
        "radius": 150,
        "currency": "EUR"
    }
    
    # Заголовки запроса
    headers = {
        "Content-Type": "application/json"
    }
    
    print("=== ДЕМОНСТРАЦИЯ ЗАПРОСА К RATEHAWK API ===\n")
    print(f"URL: {url}")
    print(f"Метод: POST")
    print(f"Заголовки: {json.dumps(headers, indent=2)}")
    print(f"Данные запроса:")
    print(json.dumps(request_data, indent=2))
    
    print("\n=== ПОПЫТКА ВЫПОЛНЕНИЯ ЗАПРОСА ===\n")
    
    # Поскольку у нас нет реального API ключа, попробуем выполнить запрос
    # чтобы увидеть ответ об ошибке аутентификации
    try:
        # Попытка запроса без аутентификации
        response = requests.post(url, headers=headers, json=request_data, timeout=10)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        
        print(f"\nТело ответа:")
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2))
        except:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    
    return request_data

def demonstrate_api_structure():
    """
    Демонстрация структуры API и возможных ответов
    """
    print("\n=== СТРУКТУРА API RATEHAWK ===\n")
    
    # Основные endpoints
    endpoints = {
        "Поиск по координатам": "https://api.worldota.net/api/b2b/v3/search/serp/geo/",
        "Поиск по региону": "https://api.worldota.net/api/b2b/v3/search/serp/region/",
        "Поиск по ID отелей": "https://api.worldota.net/api/b2b/v3/search/serp/hotels/",
        "Получение страницы отеля": "https://api.worldota.net/api/b2b/v3/hotel/info/",
        "Предварительное бронирование": "https://api.worldota.net/api/b2b/v3/hotel/prebook/",
        "Создание бронирования": "https://api.worldota.net/api/b2b/v3/hotel/order/booking/form/"
    }
    
    print("Основные endpoints:")
    for name, url in endpoints.items():
        print(f"  {name}: {url}")
    
    # Пример структуры ответа
    example_response = {
        "data": {
            "hotels": [
                {
                    "id": "maritim_proarte_hotel_berlin",
                    "hid": 7579288,
                    "rates": [
                        {
                            "match_hash": "m-742e399d-109a-51a3-b093-111fe78b7e1b",
                            "search_hash": "sr-0193a8fe-d797-7a95-9c96-42ca56746087",
                            "daily_prices": ["159.47", "159.47", "159.47"],
                            "meal": "nomeal",
                            "payment_options": {
                                "payment_types": [
                                    {
                                        "amount": "507.00",
                                        "show_amount": "478.40",
                                        "currency_code": "EUR",
                                        "type": "deposit"
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
    
    print(f"\nПример структуры ответа:")
    print(json.dumps(example_response, indent=2))

if __name__ == "__main__":
    # Выполняем демонстрацию
    request_data = simulate_ratehawk_api_request()
    demonstrate_api_structure()
    
    print("\n=== ЗАКЛЮЧЕНИЕ ===\n")
    print("Для полноценного тестирования API RateHawk необходимо:")
    print("1. Зарегистрироваться на https://www.ratehawk.com/")
    print("2. Получить API ключ в формате KEY_ID:API_KEY")
    print("3. Использовать HTTP Basic Authentication")
    print("4. Для тестирования использовать тестовый отель с hid=8473727")
    print("5. Учитывать лимиты запросов (указываются в заголовках ответа)")

