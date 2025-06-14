#!/usr/bin/env python3
"""
Тестовый скрипт для работы с API SevenRooms
"""

import requests
import json
from datetime import datetime, timedelta

# Конфигурация API (используем demo URL)
API_CONFIG = {
    "base_url": "https://demo.sevenrooms.com/api-ext/2_2",
    "client_id": "demo_client",  # Тестовые данные
    "client_secret": "demo_secret",  # Тестовые данные
    "venue_group_id": "demo_venue",  # Тестовые данные
    "start_date": "2024-01-01T00:00:00Z"
}

def test_sevenrooms_api():
    """
    Выполняет тестовые запросы к API SevenRooms
    """
    print("=== Тестирование API SevenRooms ===\n")
    
    # 1. Тест доступности API
    print("1. Проверка доступности API...")
    try:
        response = requests.get(API_CONFIG["base_url"], timeout=10)
        print(f"   Статус ответа: {response.status_code}")
        print(f"   Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            print(f"   Содержимое ответа: {response.text[:500]}...")
        else:
            print("   Ответ пустой")
            
    except requests.exceptions.RequestException as e:
        print(f"   Ошибка при подключении: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Тест аутентификации
    print("2. Попытка аутентификации...")
    auth_url = f"{API_CONFIG['base_url']}/auth"
    auth_data = {
        "client_id": API_CONFIG["client_id"],
        "client_secret": API_CONFIG["client_secret"]
    }
    
    try:
        response = requests.post(auth_url, json=auth_data, timeout=10)
        print(f"   Статус ответа: {response.status_code}")
        print(f"   Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            print(f"   Содержимое ответа: {response.text[:500]}...")
        else:
            print("   Ответ пустой")
            
    except requests.exceptions.RequestException as e:
        print(f"   Ошибка при аутентификации: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Тест получения резерваций
    print("3. Попытка получения резерваций...")
    reservations_url = f"{API_CONFIG['base_url']}/reservations"
    params = {
        "venue_group_id": API_CONFIG["venue_group_id"],
        "start_date": API_CONFIG["start_date"]
    }
    
    try:
        response = requests.get(reservations_url, params=params, timeout=10)
        print(f"   Статус ответа: {response.status_code}")
        print(f"   Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            print(f"   Содержимое ответа: {response.text[:500]}...")
        else:
            print("   Ответ пустой")
            
    except requests.exceptions.RequestException as e:
        print(f"   Ошибка при получении резерваций: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. Тест различных эндпоинтов
    print("4. Тестирование различных эндпоинтов...")
    
    endpoints_to_test = [
        "/venues",
        "/guests", 
        "/tables",
        "/availability",
        "/api/v1/reservations",  # Альтернативная версия API
        "/health",  # Проверка здоровья сервиса
        "/status"   # Статус сервиса
    ]
    
    for endpoint in endpoints_to_test:
        print(f"   Тестирование {endpoint}...")
        try:
            url = API_CONFIG["base_url"] + endpoint
            response = requests.get(url, timeout=5)
            print(f"     Статус: {response.status_code}")
            
            if response.status_code == 200 and response.text:
                print(f"     Ответ: {response.text[:100]}...")
            elif response.status_code != 200:
                print(f"     Ошибка: {response.text[:100] if response.text else 'Нет содержимого'}")
                
        except requests.exceptions.RequestException as e:
            print(f"     Ошибка подключения: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. Анализ структуры API
    print("5. Анализ структуры API...")
    
    # Попробуем найти документацию API
    doc_endpoints = [
        "/docs",
        "/swagger", 
        "/api-docs",
        "/openapi.json",
        "/swagger.json"
    ]
    
    for endpoint in doc_endpoints:
        print(f"   Проверка документации: {endpoint}...")
        try:
            url = API_CONFIG["base_url"] + endpoint
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"     Найдена документация! Статус: {response.status_code}")
                print(f"     Содержимое: {response.text[:200]}...")
            else:
                print(f"     Не найдена (статус: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"     Ошибка: {e}")

def analyze_api_response(response):
    """
    Анализирует ответ API и извлекает полезную информацию
    """
    analysis = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content_type": response.headers.get("content-type", "unknown"),
        "content_length": len(response.content),
        "response_time": response.elapsed.total_seconds()
    }
    
    # Попытка парсинга JSON
    try:
        if "application/json" in analysis["content_type"]:
            analysis["json_data"] = response.json()
        else:
            analysis["text_data"] = response.text[:1000]  # Первые 1000 символов
    except:
        analysis["text_data"] = response.text[:1000]
    
    return analysis

if __name__ == "__main__":
    test_sevenrooms_api()
    print("Тестирование завершено!")

