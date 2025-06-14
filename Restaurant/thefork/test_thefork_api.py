#!/usr/bin/env python3
"""
Тестовый скрипт для TheFork API
Выполняет тестовые запросы к различным endpoints
"""

import requests
import json
from datetime import datetime, timedelta

def test_b2b_customers_endpoint():
    """Тестирует B2B-API endpoint для получения списка клиентов"""
    
    # Базовый URL для B2B-API
    base_url = "https://api.thefork.io/manager"
    endpoint = "/v1/customers"
    
    # Параметры запроса (используем тестовые значения)
    params = {
        'groupUuid': 'test-group-uuid-12345',
        'startDate': '2024-01-01',
        'endDate': '2024-12-31',
        'limit': 10,
        'page': 1
    }
    
    # Заголовки
    headers = {
        'Accept': '*/*',
        'User-Agent': 'TheFork-API-Test/1.0'
    }
    
    print("=== Тестирование B2B-API: Get customers list ===")
    print(f"URL: {base_url}{endpoint}")
    print(f"Параметры: {json.dumps(params, indent=2)}")
    print(f"Заголовки: {json.dumps(headers, indent=2)}")
    print()
    
    try:
        response = requests.get(
            f"{base_url}{endpoint}",
            params=params,
            headers=headers,
            timeout=10
        )
        
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print()
        
        # Попытка парсинга JSON ответа
        try:
            response_json = response.json()
            print("JSON ответ:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Текстовый ответ:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    
    print("\n" + "="*50 + "\n")

def test_pos_create_endpoint():
    """Тестирует POS-API endpoint для создания POS"""
    
    # Базовый URL для POS-API
    base_url = "https://api.thefork.io/pos"
    endpoint = "/v1/create"
    
    # Тестовые данные для создания POS
    data = {
        "homepageUrl": "https://example-restaurant.com",
        "name": "Test Restaurant POS",
        "type": "restaurant",
        "oauthAuthorizeUrl": "https://example-restaurant.com/oauth/authorize",
        "oauthClientId": "test-client-id",
        "oauthClientSecret": "test-client-secret",
        "oauthScope": ["read", "write"],
        "oauthTokenUrl": "https://example-restaurant.com/oauth/token",
        "receiptOpeningUrl": "https://example-restaurant.com/receipt",
        "webhookToken": "test-webhook-token"
    }
    
    # Заголовки
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'X-Api-Key': 'test-api-key-12345',
        'User-Agent': 'TheFork-API-Test/1.0'
    }
    
    print("=== Тестирование POS-API: Create POS ===")
    print(f"URL: {base_url}{endpoint}")
    print(f"Данные: {json.dumps(data, indent=2)}")
    print(f"Заголовки: {json.dumps(headers, indent=2)}")
    print()
    
    try:
        response = requests.post(
            f"{base_url}{endpoint}",
            json=data,
            headers=headers,
            timeout=10
        )
        
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print()
        
        # Попытка парсинга JSON ответа
        try:
            response_json = response.json()
            print("JSON ответ:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Текстовый ответ:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    
    print("\n" + "="*50 + "\n")

def main():
    """Основная функция для выполнения тестов"""
    print("Начинаем тестирование TheFork API")
    print("Примечание: Ожидаются ошибки аутентификации, так как используются тестовые ключи")
    print("="*70)
    print()
    
    # Тестируем B2B-API
    test_b2b_customers_endpoint()
    
    # Тестируем POS-API
    test_pos_create_endpoint()
    
    print("Тестирование завершено!")

if __name__ == "__main__":
    main()

