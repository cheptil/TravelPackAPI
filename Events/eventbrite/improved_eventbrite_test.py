import requests
import json

# Базовый URL API Eventbrite
base_url = "https://www.eventbriteapi.com/v3"

# Заголовки для аутентификации (токен нужно получить отдельно)
def get_headers(token=None):
    """Возвращает заголовки для запросов"""
    if token:
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    else:
        return {'Content-Type': 'application/json'}

def test_user_organizations(token=None):
    """Тестируем получение организаций пользователя"""
    url = f"{base_url}/users/me/organizations/"
    headers = get_headers(token)
    
    print(f"Запрос: GET {url}")
    print(f"Заголовки: {headers}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Детали ошибки: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"Текст ошибки: {response.text}")
                
    except Exception as e:
        print(f"Исключение при запросе: {e}")

def test_organization_events(organization_id, token=None):
    """Тестируем получение событий организации"""
    url = f"{base_url}/organizations/{organization_id}/events/"
    headers = get_headers(token)
    
    print(f"Запрос: GET {url}")
    print(f"Заголовки: {headers}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Детали ошибки: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"Текст ошибки: {response.text}")
                
    except Exception as e:
        print(f"Исключение при запросе: {e}")

def test_event_details(event_id, token=None, expand=None):
    """Тестируем получение деталей события"""
    url = f"{base_url}/events/{event_id}/"
    headers = get_headers(token)
    
    params = {}
    if expand:
        params['expand'] = expand
    
    print(f"Запрос: GET {url}")
    print(f"Параметры: {params}")
    print(f"Заголовки: {headers}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Статус ответа: {response.status_code}")
        print(f"Полный URL: {response.url}")
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Детали ошибки: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"Текст ошибки: {response.text}")
                
    except Exception as e:
        print(f"Исключение при запросе: {e}")

def test_categories(token=None):
    """Тестируем получение категорий"""
    url = f"{base_url}/categories/"
    headers = get_headers(token)
    
    print(f"Запрос: GET {url}")
    print(f"Заголовки: {headers}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Детали ошибки: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"Текст ошибки: {response.text}")
                
    except Exception as e:
        print(f"Исключение при запросе: {e}")

if __name__ == "__main__":
    print("=== Улучшенное тестирование API Eventbrite ===\n")
    
    # Токен нужно получить через OAuth процесс
    # Для демонстрации используем None
    token = None
    
    print("1. Тестируем получение организаций пользователя:")
    test_user_organizations(token)
    
    print("\n" + "="*60 + "\n")
    
    print("2. Тестируем получение категорий:")
    test_categories(token)
    
    print("\n" + "="*60 + "\n")
    
    print("3. Тестируем получение событий организации (пример ID):")
    test_organization_events("123456789", token)
    
    print("\n" + "="*60 + "\n")
    
    print("4. Тестируем получение деталей события с расширениями:")
    test_event_details("123456789", token, "venue,category,ticket_availability")
    
    print("\n" + "="*60 + "\n")
    
    print("ПРИМЕЧАНИЕ:")
    print("Для полноценного тестирования необходимо:")
    print("1. Зарегистрировать приложение в Eventbrite")
    print("2. Получить OAuth токен")
    print("3. Использовать реальные ID организаций и событий")

