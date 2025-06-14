#!/usr/bin/env python3
"""
Тестовый скрипт для Google Places API (New) - Text Search
Демонстрирует структуру запроса и анализирует ответ API
"""

import requests
import json

def test_places_api():
    """
    Тестирует Google Places API Text Search (New)
    """
    
    # URL для Places API Text Search (New)
    url = "https://places.googleapis.com/v1/places:searchText"
    
    # Заголовки запроса
    headers = {
        "Content-Type": "application/json",
        # Для реального использования нужен API ключ:
        # "X-Goog-Api-Key": "YOUR_API_KEY",
        # Поля, которые мы хотим получить в ответе
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.rating,places.priceLevel"
    }
    
    # Тело запроса
    request_body = {
        "textQuery": "pizza restaurants in New York",
        "languageCode": "en",
        "regionCode": "US",
        "maxResultCount": 5
    }
    
    print("=== Тестовый запрос к Google Places API (New) ===")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Request Body: {json.dumps(request_body, indent=2)}")
    print()
    
    try:
        # Выполняем POST запрос
        response = requests.post(url, headers=headers, json=request_body, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()
        
        # Пытаемся получить JSON ответ
        try:
            response_json = response.json()
            print("Response Body:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Response Body (raw text):")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    
    print("\n" + "="*60)
    
    # Демонстрируем правильную структуру запроса с API ключом
    print("\n=== Пример правильного запроса с API ключом ===")
    
    correct_headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": "YOUR_ACTUAL_API_KEY_HERE",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.rating"
    }
    
    print("Правильные заголовки:")
    print(json.dumps(correct_headers, indent=2))
    
    print("\nПример curl команды:")
    curl_command = f"""curl -X POST -d '{json.dumps(request_body)}' \\
-H 'Content-Type: application/json' \\
-H 'X-Goog-Api-Key: YOUR_API_KEY' \\
-H 'X-Goog-FieldMask: places.displayName,places.formattedAddress,places.location' \\
'{url}'"""
    
    print(curl_command)

if __name__ == "__main__":
    test_places_api()

