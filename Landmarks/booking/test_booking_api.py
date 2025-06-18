#!/usr/bin/env python3
"""
Тестовый скрипт для Booking.com Cities API
"""

import requests
import json
from datetime import datetime

def test_booking_cities_api():
    """
    Выполняет тестовый запрос к Booking.com Cities API
    """
    
    # URL API
    url = "https://demandapi.booking.com/3.1/common/locations/cities"
    
    # Заголовки запроса
    headers = {
        "Authorization": "Bearer TEST_TOKEN_HERE",  # Фиктивный токен для демонстрации
        "Content-Type": "application/json",
        "X-Affiliate-Id": "0"  # Тестовый affiliate ID
    }
    
    # Тело запроса - получаем города Нидерландов
    payload = {
        "country": "nl",
        "languages": ["en-gb", "ru"],
        "rows": 5  # Ограничиваем количество результатов для теста
    }
    
    print("=== Тестовый запрос к Booking.com Cities API ===")
    print(f"URL: {url}")
    print(f"Заголовки: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f"Тело запроса: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    print("\n" + "="*50)
    
    try:
        # Выполняем запрос
        print("Выполняю запрос...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        # Пытаемся получить JSON ответ
        try:
            response_data = response.json()
            print(f"Тело ответа (JSON):")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"Тело ответа (текст): {response.text}")
            
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "response": response.text,
            "success": response.status_code == 200
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return {
            "error": str(e),
            "success": False
        }

def test_alternative_request():
    """
    Альтернативный тестовый запрос с другими параметрами
    """
    url = "https://demandapi.booking.com/3.1/common/locations/cities"
    
    headers = {
        "Authorization": "Bearer TEST_TOKEN_HERE",
        "Content-Type": "application/json",
        "X-Affiliate-Id": "0"
    }
    
    # Запрос без фильтров - получить все города
    payload = {
        "languages": ["en-gb"],
        "rows": 3
    }
    
    print("\n=== Альтернативный тестовый запрос ===")
    print(f"Тело запроса: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Статус ответа: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Тело ответа (JSON):")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"Тело ответа (текст): {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
        return False

if __name__ == "__main__":
    print(f"Время выполнения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Основной тест
    result1 = test_booking_cities_api()
    
    # Альтернативный тест
    result2 = test_alternative_request()
    
    print("\n" + "="*50)
    print("=== РЕЗЮМЕ ТЕСТИРОВАНИЯ ===")
    print(f"Основной запрос успешен: {result1.get('success', False)}")
    print(f"Альтернативный запрос успешен: {result2}")
    
    if not result1.get('success', False):
        print("\nОжидаемый результат: API требует валидной аутентификации")
        print("Для реального использования необходимо:")
        print("1. Получить доступ к pilot программе Booking.com")
        print("2. Получить валидный Bearer token")
        print("3. Указать корректный X-Affiliate-Id")

