import requests
import json

def test_mapbox_geocoding():
    """
    Тестирование Mapbox Geocoding API
    """
    
    print("=== Тестирование Mapbox Geocoding API ===\n")
    
    # Базовые URL для API
    forward_url = "https://api.mapbox.com/search/geocode/v6/forward"
    reverse_url = "https://api.mapbox.com/search/geocode/v6/reverse"
    
    # Тестовые параметры
    test_address = "Moscow, Russia"
    test_longitude = 37.6176
    test_latitude = 55.7558  # Координаты Москвы
    
    print("1. Тестирование Forward Geocoding (без токена)")
    print(f"Запрос: {test_address}")
    
    # Попытка запроса без токена для анализа структуры ошибки
    forward_params = {
        'q': test_address
    }
    
    try:
        response = requests.get(forward_url, params=forward_params, timeout=10)
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            try:
                json_response = response.json()
                print(f"JSON ответ: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Текстовый ответ: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("2. Тестирование Reverse Geocoding (без токена)")
    print(f"Координаты: {test_longitude}, {test_latitude}")
    
    # Попытка обратного геокодирования без токена
    reverse_params = {
        'longitude': test_longitude,
        'latitude': test_latitude
    }
    
    try:
        response = requests.get(reverse_url, params=reverse_params, timeout=10)
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            try:
                json_response = response.json()
                print(f"JSON ответ: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Текстовый ответ: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Попробуем с фиктивным токеном для анализа структуры ошибки
    print("3. Тестирование с фиктивным токеном")
    
    forward_params_with_token = {
        'q': test_address,
        'access_token': 'test_token'
    }
    
    try:
        response = requests.get(forward_url, params=forward_params_with_token, timeout=10)
        print(f"Статус код: {response.status_code}")
        
        if response.text:
            try:
                json_response = response.json()
                print(f"JSON ответ: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Текстовый ответ: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")

if __name__ == "__main__":
    test_mapbox_geocoding()

