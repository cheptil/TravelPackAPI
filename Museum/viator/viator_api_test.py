#!/usr/bin/env python3
"""
Тестовый скрипт для Viator Partner API
Демонстрирует, как сделать запрос к API для получения информации о продукте
"""

import requests
import json
from datetime import datetime

# Конфигурация API
SANDBOX_BASE_URL = "https://api.sandbox.viator.com/partner"
DEMO_API_KEY = "bcac8986-4c33-4fa0-ad3f-75409487026c"  # Демонстрационный ключ из документации
PRODUCT_CODE = "5010SYDNEY"  # Пример продукта из документации

def test_product_endpoint():
    """
    Тестирует эндпоинт /products/{product-code}
    """
    print("=== Тестирование Viator Partner API ===")
    print(f"Время запроса: {datetime.now()}")
    print(f"Базовый URL: {SANDBOX_BASE_URL}")
    print(f"Тестируемый продукт: {PRODUCT_CODE}")
    print()
    
    # Настройка заголовков
    headers = {
        "exp-api-key": DEMO_API_KEY,
        "Accept-Language": "en-US",
        "Accept": "application/json;version=2.0"
    }
    
    # URL для запроса
    url = f"{SANDBOX_BASE_URL}/products/{PRODUCT_CODE}"
    
    print(f"URL запроса: {url}")
    print("Заголовки запроса:")
    for key, value in headers.items():
        if key == "exp-api-key":
            print(f"  {key}: {value[:8]}...{value[-8:]}")  # Скрываем часть ключа
        else:
            print(f"  {key}: {value}")
    print()
    
    try:
        # Выполнение запроса
        print("Выполняем GET запрос...")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Информация о ответе
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        print()
        
        # Содержимое ответа
        if response.status_code == 200:
            print("✅ Запрос выполнен успешно!")
            try:
                data = response.json()
                print("Структура ответа:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Ответ не является валидным JSON:")
                print(response.text)
        else:
            print(f"❌ Ошибка запроса: {response.status_code}")
            print("Содержимое ответа:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
    
    return response if 'response' in locals() else None

def test_modified_since_endpoint():
    """
    Тестирует эндпоинт /products/modified-since
    """
    print("\n" + "="*50)
    print("=== Тестирование эндпоинта /products/modified-since ===")
    
    headers = {
        "exp-api-key": DEMO_API_KEY,
        "Accept-Language": "en-US",
        "Accept": "application/json;version=2.0"
    }
    
    # URL с параметрами
    url = f"{SANDBOX_BASE_URL}/products/modified-since"
    params = {
        "count": 5  # Запрашиваем только 5 продуктов для тестирования
    }
    
    print(f"URL запроса: {url}")
    print(f"Параметры: {params}")
    print()
    
    try:
        print("Выполняем GET запрос...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Запрос выполнен успешно!")
            try:
                data = response.json()
                print("Краткая информация о ответе:")
                if 'products' in data:
                    print(f"Количество продуктов: {len(data['products'])}")
                    if data['products']:
                        first_product = data['products'][0]
                        print(f"Первый продукт: {first_product.get('productCode', 'N/A')}")
                        print(f"Название: {first_product.get('title', 'N/A')}")
                print("\nПолный ответ:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Ответ не является валидным JSON:")
                print(response.text)
        else:
            print(f"❌ Ошибка запроса: {response.status_code}")
            print("Содержимое ответа:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    # Тестируем оба эндпоинта
    response1 = test_product_endpoint()
    test_modified_since_endpoint()
    
    print("\n" + "="*50)
    print("=== Заключение ===")
    print("Тестирование завершено. Проверьте результаты выше.")

