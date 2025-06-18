import requests
import json

# Тестовый запрос к API 2GIS Places
# Попробуем сделать запрос без ключа, чтобы увидеть структуру ошибки
# и понять, как работает API

def test_2gis_api():
    # Базовый URL API
    base_url = "https://catalog.api.2gis.com/3.0/items"
    
    # Параметры запроса (без API ключа для начала)
    params = {
        'q': 'cafe',
        'location': '37.630866,55.752256',  # Координаты Москвы
        'type': 'branch',
        'page_size': 5
    }
    
    print("=== Тестовый запрос к API 2GIS Places ===")
    print(f"URL: {base_url}")
    print(f"Параметры: {params}")
    print()
    
    try:
        # Выполняем запрос
        response = requests.get(base_url, params=params)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"URL запроса: {response.url}")
        print()
        
        # Выводим заголовки ответа
        print("=== Заголовки ответа ===")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
        print()
        
        # Пытаемся получить JSON ответ
        try:
            json_response = response.json()
            print("=== JSON ответ ===")
            print(json.dumps(json_response, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("=== Текстовый ответ ===")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

def test_with_demo_key():
    """Попробуем с демо-ключом, если он доступен"""
    base_url = "https://catalog.api.2gis.com/3.0/items"
    
    # Попробуем несколько вариантов демо-ключей
    demo_keys = ['demo', 'test', 'YOUR_KEY']
    
    params = {
        'q': 'restaurant',
        'location': '37.630866,55.752256',
        'page_size': 3
    }
    
    for demo_key in demo_keys:
        print(f"\n=== Тестирование с ключом: {demo_key} ===")
        params['key'] = demo_key
        
        try:
            response = requests.get(base_url, params=params)
            print(f"Статус: {response.status_code}")
            
            if response.status_code == 200:
                json_response = response.json()
                print("Успешный ответ!")
                print(json.dumps(json_response, indent=2, ensure_ascii=False))
                break
            else:
                try:
                    error_response = response.json()
                    print("Ошибка:")
                    print(json.dumps(error_response, indent=2, ensure_ascii=False))
                except:
                    print(f"Ошибка: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")

def test_different_endpoints():
    """Тестируем разные эндпоинты API"""
    endpoints = [
        "https://catalog.api.2gis.com/3.0/items",
        "https://catalog.api.2gis.com/2.0/region/search"
    ]
    
    for endpoint in endpoints:
        print(f"\n=== Тестирование эндпоинта: {endpoint} ===")
        
        if "region" in endpoint:
            params = {'q': 'Moscow'}
        else:
            params = {'q': 'cafe', 'location': '37.630866,55.752256'}
            
        try:
            response = requests.get(endpoint, params=params)
            print(f"Статус: {response.status_code}")
            print(f"URL: {response.url}")
            
            try:
                json_response = response.json()
                print(json.dumps(json_response, indent=2, ensure_ascii=False))
            except:
                print(response.text)
                
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    # Выполняем тесты
    test_2gis_api()
    test_with_demo_key()
    test_different_endpoints()

