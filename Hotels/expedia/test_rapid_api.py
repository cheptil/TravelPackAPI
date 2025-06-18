#!/usr/bin/env python3
"""
Тестовый запрос к Expedia Group Rapid API
Демонстрация использования Shopping API с тестовыми заголовками
"""

import requests
import json
from datetime import datetime, timedelta

def test_rapid_api_shopping():
    """
    Выполняет тестовый запрос к Rapid Shopping API
    Использует тестовые заголовки для получения статичных ответов
    """
    
    # Базовый URL для Rapid API (предполагаемый на основе документации)
    base_url = "https://api.ean.com/v3"
    
    # Эндпоинт для поиска отелей
    endpoint = "/properties/availability"
    
    # Тестовые заголовки (из документации)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "test": "standard",  # Тестовый заголовок для получения стандартного ответа
        # Примечание: В реальном использовании здесь должен быть API ключ
        # "Authorization": "Bearer YOUR_API_KEY"
    }
    
    # Параметры запроса для поиска отелей
    # Используем Нью-Йорк как пример направления
    checkin_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    checkout_date = (datetime.now() + timedelta(days=32)).strftime("%Y-%m-%d")
    
    params = {
        "checkin": checkin_date,
        "checkout": checkout_date,
        "occupancy": "2",  # 2 взрослых
        "property_id": "12345",  # Тестовый ID отеля
        "currency": "USD",
        "language": "en-US",
        "include": "property_details,room_types,rates"
    }
    
    print("=== Тестовый запрос к Expedia Group Rapid API ===")
    print(f"URL: {base_url}{endpoint}")
    print(f"Заголовки: {json.dumps(headers, indent=2)}")
    print(f"Параметры: {json.dumps(params, indent=2)}")
    print()
    
    try:
        # Выполняем GET запрос
        print("Выполняю запрос...")
        response = requests.get(
            f"{base_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=30
        )
        
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print()
        
        # Пытаемся получить JSON ответ
        try:
            response_data = response.json()
            print("JSON ответ:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Ответ не в формате JSON:")
            print(response.text)
            
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
            "success": response.status_code == 200
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return {
            "error": str(e),
            "success": False
        }

def test_alternative_endpoint():
    """
    Тестирует альтернативный эндпоинт для получения информации о свойствах
    """
    print("\n=== Тестовый запрос к Content API ===")
    
    # Альтернативный URL на основе документации
    base_url = "https://api.ean.com/v3"
    endpoint = "/properties/content"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "test": "standard"
    }
    
    params = {
        "property_id": "12345",
        "language": "en-US",
        "include": "property_details,amenities,images"
    }
    
    print(f"URL: {base_url}{endpoint}")
    print(f"Параметры: {json.dumps(params, indent=2)}")
    
    try:
        response = requests.get(
            f"{base_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=30
        )
        
        print(f"Статус код: {response.status_code}")
        print("Ответ:")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        
        return {
            "status_code": response.status_code,
            "content": response.text,
            "success": response.status_code == 200
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    print("Начинаю тестирование Expedia Group Rapid API...")
    print("=" * 60)
    
    # Тест основного Shopping API
    result1 = test_rapid_api_shopping()
    
    # Тест Content API
    result2 = test_alternative_endpoint()
    
    print("\n" + "=" * 60)
    print("РЕЗЮМЕ ТЕСТИРОВАНИЯ:")
    print(f"Shopping API - Успешно: {result1.get('success', False)}")
    print(f"Content API - Успешно: {result2.get('success', False)}")
    
    # Сохраняем результаты в файл
    results = {
        "timestamp": datetime.now().isoformat(),
        "shopping_api": result1,
        "content_api": result2
    }
    
    with open("/home/ubuntu/api_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("Результаты сохранены в api_test_results.json")

