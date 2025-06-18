import requests
import json
from urllib.parse import quote

def test_bandsintown_api_with_example_id():
    """
    Тестовый запрос к Bandsintown API с использованием примера app_id из документации
    """
    
    # Базовый URL API
    base_url = "https://rest.bandsintown.com"
    
    # Параметры для тестового запроса
    artist_name = "Maroon 5"  # Используем артиста из примера в документации
    app_id = "yOUrSuP3r3ven7aPp-id"  # Пример app_id из документации
    
    # Кодирование имени артиста для URL
    encoded_artist = quote(artist_name)
    
    # Формирование URL для запроса информации об артисте
    artist_info_url = f"{base_url}/artists/{encoded_artist}"
    
    # Параметры запроса
    params = {
        "app_id": app_id
    }
    
    print(f"Выполняю запрос к Bandsintown API с примером app_id...")
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

def test_different_artists():
    """
    Тестирование с разными артистами
    """
    artists = ["Coldplay", "The Beatles", "Radiohead", "Adele"]
    app_id = "yOUrSuP3r3ven7aPp-id"
    base_url = "https://rest.bandsintown.com"
    
    for artist in artists:
        print(f"\n=== Тестирование артиста: {artist} ===")
        encoded_artist = quote(artist)
        url = f"{base_url}/artists/{encoded_artist}"
        params = {"app_id": app_id}
        
        try:
            response = requests.get(url, params=params)
            print(f"Статус: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Успех! Найден артист: {data.get('name', 'Неизвестно')}")
                print(f"ID: {data.get('id', 'Неизвестно')}")
                print(f"URL: {data.get('url', 'Неизвестно')}")
                if 'tracker_count' in data:
                    print(f"Количество подписчиков: {data['tracker_count']}")
            else:
                print(f"Ошибка: {response.text}")
                
        except Exception as e:
            print(f"Исключение: {e}")

if __name__ == "__main__":
    print("=== Тестирование Bandsintown API с примером app_id ===\n")
    
    # Тест 1: Использование примера из документации
    print("1. Тестирование с Maroon 5 (пример из документации)")
    artist_data = test_bandsintown_api_with_example_id()
    
    # Тест 2: Тестирование с разными артистами
    print("\n2. Тестирование с разными артистами")
    test_different_artists()
    
    print("\n=== Тестирование завершено ===")

