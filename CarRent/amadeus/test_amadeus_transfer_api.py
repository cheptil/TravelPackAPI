import requests
import json
from datetime import datetime, timedelta

# Базовый URL для тестовой среды Amadeus
BASE_URL = "https://test.api.amadeus.com/v1"

def test_transfer_search():
    """
    Тестовый запрос к API Amadeus Transfer Search
    """
    
    # URL эндпоинта
    url = f"{BASE_URL}/shopping/transfer-offers"
    
    # Заголовки запроса
    headers = {
        "Content-Type": "application/json",
        # "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Требуется API ключ
    }
    
    # Тестовые данные запроса
    # Трансфер из аэропорта CDG (Париж) до Эйфелевой башни
    request_data = {
        "startLocationCode": "CDG",  # Аэропорт Шарль де Голль
        "endAddressLine": "Avenue Anatole France, 5",
        "endCityName": "Paris",
        "endZipCode": "75007",
        "endCountryCode": "FR",
        "endName": "Eiffel Tower Area",
        "endGeoCode": "48.859466,2.2976965",
        "transferType": "PRIVATE",
        "startDateTime": "2024-12-15T14:30:00",  # Дата в будущем
        "passengers": 2
    }
    
    print("=== Тестовый запрос к Amadeus Transfer Search API ===")
    print(f"URL: {url}")
    print(f"Метод: POST")
    print(f"Заголовки: {json.dumps(headers, indent=2)}")
    print(f"Данные запроса:")
    print(json.dumps(request_data, indent=2))
    print("\n" + "="*50)
    
    try:
        # Выполняем запрос
        response = requests.post(url, headers=headers, json=request_data)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        # Пытаемся получить JSON ответ
        try:
            response_json = response.json()
            print(f"Ответ API:")
            print(json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print(f"Ответ (текст): {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    test_transfer_search()

