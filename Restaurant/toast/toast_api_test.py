#!/usr/bin/env python3
"""
Демонстрационный тестовый запрос к Toast API
Этот скрипт показывает, как выполнить запрос аутентификации к Toast API
"""

import requests
import json
from datetime import datetime

def test_toast_api_authentication():
    """
    Выполняет тестовый запрос аутентификации к Toast API
    Использует примерные учетные данные для демонстрации
    """
    
    # URL для аутентификации (production endpoint - для демонстрации)
    # В реальности нужно использовать sandbox URL, предоставленный Toast team
    auth_url = "https://ws-api.toasttab.com/authentication/v1/authentication/login"
    
    # Примерные учетные данные (НЕ РЕАЛЬНЫЕ)
    # В реальности эти данные предоставляются командой Toast integrations
    test_credentials = {
        "clientId": "demo_client_id_12345",
        "clientSecret": "demo_client_secret_67890", 
        "userAccessType": "TOAST_MACHINE_CLIENT"
    }
    
    # Заголовки запроса
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Toast-API-Test-Client/1.0"
    }
    
    print("=== ТЕСТОВЫЙ ЗАПРОС К TOAST API ===")
    print(f"Время запроса: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {auth_url}")
    print(f"Метод: POST")
    print(f"Заголовки: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f"Тело запроса: {json.dumps(test_credentials, indent=2, ensure_ascii=False)}")
    print("\n" + "="*50)
    
    try:
        # Выполняем POST запрос
        print("Выполняю запрос...")
        response = requests.post(
            auth_url,
            json=test_credentials,
            headers=headers,
            timeout=30
        )
        
        print(f"\nСтатус код ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        # Пытаемся получить JSON ответ
        try:
            response_json = response.json()
            print(f"Тело ответа (JSON): {json.dumps(response_json, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            print(f"Тело ответа (текст): {response.text}")
        
        # Анализ результата
        print("\n" + "="*50)
        print("АНАЛИЗ РЕЗУЛЬТАТА:")
        
        if response.status_code == 200:
            print("✅ Успешная аутентификация!")
            print("Получен токен доступа для дальнейших запросов к API")
        elif response.status_code == 401:
            print("❌ Ошибка аутентификации (401 Unauthorized)")
            print("Это ожидаемый результат, так как используются демонстрационные учетные данные")
            print("Для реальной работы нужны учетные данные от команды Toast integrations")
        elif response.status_code == 404:
            print("❌ Endpoint не найден (404 Not Found)")
            print("Возможно, используется неправильный URL или API недоступен")
        else:
            print(f"❓ Неожиданный статус код: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        print("Возможные причины:")
        print("- Нет подключения к интернету")
        print("- Неправильный URL")
        print("- Сервер недоступен")
        
    print("\n" + "="*50)
    return response if 'response' in locals() else None

def demonstrate_successful_flow():
    """
    Демонстрирует, как выглядел бы успешный поток аутентификации
    """
    print("\n=== ДЕМОНСТРАЦИЯ УСПЕШНОГО ПОТОКА ===")
    
    # Пример успешного ответа из документации
    successful_response = {
        "token": {
            "tokenType": "Bearer",
            "scope": "string",
            "expiresIn": 86400,
            "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        },
        "status": "SUCCESS"
    }
    
    print("При успешной аутентификации API вернул бы:")
    print(json.dumps(successful_response, indent=2, ensure_ascii=False))
    
    print("\nДалее этот токен можно использовать для запросов к другим API:")
    print("Authorization: Bearer <accessToken>")
    
    # Пример запроса к другому API с токеном
    print("\nПример запроса к Configuration API:")
    example_config_request = {
        "url": "https://ws-api.toasttab.com/config/v1/restaurants/{restaurantGuid}",
        "method": "GET",
        "headers": {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "Toast-Restaurant-External-ID": "{restaurantGuid}"
        }
    }
    print(json.dumps(example_config_request, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    # Выполняем тестовый запрос
    response = test_toast_api_authentication()
    
    # Демонстрируем успешный поток
    demonstrate_successful_flow()
    
    print("\n=== ЗАКЛЮЧЕНИЕ ===")
    print("Для полноценной работы с Toast API необходимо:")
    print("1. Подать заявку на партнерство с Toast")
    print("2. Пройти процесс одобрения и подписания соглашения")
    print("3. Получить учетные данные для sandbox окружения")
    print("4. Разработать и протестировать интеграцию")
    print("5. Пройти сертификацию для доступа к production окружению")

