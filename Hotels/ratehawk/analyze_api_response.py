#!/usr/bin/env python3
"""
Анализ ответа API RateHawk на основе полученных данных
"""

import json

def analyze_api_response():
    """
    Анализ ответа API, полученного при тестировании
    """
    
    # Реальный ответ, полученный от API
    actual_response = {
        "data": None,
        "debug": {
            "request": {
                "checkin": "2025-10-22",
                "checkout": "2025-10-25",
                "residency": "gb",
                "language": "en",
                "guests": [
                    {
                        "adults": 2,
                        "children": []
                    }
                ],
                "longitude": 13.38886,
                "latitude": 52.517036,
                "radius": 150,
                "currency": "EUR"
            },
            "key_id": 0,
            "validation_error": None
        },
        "status": "error",
        "error": "no_auth_header"
    }
    
    # Заголовки ответа
    response_headers = {
        "Date": "Wed, 18 Jun 2025 13:15:11 GMT",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "302",
        "Connection": "keep-alive",
        "version": "b799663",
        "www-authenticate": "Basic realm=\"Restricted\"",
        "x-partner-application-time": "0.00",
        "x-partner-error-slug": "no_auth_header",
        "request-id": "f3ec77d52f8666fb30df3c0c9b68dc81, 5c14beb4fc80f0c9f141f04c578bea3f",
        "cf-cache-status": "DYNAMIC",
        "Server": "cloudflare",
        "CF-RAY": "951b0dd24d2205f6-IAD"
    }
    
    print("=== АНАЛИЗ ОТВЕТА API RATEHAWK ===\n")
    
    print("1. СТАТУС ОТВЕТА:")
    print("   - HTTP Status: 401 Unauthorized")
    print("   - Причина: Отсутствует заголовок авторизации")
    print("   - Ошибка: no_auth_header")
    
    print("\n2. СТРУКТУРА ОТВЕТА:")
    print("   - data: null (данные отсутствуют из-за ошибки авторизации)")
    print("   - status: 'error'")
    print("   - error: 'no_auth_header'")
    print("   - debug: содержит отладочную информацию")
    
    print("\n3. ОТЛАДОЧНАЯ ИНФОРМАЦИЯ:")
    print("   - Запрос был корректно распарсен сервером")
    print("   - Все параметры запроса сохранены в debug.request")
    print("   - key_id: 0 (указывает на отсутствие аутентификации)")
    print("   - validation_error: null (ошибок валидации нет)")
    
    print("\n4. ЗАГОЛОВКИ ОТВЕТА:")
    print("   - www-authenticate: Basic realm=\"Restricted\" - требуется Basic Auth")
    print("   - x-partner-application-time: 0.00 - время обработки запроса")
    print("   - x-partner-error-slug: no_auth_header - код ошибки")
    print("   - request-id: уникальный идентификатор запроса для отладки")
    print("   - version: b799663 - версия API")
    
    print("\n5. ВЫВОДЫ:")
    print("   ✓ API работает и доступен")
    print("   ✓ Endpoint корректный")
    print("   ✓ Формат запроса правильный")
    print("   ✓ Сервер корректно обрабатывает JSON")
    print("   ✗ Требуется аутентификация для получения данных")
    
    print("\n6. СЛЕДУЮЩИЕ ШАГИ:")
    print("   - Получить API ключ через регистрацию")
    print("   - Добавить HTTP Basic Authentication")
    print("   - Повторить запрос с корректными учетными данными")
    
    return actual_response, response_headers

def demonstrate_correct_request():
    """
    Демонстрация корректного запроса с аутентификацией
    """
    print("\n=== ПРИМЕР КОРРЕКТНОГО ЗАПРОСА ===\n")
    
    correct_request = """
curl --user 'YOUR_KEY_ID:YOUR_API_KEY' \\
     'https://api.worldota.net/api/b2b/v3/search/serp/geo/' \\
     --header 'Content-Type: application/json' \\
     --data '{
       "checkin": "2025-10-22",
       "checkout": "2025-10-25",
       "residency": "gb",
       "language": "en",
       "guests": [
         {
           "adults": 2,
           "children": []
         }
       ],
       "longitude": 13.38886,
       "latitude": 52.517036,
       "radius": 150,
       "currency": "EUR"
     }'
"""
    
    print("Команда curl с аутентификацией:")
    print(correct_request)
    
    print("\nПример в Python:")
    python_example = '''
import requests
from requests.auth import HTTPBasicAuth

url = "https://api.worldota.net/api/b2b/v3/search/serp/geo/"
auth = HTTPBasicAuth('YOUR_KEY_ID', 'YOUR_API_KEY')
headers = {"Content-Type": "application/json"}
data = {
    "checkin": "2025-10-22",
    "checkout": "2025-10-25",
    "residency": "gb",
    "language": "en",
    "guests": [{"adults": 2, "children": []}],
    "longitude": 13.38886,
    "latitude": 52.517036,
    "radius": 150,
    "currency": "EUR"
}

response = requests.post(url, auth=auth, headers=headers, json=data)
print(response.json())
'''
    print(python_example)

if __name__ == "__main__":
    analyze_api_response()
    demonstrate_correct_request()

