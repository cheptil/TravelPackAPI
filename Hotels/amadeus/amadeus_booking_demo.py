#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования Amadeus Hotel Booking API
Этот скрипт показывает структуру запроса для создания бронирования отеля
"""

import requests
import json
from datetime import datetime, timedelta

# Конфигурация API
BASE_URL = "https://test.api.amadeus.com/v2"
BOOKING_ENDPOINT = "/booking/hotel-orders"

# ВНИМАНИЕ: Для реального использования нужно получить API ключи на https://developers.amadeus.com
# Этот пример показывает структуру запроса
API_KEY = "YOUR_API_KEY_HERE"
API_SECRET = "YOUR_API_SECRET_HERE"

def get_access_token(api_key, api_secret):
    """
    Получение access token для авторизации
    В реальном приложении этот токен нужно кэшировать и обновлять при истечении
    """
    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    
    # В демонстрационном режиме возвращаем фиктивный токен
    return "DEMO_ACCESS_TOKEN"

def create_hotel_booking_request():
    """
    Создание структуры запроса для бронирования отеля
    Основано на документации Amadeus Hotel Booking API v2.0
    """
    
    # Пример структуры запроса
    booking_request = {
        "data": {
            "type": "hotel-order",
            "guests": [
                {
                    "tid": 1,
                    "title": "MR",
                    "firstName": "JOHN",
                    "lastName": "DOE",
                    "phone": "+33123456789",
                    "email": "john.doe@example.com"
                }
            ],
            "travelAgent": {
                "contact": {
                    "email": "travel.agent@example.com"
                }
            },
            "roomAssociations": [
                {
                    "guestReferences": [
                        {
                            "guestReference": "1"
                        }
                    ],
                    "hotelOfferId": "HOTEL_OFFER_ID_FROM_SEARCH_API"
                }
            ],
            "payment": {
                "method": "CREDIT_CARD",
                "paymentCard": {
                    "paymentCardInfo": {
                        "vendorCode": "VI",
                        "cardNumber": "4111111111111111",
                        "expiryDate": "2025-12",
                        "holderName": "JOHN DOE"
                    }
                }
            }
        }
    }
    
    return booking_request

def simulate_hotel_booking():
    """
    Симуляция запроса на бронирование отеля
    """
    print("=== Демонстрация Amadeus Hotel Booking API ===\n")
    
    # Получение access token
    print("1. Получение access token...")
    access_token = get_access_token(API_KEY, API_SECRET)
    print(f"   Access token: {access_token[:20]}...\n")
    
    # Подготовка запроса
    print("2. Подготовка запроса на бронирование...")
    booking_data = create_hotel_booking_request()
    
    # Заголовки запроса
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # URL для запроса
    url = BASE_URL + BOOKING_ENDPOINT
    
    print(f"   URL: {url}")
    print(f"   Method: POST")
    print(f"   Headers: {json.dumps(headers, indent=2)}")
    print(f"   Body: {json.dumps(booking_data, indent=2)}\n")
    
    # В демонстрационном режиме не выполняем реальный запрос
    print("3. Выполнение запроса (ДЕМО РЕЖИМ)...")
    print("   ВНИМАНИЕ: Реальный запрос не выполняется, так как требуется валидный API ключ")
    print("   и offer ID из предыдущего поиска отелей.\n")
    
    # Симуляция ответа
    simulated_response = {
        "data": [
            {
                "type": "hotel-order",
                "id": "XD_8138319951754",
                "self": "https://test.api.amadeus.com/v2/booking/hotel-orders/XD_8138319951754",
                "associatedRecords": [
                    {
                        "reference": "C9QHBU",
                        "originSystemCode": "GDS"
                    }
                ],
                "hotelBookings": [
                    {
                        "type": "hotel-booking",
                        "id": "XD_8138319951754_1",
                        "roomAssociations": [
                            {
                                "guestReferences": [
                                    {
                                        "guestReference": "1"
                                    }
                                ],
                                "hotelOfferId": "HOTEL_OFFER_ID_FROM_SEARCH_API"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    print("4. Симулированный ответ API:")
    print(json.dumps(simulated_response, indent=2))
    
    return simulated_response

def analyze_booking_response(response):
    """
    Анализ ответа API бронирования
    """
    print("\n=== Анализ ответа ===")
    
    if "data" in response and len(response["data"]) > 0:
        booking = response["data"][0]
        
        print(f"✅ Бронирование создано успешно!")
        print(f"   ID заказа: {booking.get('id', 'N/A')}")
        print(f"   Тип: {booking.get('type', 'N/A')}")
        print(f"   Ссылка: {booking.get('self', 'N/A')}")
        
        if "associatedRecords" in booking:
            for record in booking["associatedRecords"]:
                print(f"   Референс: {record.get('reference', 'N/A')}")
                print(f"   Система: {record.get('originSystemCode', 'N/A')}")
        
        if "hotelBookings" in booking:
            print(f"   Количество бронирований отелей: {len(booking['hotelBookings'])}")
    else:
        print("❌ Ошибка в ответе API")

if __name__ == "__main__":
    # Выполнение демонстрации
    response = simulate_hotel_booking()
    analyze_booking_response(response)
    
    print("\n=== Дополнительная информация ===")
    print("Для реального использования API:")
    print("1. Зарегистрируйтесь на https://developers.amadeus.com")
    print("2. Получите API ключи (client_id и client_secret)")
    print("3. Сначала используйте Hotel Search API для получения offer ID")
    print("4. Замените 'HOTEL_OFFER_ID_FROM_SEARCH_API' на реальный offer ID")
    print("5. Используйте валидные данные гостя и платежной карты")
    print("6. ВНИМАНИЕ: Не тестируйте на продакшене - используйте только тестовую среду!")

