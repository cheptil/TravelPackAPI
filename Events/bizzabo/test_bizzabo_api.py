#!/usr/bin/env python3
"""
Тестовый скрипт для Bizzabo Partner API
Выполняет запросы к Mock Server для демонстрации функциональности API
"""

import requests
import json
from datetime import datetime

# Конфигурация API
MOCK_SERVER_BASE_URL = "https://stoplight.io/mocks/bizzabo/bizzabo-partner-apis/38558236"
LIVE_SERVER_BASE_URL = "https://api.bizzabo.com/v1"

# Заголовки для запросов
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer mock_token_123"  # Для Mock Server
}

def test_list_events():
    """
    Тестирует эндпоинт List Events
    """
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ЭНДПОИНТА: List Events")
    print("=" * 60)
    
    # URL для Mock Server
    url = f"{MOCK_SERVER_BASE_URL}/v1/events"
    
    print(f"URL: {url}")
    print(f"Метод: GET")
    print(f"Заголовки: {json.dumps(HEADERS, indent=2, ensure_ascii=False)}")
    
    try:
        # Выполняем запрос
        print("\nВыполняем запрос...")
        response = requests.get(url, headers=HEADERS, timeout=30)
        
        # Информация о ответе
        print(f"\nСтатус код: {response.status_code}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # Тело ответа
        print(f"\nТело ответа:")
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                json_data = response.json()
                print(json.dumps(json_data, indent=2, ensure_ascii=False))
                return json_data
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON")
                print(response.text)
        else:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    
    return response

def test_list_events_with_parameters():
    """
    Тестирует эндпоинт List Events с параметрами
    """
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЭНДПОИНТА: List Events с параметрами")
    print("=" * 60)
    
    # URL для Mock Server с параметрами
    url = f"{MOCK_SERVER_BASE_URL}/v1/events"
    
    # Параметры запроса
    params = {
        "page": 1,
        "size": 10,
        "sort": "created_at"
    }
    
    print(f"URL: {url}")
    print(f"Метод: GET")
    print(f"Параметры: {json.dumps(params, indent=2, ensure_ascii=False)}")
    print(f"Заголовки: {json.dumps(HEADERS, indent=2, ensure_ascii=False)}")
    
    try:
        # Выполняем запрос
        print("\nВыполняем запрос...")
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        
        # Информация о ответе
        print(f"\nСтатус код: {response.status_code}")
        print(f"Финальный URL: {response.url}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # Тело ответа
        print(f"\nТело ответа:")
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                json_data = response.json()
                print(json.dumps(json_data, indent=2, ensure_ascii=False))
                return json_data
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON")
                print(response.text)
        else:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    
    return response

def test_get_account():
    """
    Тестирует эндпоинт Get Account
    """
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЭНДПОИНТА: Get Account")
    print("=" * 60)
    
    # URL для Mock Server
    url = f"{MOCK_SERVER_BASE_URL}/v1/account"
    
    print(f"URL: {url}")
    print(f"Метод: GET")
    print(f"Заголовки: {json.dumps(HEADERS, indent=2, ensure_ascii=False)}")
    
    try:
        # Выполняем запрос
        print("\nВыполняем запрос...")
        response = requests.get(url, headers=HEADERS, timeout=30)
        
        # Информация о ответе
        print(f"\nСтатус код: {response.status_code}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # Тело ответа
        print(f"\nТело ответа:")
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                json_data = response.json()
                print(json.dumps(json_data, indent=2, ensure_ascii=False))
                return json_data
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON")
                print(response.text)
        else:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    
    return response

def main():
    """
    Основная функция для выполнения всех тестов
    """
    print("ТЕСТИРОВАНИЕ BIZZABO PARTNER API")
    print(f"Время выполнения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mock Server: {MOCK_SERVER_BASE_URL}")
    
    # Выполняем тесты
    results = {}
    
    # Тест 1: List Events (базовый)
    results['list_events_basic'] = test_list_events()
    
    # Тест 2: List Events с параметрами
    results['list_events_with_params'] = test_list_events_with_parameters()
    
    # Тест 3: Get Account
    results['get_account'] = test_get_account()
    
    # Сводка результатов
    print("\n" + "=" * 60)
    print("СВОДКА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    for test_name, result in results.items():
        if result and hasattr(result, 'status_code'):
            status = "✅ УСПЕШНО" if result.status_code == 200 else f"❌ ОШИБКА ({result.status_code})"
            print(f"{test_name}: {status}")
        else:
            print(f"{test_name}: ❌ ОШИБКА (Нет ответа)")
    
    return results

if __name__ == "__main__":
    results = main()

