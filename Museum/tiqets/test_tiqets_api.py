#!/usr/bin/env python3
"""
Тестовый скрипт для API Tiqets Distributor API
"""

import requests
import json
from datetime import datetime

# Конфигурация
TEST_BASE_URL = "https://api-tiqt-test.steq.it/v2"
PROD_BASE_URL = "https://api.tiqets.com/v2"

# Используем тестовую среду
BASE_URL = TEST_BASE_URL

def test_products_endpoint_without_auth():
    """
    Тестирование эндпоинта /products без аутентификации
    Ожидаем получить ошибку 401 Unauthorized
    """
    print("=== Тест 1: Запрос /products без аутентификации ===")
    
    url = f"{BASE_URL}/products"
    headers = {
        'User-Agent': 'Tiqets-API-Test-Client/1.0',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.text:
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Raw Response: {response.text}")
        else:
            print("Empty response body")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print()

def test_products_endpoint_with_fake_auth():
    """
    Тестирование эндпоинта /products с поддельной аутентификацией
    Ожидаем получить ошибку 401 или 403
    """
    print("=== Тест 2: Запрос /products с поддельной аутентификацией ===")
    
    url = f"{BASE_URL}/products"
    headers = {
        'User-Agent': 'Tiqets-API-Test-Client/1.0',
        'Accept': 'application/json',
        'Authorization': 'Token fake-api-key-for-testing'
    }
    
    # Добавляем параметры для тестирования
    params = {
        'city_name': 'Amsterdam',
        'language': 'en',
        'currency': 'EUR'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"URL: {url}")
        print(f"Parameters: {params}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.text:
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Raw Response: {response.text}")
        else:
            print("Empty response body")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print()

def test_single_product_endpoint():
    """
    Тестирование эндпоинта для получения одного продукта
    Используем тестовый Product ID 1006356
    """
    print("=== Тест 3: Запрос информации о тестовом продукте ===")
    
    product_id = 1006356  # Тестовый продукт "The Museum of Cognitive Dissonance"
    url = f"{BASE_URL}/products/{product_id}"
    headers = {
        'User-Agent': 'Tiqets-API-Test-Client/1.0',
        'Accept': 'application/json',
        'Authorization': 'Token fake-api-key-for-testing'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.text:
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Raw Response: {response.text}")
        else:
            print("Empty response body")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print()

def test_api_connectivity():
    """
    Базовый тест соединения с API
    """
    print("=== Тест 4: Проверка соединения с API ===")
    
    # Попробуем различные эндпоинты
    endpoints_to_test = [
        "/",
        "/health",
        "/status", 
        "/version",
        "/products"
    ]
    
    for endpoint in endpoints_to_test:
        url = f"{BASE_URL}{endpoint}"
        headers = {
            'User-Agent': 'Tiqets-API-Test-Client/1.0',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            print(f"Endpoint: {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 200 and response.text:
                try:
                    json_response = response.json()
                    print(f"  Response: {json.dumps(json_response, indent=2, ensure_ascii=False)[:200]}...")
                except json.JSONDecodeError:
                    print(f"  Raw Response: {response.text[:200]}...")
                    
        except requests.exceptions.RequestException as e:
            print(f"Endpoint: {endpoint} - Error: {e}")
    
    print()

if __name__ == "__main__":
    print(f"Тестирование Tiqets Distributor API")
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Базовый URL: {BASE_URL}")
    print("=" * 60)
    print()
    
    # Выполняем тесты
    test_api_connectivity()
    test_products_endpoint_without_auth()
    test_products_endpoint_with_fake_auth()
    test_single_product_endpoint()
    
    print("=" * 60)
    print("Тестирование завершено")

