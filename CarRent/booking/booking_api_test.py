#!/usr/bin/env python3
"""
Тестовый скрипт для Booking.com Demand API
Демонстрирует структуру запроса к API поиска размещений
"""

import requests
import json
from datetime import datetime, timedelta

def test_booking_api():
    """
    Тестовый запрос к Booking.com Demand API для поиска размещений
    """
    
    # URL API
    api_url = "https://demandapi.booking.com/3.1/accommodations/search"
    
    # Заголовки запроса
    headers = {
        "Authorization": "Bearer YOUR_API_TOKEN_HERE",  # Требуется реальный токен
        "Content-Type": "application/json",
        "X-Affiliate-Id": "0"  # Требуется реальный ID партнера
    }
    
    # Подготовка дат (заезд через неделю, выезд через 10 дней)
    checkin_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    checkout_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    
    # Тело запроса
    request_body = {
        "booker": {
            "country": "nl",  # Нидерланды
            "platform": "desktop"
        },
        "checkin": checkin_date,
        "checkout": checkout_date,
        "city": -2146479,  # ID города (пример)
        "extras": [
            "extra_charges",
            "products"
        ],
        "guests": {
            "number_of_adults": 2,
            "number_of_rooms": 1
        },
        "currency": "EUR",
        "rows": 10  # Ограничиваем количество результатов
    }
    
    print("=== Тестовый запрос к Booking.com Demand API ===")
    print(f"URL: {api_url}")
    print(f"Заголовки: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f"Тело запроса: {json.dumps(request_body, indent=2, ensure_ascii=False)}")
    print()
    
    try:
        # Выполнение запроса
        print("Выполняю запрос...")
        response = requests.post(
            api_url,
            headers=headers,
            json=request_body,
            timeout=30
        )
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        # Попытка парсинга JSON ответа
        try:
            response_data = response.json()
            print(f"Тело ответа: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            print(f"Тело ответа (текст): {response.text}")
            
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

def analyze_response(response):
    """
    Анализ ответа API
    """
    if response is None:
        print("Нет ответа для анализа")
        return
        
    print("\n=== Анализ ответа ===")
    
    if response.status_code == 200:
        print("✅ Успешный запрос!")
        try:
            data = response.json()
            print(f"Получено размещений: {len(data.get('data', []))}")
            if 'request_id' in data:
                print(f"ID запроса: {data['request_id']}")
            if 'next_page' in data:
                print(f"Следующая страница: {data['next_page']}")
        except:
            print("Не удалось разобрать JSON ответ")
            
    elif response.status_code == 401:
        print("❌ Ошибка аутентификации (401)")
        print("Требуется действительный Bearer токен")
        
    elif response.status_code == 403:
        print("❌ Доступ запрещен (403)")
        print("Возможно, неверный X-Affiliate-Id или нет доступа к API")
        
    elif response.status_code == 400:
        print("❌ Неверный запрос (400)")
        print("Проверьте параметры запроса")
        
    else:
        print(f"❌ Неожиданный статус: {response.status_code}")

if __name__ == "__main__":
    # Выполнение тестового запроса
    response = test_booking_api()
    
    # Анализ результата
    analyze_response(response)
    
    print("\n=== Заключение ===")
    print("Для реального использования API требуется:")
    print("1. Регистрация в программе партнеров Booking.com")
    print("2. Получение API токена (Bearer token)")
    print("3. Получение Affiliate ID")
    print("4. Доступ к пилотной программе (API находится в раннем доступе)")

