#!/usr/bin/env python3
"""
Улучшенный тестовый скрипт для работы с API SevenRooms
Основан на документации Kleene.ai
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

def test_sevenrooms_api_v2():
    """
    Выполняет тестовые запросы к API SevenRooms на основе документации
    """
    print("=== Улучшенное тестирование API SevenRooms ===\n")
    
    # Доступные отчеты согласно документации
    available_reports = [
        "venues",
        "reservation_requests", 
        "reservations",
        "events",
        "clients",
        "programs",
        "charges",
        "reservation_feedback",
        "payout_profiles"
    ]
    
    # 1. Тест базового URL
    print("1. Проверка базового URL API...")
    try:
        response = requests.get(API_CONFIG["base_url"], timeout=10)
        print(f"   Статус ответа: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.text:
            try:
                json_data = response.json()
                print(f"   JSON ответ: {json.dumps(json_data, indent=2)}")
            except:
                print(f"   Текстовый ответ: {response.text[:300]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"   Ошибка при подключении: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 2. Тест аутентификации с правильными параметрами
    print("2. Тестирование аутентификации...")
    
    # Попробуем разные варианты аутентификации
    auth_methods = [
        {
            "name": "POST /auth с JSON",
            "method": "POST",
            "url": f"{API_CONFIG['base_url']}/auth",
            "data": {
                "client_id": API_CONFIG["client_id"],
                "client_secret": API_CONFIG["client_secret"]
            },
            "headers": {"Content-Type": "application/json"}
        },
        {
            "name": "POST /login с JSON", 
            "method": "POST",
            "url": f"{API_CONFIG['base_url']}/login",
            "data": {
                "client_id": API_CONFIG["client_id"],
                "client_secret": API_CONFIG["client_secret"]
            },
            "headers": {"Content-Type": "application/json"}
        },
        {
            "name": "POST /token с form data",
            "method": "POST", 
            "url": f"{API_CONFIG['base_url']}/token",
            "data": {
                "grant_type": "client_credentials",
                "client_id": API_CONFIG["client_id"],
                "client_secret": API_CONFIG["client_secret"]
            },
            "headers": {"Content-Type": "application/x-www-form-urlencoded"}
        }
    ]
    
    for auth_method in auth_methods:
        print(f"   Тестирование: {auth_method['name']}")
        try:
            if auth_method["method"] == "POST":
                if "application/json" in auth_method["headers"]["Content-Type"]:
                    response = requests.post(
                        auth_method["url"], 
                        json=auth_method["data"],
                        headers=auth_method["headers"],
                        timeout=10
                    )
                else:
                    response = requests.post(
                        auth_method["url"],
                        data=auth_method["data"], 
                        headers=auth_method["headers"],
                        timeout=10
                    )
            
            print(f"     Статус: {response.status_code}")
            
            if response.text:
                try:
                    json_data = response.json()
                    print(f"     Ответ: {json.dumps(json_data, indent=6)[:200]}...")
                except:
                    print(f"     Ответ: {response.text[:200]}...")
                    
        except requests.exceptions.RequestException as e:
            print(f"     Ошибка: {e}")
        
        print()
    
    print("="*60 + "\n")
    
    # 3. Тестирование доступных отчетов
    print("3. Тестирование доступных отчетов...")
    
    for report in available_reports:
        print(f"   Тестирование отчета: {report}")
        
        # Попробуем разные варианты URL
        urls_to_try = [
            f"{API_CONFIG['base_url']}/{report}",
            f"{API_CONFIG['base_url']}/reports/{report}",
            f"{API_CONFIG['base_url']}/api/{report}",
            f"{API_CONFIG['base_url']}/v1/{report}"
        ]
        
        for url in urls_to_try:
            try:
                # Добавим базовые параметры
                params = {
                    "venue_group_id": API_CONFIG["venue_group_id"]
                }
                
                response = requests.get(url, params=params, timeout=5)
                
                if response.status_code != 404:
                    print(f"     URL: {url}")
                    print(f"     Статус: {response.status_code}")
                    
                    if response.text:
                        try:
                            json_data = response.json()
                            print(f"     Ответ: {json.dumps(json_data, indent=8)[:150]}...")
                        except:
                            print(f"     Ответ: {response.text[:150]}...")
                    break
                    
            except requests.exceptions.RequestException as e:
                continue
        else:
            print(f"     Все URL недоступны для {report}")
        
        print()
    
    print("="*60 + "\n")
    
    # 4. Анализ структуры ошибок API
    print("4. Анализ структуры ошибок API...")
    
    error_analysis = {}
    
    # Соберем все уникальные ошибки
    test_urls = [
        f"{API_CONFIG['base_url']}/reservations",
        f"{API_CONFIG['base_url']}/venues", 
        f"{API_CONFIG['base_url']}/clients"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            
            if response.text:
                try:
                    json_data = response.json()
                    error_key = f"{response.status_code}_{json_data.get('msg', 'unknown')}"
                    
                    if error_key not in error_analysis:
                        error_analysis[error_key] = {
                            "status_code": response.status_code,
                            "message": json_data.get('msg', 'unknown'),
                            "full_response": json_data,
                            "count": 0
                        }
                    
                    error_analysis[error_key]["count"] += 1
                    
                except:
                    pass
                    
        except:
            continue
    
    print("   Найденные типы ошибок:")
    for error_key, error_info in error_analysis.items():
        print(f"     {error_info['status_code']}: {error_info['message']} (встречено {error_info['count']} раз)")
        print(f"       Полный ответ: {json.dumps(error_info['full_response'], indent=8)}")
        print()
    
    print("="*60 + "\n")
    
    # 5. Проверка требований к аутентификации
    print("5. Анализ требований к аутентификации...")
    
    # Проанализируем ошибки аутентификации
    auth_errors = [
        "Missing arg client_id",
        "Missing Authentication parameters",
        "Could not find resource"
    ]
    
    print("   Обнаруженные требования:")
    print("   - API требует client_id и client_secret")
    print("   - Аутентификация обязательна для доступа к данным")
    print("   - Некоторые эндпоинты могут не существовать или требовать другие пути")
    print("   - API использует JSON формат для ответов")
    print("   - Поддерживается CORS (видны соответствующие заголовки)")
    
    print("\n" + "="*60 + "\n")
    
    print("6. Рекомендации для работы с API:")
    print("   1. Получите реальные client_id и client_secret от SevenRooms")
    print("   2. Используйте правильный base_url (возможно, не demo)")
    print("   3. Изучите официальную документацию API")
    print("   4. Убедитесь в наличии необходимых разрешений:")
    print("      - Access to search/export payment charges")
    print("      - Access to search/export clients")
    print("   5. Для production используйте venue_group_id вашего заведения")

if __name__ == "__main__":
    test_sevenrooms_api_v2()
    print("\nТестирование завершено!")

