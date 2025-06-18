import requests
import json

# Тестовый запрос к Amadeus City Search API
def test_amadeus_city_search():
    # URL для тестовой среды
    base_url = "https://test.api.amadeus.com/v1"
    endpoint = "/reference-data/locations/cities"
    
    # Параметры запроса
    params = {
        "keyword": "PAR",  # Ищем города, начинающиеся с "PAR"
        "max": 5,          # Максимум 5 результатов
        "include": "AIRPORTS"  # Включаем информацию об аэропортах
    }
    
    # Заголовки (пока без авторизации)
    headers = {
        "Accept": "application/vnd.amadeus+json"
    }
    
    try:
        print("Делаем запрос к Amadeus City Search API...")
        print(f"URL: {base_url + endpoint}")
        print(f"Параметры: {params}")
        print(f"Заголовки: {headers}")
        print("-" * 50)
        
        response = requests.get(
            base_url + endpoint,
            params=params,
            headers=headers
        )
        
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            data = response.json()
            print("Успешный ответ:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("Ошибка:")
            print(f"Статус: {response.status_code}")
            print(f"Текст ответа: {response.text}")
            
            # Попробуем распарсить JSON ошибки
            try:
                error_data = response.json()
                print("JSON ошибки:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print("Не удалось распарсить JSON ошибки")
                
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    test_amadeus_city_search()

