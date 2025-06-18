#!/usr/bin/env python3
"""
Тестовый скрипт для Google Hotels API (Travel Partner API)
Демонстрирует структуру запроса к accounts.priceViews.get
"""

import requests
import json
from datetime import datetime

# Константы API
BASE_URL = "https://travelpartner.googleapis.com"
API_VERSION = "v3"

def test_google_hotels_api():
    """
    Тестовый запрос к Google Hotels API
    Примечание: Для реального использования требуется OAuth 2.0 токен
    """
    
    # Примерные параметры (в реальном использовании должны быть настоящие)
    account_id = "123456789"  # Пример account ID
    partner_hotel_id = "hotel_example_123"  # Пример partner hotel ID
    
    # Формирование URL запроса
    resource_name = f"accounts/{account_id}/priceViews/{partner_hotel_id}"
    url = f"{BASE_URL}/{API_VERSION}/{resource_name}"
    
    print("=== Тестовый запрос к Google Hotels API ===")
    print(f"URL: {url}")
    print(f"Метод: GET")
    print(f"Требуемый OAuth scope: https://www.googleapis.com/auth/travelpartner")
    print()
    
    # Заголовки запроса (без реального токена)
    headers = {
        "Authorization": "Bearer YOUR_OAUTH_TOKEN_HERE",
        "Content-Type": "application/json"
    }
    
    print("Заголовки запроса:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    print()
    
    # Попытка выполнить запрос (ожидается ошибка аутентификации)
    try:
        print("Выполнение запроса...")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        print()
        
        # Попытка парсинга JSON ответа
        try:
            response_data = response.json()
            print("Тело ответа (JSON):")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Тело ответа (текст):")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    
    print()
    print("=== Ожидаемая структура успешного ответа ===")
    
    # Пример ожидаемой структуры ответа
    expected_response = {
        "name": f"accounts/{account_id}/priceViews/{partner_hotel_id}",
        "perItineraryPrices": [
            {
                "checkinDate": {
                    "year": 2025,
                    "month": 7,
                    "day": 15
                },
                "lengthOfStayDays": 2,
                "price": 150.00,
                "taxes": 15.00,
                "fees": 5.00,
                "currencyCode": "USD",
                "updateTime": "2025-06-18T13:00:00Z"
            },
            {
                "checkinDate": {
                    "year": 2025,
                    "month": 7,
                    "day": 16
                },
                "lengthOfStayDays": 3,
                "price": 225.00,
                "taxes": 22.50,
                "fees": 7.50,
                "currencyCode": "USD",
                "updateTime": "2025-06-18T13:00:00Z"
            }
        ]
    }
    
    print(json.dumps(expected_response, indent=2, ensure_ascii=False))

def demonstrate_oauth_flow():
    """
    Демонстрация процесса OAuth 2.0 для Google Hotels API
    """
    print("\n=== Процесс OAuth 2.0 аутентификации ===")
    print("1. Регистрация приложения в Google Cloud Console")
    print("2. Получение client_id и client_secret")
    print("3. Настройка redirect_uri")
    print("4. Запрос authorization code:")
    
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        "client_id=YOUR_CLIENT_ID&"
        "redirect_uri=YOUR_REDIRECT_URI&"
        "scope=https://www.googleapis.com/auth/travelpartner&"
        "response_type=code&"
        "access_type=offline"
    )
    print(f"   {auth_url}")
    
    print("5. Обмен authorization code на access_token:")
    token_request = {
        "url": "https://oauth2.googleapis.com/token",
        "method": "POST",
        "data": {
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET",
            "code": "AUTHORIZATION_CODE",
            "grant_type": "authorization_code",
            "redirect_uri": "YOUR_REDIRECT_URI"
        }
    }
    print(f"   {json.dumps(token_request, indent=2)}")
    
    print("6. Использование access_token в заголовке Authorization")

if __name__ == "__main__":
    test_google_hotels_api()
    demonstrate_oauth_flow()
    
    print("\n=== Заключение ===")
    print("Для успешного использования Google Hotels API необходимо:")
    print("1. Зарегистрировать приложение в Google Cloud Console")
    print("2. Получить доступ к Travel Partner API")
    print("3. Настроить OAuth 2.0 аутентификацию")
    print("4. Получить реальные account_id и partner_hotel_id")
    print("5. Использовать действительный access_token в запросах")

