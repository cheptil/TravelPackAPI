#!/usr/bin/env python3
"""
Демонстрационный скрипт для API Avis
Показывает правильную структуру запросов и обработку ответов
"""

import requests
import json
from datetime import datetime

def demonstrate_api_structure():
    """
    Демонстрация правильной структуры запросов к API Avis
    """
    print("📋 Демонстрация структуры API Avis")
    print("=" * 50)
    
    # 1. Структура запроса для получения токена
    print("\n🔑 1. Получение Access Token")
    print("Endpoint: GET https://stage.abgapiservices.com/oauth/token/v1")
    print("Заголовки:")
    print("  client_id: [ваш_client_id]")
    print("  client_secret: [ваш_client_secret]")
    
    token_example = {
        "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJwem5vRHdsYlNUcmFwM2FTQzdSUUl3anpzb2NJWGlaTUQ2cUxBakh5X0NVIn0...",
        "token_type": "Bearer",
        "expires_in": 7140
    }
    
    print("\nПример успешного ответа:")
    print(json.dumps(token_example, indent=2, ensure_ascii=False))
    
    # 2. Структура запроса к Car Locations API
    print("\n🚗 2. Car Locations API")
    print("Endpoint: GET https://stage.abgapiservices.com/cars/locations/v1/")
    print("Заголовки:")
    print("  client_id: [ваш_client_id]")
    print("  Authorization: Bearer [access_token]")
    print("Параметры запроса:")
    print("  country_code: US")
    print("  brand: Avis")
    print("  keyword: Denver")
    
    # Пример ожидаемого ответа (на основе документации)
    locations_example = {
        "status": {
            "request_time": datetime.now().isoformat() + "Z",
            "request_errors": 0
        },
        "locations": [
            {
                "location_code": "DENB01",
                "name": "Denver International Airport",
                "address": {
                    "street": "24890 E 78th Ave",
                    "city": "Denver",
                    "state": "CO",
                    "postal_code": "80249",
                    "country": "US"
                },
                "coordinates": {
                    "latitude": 39.8561,
                    "longitude": -104.6737
                },
                "operating_hours": {
                    "monday": "05:00-23:59",
                    "tuesday": "05:00-23:59",
                    "wednesday": "05:00-23:59",
                    "thursday": "05:00-23:59",
                    "friday": "05:00-23:59",
                    "saturday": "05:00-23:59",
                    "sunday": "05:00-23:59"
                },
                "brand": "Avis",
                "phone": "+1-800-331-1212"
            },
            {
                "location_code": "DENC02",
                "name": "Denver Downtown",
                "address": {
                    "street": "1900 Broadway",
                    "city": "Denver",
                    "state": "CO",
                    "postal_code": "80202",
                    "country": "US"
                },
                "coordinates": {
                    "latitude": 39.7392,
                    "longitude": -104.9903
                },
                "operating_hours": {
                    "monday": "07:00-18:00",
                    "tuesday": "07:00-18:00",
                    "wednesday": "07:00-18:00",
                    "thursday": "07:00-18:00",
                    "friday": "07:00-18:00",
                    "saturday": "08:00-17:00",
                    "sunday": "10:00-16:00"
                },
                "brand": "Avis",
                "phone": "+1-800-331-1212"
            }
        ]
    }
    
    print("\nПример ожидаемого ответа:")
    print(json.dumps(locations_example, indent=2, ensure_ascii=False))
    
    # Сохраняем пример в файл
    with open('/home/ubuntu/api_structure_example.json', 'w', encoding='utf-8') as f:
        json.dump({
            "token_response": token_example,
            "locations_response": locations_example
        }, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Примеры структуры сохранены в api_structure_example.json")

def analyze_error_responses():
    """
    Анализ полученных ошибок
    """
    print("\n❌ Анализ ошибок API")
    print("=" * 30)
    
    # Ошибка аутентификации
    auth_error = {
        "status": {
            "request_time": "2025-06-14T14:52:22Z",
            "request_errors": 1,
            "errors": [
                {
                    "code": "401",
                    "message": "Unauthorized",
                    "reason": "unauthorized_client",
                    "details": "INVALID_CREDENTIALS: Invalid client credentials"
                }
            ]
        }
    }
    
    print("🔐 Ошибка аутентификации (401):")
    print(json.dumps(auth_error, indent=2, ensure_ascii=False))
    
    # Ошибка отсутствия токена
    token_missing_error = {
        "error": "invalid_request",
        "description": "The required parameter access token is missing."
    }
    
    print("\n🎫 Ошибка отсутствия токена (400):")
    print(json.dumps(token_missing_error, indent=2, ensure_ascii=False))
    
    # Ошибка отсутствия заголовков
    headers_missing_error = {
        "status": {
            "request_time": "2025-06-14T14:52:51Z",
            "request_errors": 2,
            "errors": [
                {
                    "code": "400",
                    "message": "Bad Request",
                    "reason": "validation.request.parameter.header.missing",
                    "details": "Header parameter 'client_id' is required on path '/v1' but not found in request."
                },
                {
                    "code": "400",
                    "message": "Bad Request",
                    "reason": "validation.request.parameter.header.missing",
                    "details": "Header parameter 'client_secret' is required on path '/v1' but not found in request."
                }
            ]
        }
    }
    
    print("\n📋 Ошибка отсутствия заголовков (400):")
    print(json.dumps(headers_missing_error, indent=2, ensure_ascii=False))

def create_test_summary():
    """
    Создание сводки тестирования
    """
    print("\n📊 Сводка тестирования API")
    print("=" * 40)
    
    summary = {
        "api_base_url": "https://stage.abgapiservices.com",
        "authentication": {
            "method": "OAuth 2.0",
            "token_endpoint": "/oauth/token/v1",
            "required_headers": ["client_id", "client_secret"],
            "token_lifetime": "7140 seconds (~2 hours)"
        },
        "tested_endpoints": {
            "/cars/locations/v1/": {
                "status": "requires_authentication",
                "method": "GET",
                "description": "Поиск локаций проката автомобилей"
            },
            "/cars/availability/v1/": {
                "status": "requires_authentication", 
                "method": "GET",
                "description": "Информация о доступности автомобилей"
            },
            "/cars/reservation/v1/": {
                "status": "requires_authentication",
                "method": "POST/GET/PUT/DELETE",
                "description": "Управление бронированиями"
            },
            "/cars/terms_and_conditions/v1/": {
                "status": "requires_authentication",
                "method": "GET", 
                "description": "Условия и положения"
            }
        },
        "error_handling": {
            "401": "Недействительные учетные данные",
            "400": "Отсутствуют обязательные параметры или заголовки"
        },
        "response_format": "JSON",
        "test_results": {
            "api_structure": "✅ Подтверждена",
            "authentication_required": "✅ Подтверждено",
            "error_responses": "✅ Структурированы",
            "endpoints_accessible": "❌ Требуют валидные учетные данные"
        }
    }
    
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    # Сохраняем сводку
    with open('/home/ubuntu/api_test_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Сводка сохранена в api_test_summary.json")

def main():
    """
    Основная функция
    """
    print("🧪 Демонстрация и анализ API Avis")
    print("=" * 60)
    
    # Демонстрируем структуру API
    demonstrate_api_structure()
    
    # Анализируем ошибки
    analyze_error_responses()
    
    # Создаем сводку
    create_test_summary()
    
    print("\n" + "=" * 60)
    print("✅ Демонстрация завершена")

if __name__ == "__main__":
    main()

