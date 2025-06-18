import requests
import json

# Базовый URL API Ticketmaster Discovery
base_url = "https://app.ticketmaster.com/discovery/v2"

def test_api_without_key():
    """Тестовый запрос без API ключа для демонстрации ошибки аутентификации"""
    url = f"{base_url}/events.json"
    params = {
        'size': 1,
        'countryCode': 'US'
    }
    
    print("=== Тестовый запрос без API ключа ===")
    print(f"URL: {url}")
    print(f"Параметры: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            try:
                data = response.json()
                print(f"Ответ JSON: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Текст ответа: {response.text}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

def test_api_with_demo_key():
    """Попытка использовать демо-ключ или общедоступный ключ"""
    # Некоторые API предоставляют демо-ключи для тестирования
    demo_keys = [
        'demo',
        'test',
        'sample',
        'apikey'  # иногда используется как плейсхолдер
    ]
    
    url = f"{base_url}/events.json"
    
    for key in demo_keys:
        params = {
            'apikey': key,
            'size': 1,
            'countryCode': 'US'
        }
        
        print(f"\n=== Тестирование с ключом: {key} ===")
        print(f"URL: {url}")
        print(f"Параметры: {params}")
        
        try:
            response = requests.get(url, params=params)
            print(f"Статус код: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Успешный запрос!")
                data = response.json()
                print(f"Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return response
            else:
                if response.text:
                    try:
                        data = response.json()
                        print(f"Ошибка: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    except json.JSONDecodeError:
                        print(f"Текст ответа: {response.text}")
                        
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
    
    return None

if __name__ == "__main__":
    print("Тестирование API Ticketmaster Discovery")
    print("=" * 50)
    
    # Тест без ключа
    test_api_without_key()
    
    # Тест с демо-ключами
    test_api_with_demo_key()
    
    print("\n" + "=" * 50)
    print("Для полноценного тестирования необходимо получить API ключ")
    print("на сайте: https://developer.ticketmaster.com/")

