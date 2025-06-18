import requests
import json

# Базовый URL API Eventbrite
base_url = "https://www.eventbriteapi.com/v3"

# Попробуем сделать запрос к эндпоинту категорий (обычно публичный)
def test_categories_endpoint():
    """Тестируем эндпоинт категорий"""
    url = f"{base_url}/categories/"
    
    try:
        response = requests.get(url)
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            
    except Exception as e:
        print(f"Исключение при запросе: {e}")

# Попробуем сделать запрос к эндпоинту поиска событий
def test_events_search():
    """Тестируем эндпоинт поиска событий"""
    url = f"{base_url}/events/search/"
    
    # Параметры поиска
    params = {
        'location.address': 'San Francisco',
        'expand': 'venue'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Статус ответа: {response.status_code}")
        print(f"URL запроса: {response.url}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            
    except Exception as e:
        print(f"Исключение при запросе: {e}")

# Попробуем получить информацию о пользователе (требует токен)
def test_user_me():
    """Тестируем эндпоинт информации о пользователе"""
    url = f"{base_url}/users/me/"
    
    try:
        response = requests.get(url)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            
    except Exception as e:
        print(f"Исключение при запросе: {e}")

if __name__ == "__main__":
    print("=== Тестирование API Eventbrite ===\n")
    
    print("1. Тестируем эндпоинт категорий:")
    test_categories_endpoint()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Тестируем поиск событий:")
    test_events_search()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Тестируем эндпоинт пользователя (без токена):")
    test_user_me()

