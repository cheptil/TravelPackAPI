import requests
import json

def test_geodb_cities_api():
    """
    Тестовый запрос к API GeoDB Cities
    Примечание: Для работы требуется API ключ от RapidAPI
    """
    
    # URL эндпоинта для получения городов
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    
    # Параметры запроса - получаем российские города
    params = {
        "countryIds": "RU",
        "limit": 10  # Ограничиваем количество результатов
    }
    
    # Заголовки (требуется API ключ)
    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY_HERE",  # Замените на реальный ключ
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    
    try:
        print("Отправляем запрос к GeoDB Cities API...")
        print(f"URL: {url}")
        print(f"Параметры: {params}")
        
        # Выполняем запрос
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Запрос выполнен успешно!")
            print(f"Получено данных: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # Анализируем структуру ответа
            if 'data' in data:
                cities = data['data']
                print(f"\nКоличество городов в ответе: {len(cities)}")
                
                if cities:
                    print("\nПример первого города:")
                    first_city = cities[0]
                    for key, value in first_city.items():
                        print(f"  {key}: {value}")
                        
        elif response.status_code == 401:
            print("Ошибка авторизации: требуется действительный API ключ")
        elif response.status_code == 403:
            print("Доступ запрещен: проверьте права доступа к API")
        else:
            print(f"Ошибка запроса: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

def test_without_api_key():
    """
    Тест запроса без API ключа для демонстрации структуры
    """
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    params = {"countryIds": "RU", "limit": 5}
    
    print("Тестируем запрос без API ключа...")
    print(f"URL: {url}")
    print(f"Параметры: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"Статус ответа: {response.status_code}")
        print(f"Ответ: {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    print("=== Тестирование API GeoDB Cities ===\n")
    
    # Тест без API ключа (покажет требование авторизации)
    test_without_api_key()
    
    print("\n" + "="*50 + "\n")
    
    # Тест с API ключом (требует настройки)
    print("Для полного тестирования замените YOUR_API_KEY_HERE на реальный ключ от RapidAPI")
    # test_geodb_cities_api()

