#!/usr/bin/env python3
"""
Тестовый запрос к Rapid API от Expedia Group
"""

import requests
import json

def test_rapid_api():
    """
    Выполняет тестовый запрос к Rapid API
    """
    
    # Базовый URL для Rapid API (предположительно)
    base_url = "https://api.ean.com/v3"
    
    # Альтернативные URL для тестирования
    alternative_urls = [
        "https://api.expediagroup.com/v3",
        "https://rapid-api.expediagroup.com/v3",
        "https://developers.expediagroup.com/api/v3"
    ]
    
    # Заголовки для тестового запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'test': 'standard',  # Тестовый заголовок из документации
        'User-Agent': 'TestClient/1.0'
    }
    
    # Параметры для поиска отелей (пример)
    params = {
        'checkin': '2025-07-01',
        'checkout': '2025-07-03',
        'occupancy': '2',
        'currency': 'USD',
        'language': 'en-US',
        'region_id': '6054439'  # Пример ID региона (Нью-Йорк)
    }
    
    print("=== Тестирование Rapid API ===\n")
    
    # Попробуем разные endpoints
    endpoints = [
        '/properties/availability',
        '/properties/search',
        '/regions',
        '/properties'
    ]
    
    for base in [base_url] + alternative_urls:
        print(f"Тестируем базовый URL: {base}")
        
        for endpoint in endpoints:
            url = base + endpoint
            print(f"\nЗапрос к: {url}")
            print(f"Заголовки: {headers}")
            print(f"Параметры: {params}")
            
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                print(f"Статус код: {response.status_code}")
                print(f"Заголовки ответа: {dict(response.headers)}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"Ответ (JSON): {json.dumps(data, indent=2, ensure_ascii=False)}")
                        return True, data
                    except json.JSONDecodeError:
                        print(f"Ответ (текст): {response.text[:500]}...")
                        return True, response.text
                else:
                    print(f"Ошибка: {response.text[:200]}...")
                    
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса: {e}")
            
            print("-" * 50)
    
    return False, None

def test_without_auth():
    """
    Тестирует публичные endpoints без аутентификации
    """
    print("\n=== Тестирование публичных endpoints ===\n")
    
    # Попробуем найти публичную документацию API
    public_urls = [
        "https://developers.expediagroup.com/docs/api",
        "https://developers.expediagroup.com/openapi",
        "https://api.expediagroup.com/docs",
        "https://rapid-api.expediagroup.com/docs"
    ]
    
    headers = {
        'User-Agent': 'TestClient/1.0',
        'Accept': 'application/json, text/html'
    }
    
    for url in public_urls:
        print(f"Проверяем: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Статус: {response.status_code}")
            if response.status_code == 200:
                print(f"Контент-тип: {response.headers.get('content-type', 'неизвестно')}")
                print(f"Размер ответа: {len(response.content)} байт")
                if 'json' in response.headers.get('content-type', ''):
                    try:
                        data = response.json()
                        print(f"JSON ответ: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
                    except:
                        pass
                return True, response
        except Exception as e:
            print(f"Ошибка: {e}")
        print("-" * 30)
    
    return False, None

if __name__ == "__main__":
    print("Начинаем тестирование Rapid API...")
    
    # Сначала попробуем основные API endpoints
    success, result = test_rapid_api()
    
    if not success:
        print("\nОсновные API endpoints недоступны, пробуем публичные...")
        success, result = test_without_auth()
    
    if success:
        print(f"\n✅ Тестирование завершено успешно!")
    else:
        print(f"\n❌ Не удалось получить доступ к API")
        print("Возможные причины:")
        print("1. Требуется регистрация и получение API ключей")
        print("2. API доступен только для зарегистрированных партнеров")
        print("3. Неправильные URL endpoints")
        print("4. Требуется специальная аутентификация")

