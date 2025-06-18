import requests
import json
from urllib.parse import quote

def test_bandsintown_api():
    """
    Тестовый запрос к Bandsintown API для получения информации об артисте
    """
    
    # Базовый URL API
    base_url = "https://rest.bandsintown.com"
    
    # Параметры для тестового запроса
    artist_name = "Coldplay"  # Популярный артист для тестирования
    app_id = "test_app_id"    # Тестовый ID приложения
    
    # Кодирование имени артиста для URL
    encoded_artist = quote(artist_name)
    
    # Формирование URL для запроса информации об артисте
    artist_info_url = f"{base_url}/artists/{encoded_artist}"
    
    # Параметры запроса
    params = {
        "app_id": app_id
    }
    
    print(f"Выполняю запрос к Bandsintown API...")
    print(f"URL: {artist_info_url}")
    print(f"Параметры: {params}")
    print("-" * 50)
    
    try:
        # Выполнение GET запроса
        response = requests.get(artist_info_url, params=params)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        print("-" * 50)
        
        # Проверка успешности запроса
        if response.status_code == 200:
            # Парсинг JSON ответа
            data = response.json()
            print("Успешный ответ от API!")
            print("Данные об артисте:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            return data
            
        else:
            print(f"Ошибка API: {response.status_code}")
            print(f"Текст ответа: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        print(f"Текст ответа: {response.text}")
        return None

def test_artist_events():
    """
    Тестовый запрос для получения событий артиста
    """
    
    base_url = "https://rest.bandsintown.com"
    artist_name = "Coldplay"
    app_id = "test_app_id"
    
    encoded_artist = quote(artist_name)
    events_url = f"{base_url}/artists/{encoded_artist}/events"
    
    params = {
        "app_id": app_id
    }
    
    print(f"\nВыполняю запрос событий артиста...")
    print(f"URL: {events_url}")
    print(f"Параметры: {params}")
    print("-" * 50)
    
    try:
        response = requests.get(events_url, params=params)
        
        print(f"Статус ответа: {response.status_code}")
        print("-" * 50)
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ от API!")
            print(f"Количество событий: {len(data) if isinstance(data, list) else 'Не список'}")
            
            if isinstance(data, list) and len(data) > 0:
                print("Первое событие:")
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
            else:
                print("События не найдены или данные в неожиданном формате")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            
            return data
            
        else:
            print(f"Ошибка API: {response.status_code}")
            print(f"Текст ответа: {response.text}")
            return None
            
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

if __name__ == "__main__":
    print("=== Тестирование Bandsintown API ===\n")
    
    # Тест 1: Получение информации об артисте
    print("1. Тестирование получения информации об артисте")
    artist_data = test_bandsintown_api()
    
    # Тест 2: Получение событий артиста
    print("\n2. Тестирование получения событий артиста")
    events_data = test_artist_events()
    
    print("\n=== Тестирование завершено ===")

