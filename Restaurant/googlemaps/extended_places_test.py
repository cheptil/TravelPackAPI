#!/usr/bin/env python3
"""
Расширенный тест Google Places API (New)
Демонстрирует различные типы запросов и анализирует ответы
"""

import requests
import json

def test_different_search_types():
    """
    Тестирует различные типы поисковых запросов
    """
    
    base_url = "https://places.googleapis.com/v1/places:searchText"
    
    # Различные примеры запросов
    test_cases = [
        {
            "name": "Поиск ресторанов",
            "body": {
                "textQuery": "pizza restaurants in New York",
                "languageCode": "en",
                "regionCode": "US",
                "maxResultCount": 3
            },
            "fieldMask": "places.displayName,places.formattedAddress,places.rating"
        },
        {
            "name": "Поиск по адресу",
            "body": {
                "textQuery": "123 Main Street, New York",
                "languageCode": "en",
                "regionCode": "US"
            },
            "fieldMask": "places.displayName,places.formattedAddress,places.location"
        },
        {
            "name": "Поиск по номеру телефона",
            "body": {
                "textQuery": "+1 212-555-0123",
                "regionCode": "US"
            },
            "fieldMask": "places.displayName,places.formattedAddress,places.internationalPhoneNumber"
        },
        {
            "name": "Поиск с фильтрами",
            "body": {
                "textQuery": "coffee shops",
                "languageCode": "en",
                "regionCode": "US",
                "maxResultCount": 5,
                "openNow": True,
                "minRating": 4.0
            },
            "fieldMask": "places.displayName,places.rating,places.currentOpeningHours"
        }
    ]
    
    print("=== Тестирование различных типов запросов Places API ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}")
        print("-" * 50)
        
        headers = {
            "Content-Type": "application/json",
            "X-Goog-FieldMask": test_case['fieldMask']
            # Для реального использования добавить:
            # "X-Goog-Api-Key": "YOUR_API_KEY"
        }
        
        print(f"Request Body: {json.dumps(test_case['body'], indent=2)}")
        print(f"Field Mask: {test_case['fieldMask']}")
        
        try:
            response = requests.post(base_url, headers=headers, json=test_case['body'], timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 403:
                error_data = response.json()
                print(f"Expected Error: {error_data['error']['message']}")
            else:
                print(f"Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n")

def demonstrate_field_masks():
    """
    Демонстрирует различные варианты Field Mask
    """
    
    print("=== Примеры Field Mask для различных уровней тарификации ===\n")
    
    field_mask_examples = {
        "Text Search Essentials ID Only SKU": [
            "places.attributions",
            "places.id", 
            "places.name",
            "nextPageToken"
        ],
        "Text Search Pro SKU": [
            "places.displayName",
            "places.formattedAddress", 
            "places.location",
            "places.photos",
            "places.rating",
            "places.types",
            "places.viewport"
        ],
        "Text Search Enterprise SKU": [
            "places.currentOpeningHours",
            "places.internationalPhoneNumber",
            "places.priceLevel",
            "places.rating",
            "places.websiteUri"
        ],
        "Text Search Enterprise + Atmosphere SKU": [
            "places.allowsDogs",
            "places.goodForChildren",
            "places.restroom",
            "places.accessibilityOptions"
        ]
    }
    
    for sku_name, fields in field_mask_examples.items():
        print(f"{sku_name}:")
        field_mask = ",".join(fields)
        print(f"  Field Mask: {field_mask}")
        print(f"  Поля: {', '.join(fields)}")
        print()

def create_sample_responses():
    """
    Создает примеры ожидаемых ответов API
    """
    
    print("=== Примеры ожидаемых ответов от API ===\n")
    
    sample_success_response = {
        "places": [
            {
                "id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
                "displayName": {
                    "text": "Joe's Pizza",
                    "languageCode": "en"
                },
                "formattedAddress": "123 Broadway, New York, NY 10001, USA",
                "location": {
                    "latitude": 40.7589,
                    "longitude": -73.9851
                },
                "rating": 4.2,
                "priceLevel": "PRICE_LEVEL_INEXPENSIVE"
            },
            {
                "id": "ChIJrTLr-GyuEmsRBfy61i59si0",
                "displayName": {
                    "text": "Tony's Pizzeria",
                    "languageCode": "en"
                },
                "formattedAddress": "456 5th Ave, New York, NY 10018, USA",
                "location": {
                    "latitude": 40.7505,
                    "longitude": -73.9934
                },
                "rating": 4.5,
                "priceLevel": "PRICE_LEVEL_MODERATE"
            }
        ]
    }
    
    print("Пример успешного ответа:")
    print(json.dumps(sample_success_response, indent=2, ensure_ascii=False))
    print()
    
    sample_error_response = {
        "error": {
            "code": 400,
            "message": "Field mask is required. Please specify the fields to return.",
            "status": "INVALID_ARGUMENT"
        }
    }
    
    print("Пример ответа с ошибкой:")
    print(json.dumps(sample_error_response, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_different_search_types()
    demonstrate_field_masks()
    create_sample_responses()

