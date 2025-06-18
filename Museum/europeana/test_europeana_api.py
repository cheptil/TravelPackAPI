import requests
import json

# Попробуем сделать тестовый запрос к API Europeana
# Базовый URL для Search API
base_url = "https://api.europeana.eu/record/v2/search.json"

# Параметры запроса (попробуем без API ключа для начала)
params = {
    'query': 'Van Gogh',  # Поиск по Ван Гогу
    'rows': 5,  # Ограничим количество результатов
    'profile': 'minimal'  # Минимальный профиль данных
}

print("Тестовый запрос к Europeana Search API")
print("=" * 50)
print(f"URL: {base_url}")
print(f"Параметры: {params}")
print()

try:
    # Выполняем запрос
    response = requests.get(base_url, params=params)
    
    print(f"Статус ответа: {response.status_code}")
    print(f"URL запроса: {response.url}")
    print()
    
    if response.status_code == 200:
        # Парсим JSON ответ
        data = response.json()
        
        print("Успешный ответ!")
        print(f"Тип данных: {type(data)}")
        print()
        
        # Выводим структуру ответа
        if isinstance(data, dict):
            print("Ключи в ответе:")
            for key in data.keys():
                print(f"  - {key}")
            print()
            
            # Если есть результаты поиска
            if 'items' in data:
                print(f"Количество найденных элементов: {len(data['items'])}")
                print()
                
                # Показываем первый элемент
                if data['items']:
                    first_item = data['items'][0]
                    print("Первый найденный элемент:")
                    print(json.dumps(first_item, indent=2, ensure_ascii=False))
            
            # Показываем общую информацию
            if 'totalResults' in data:
                print(f"Общее количество результатов: {data['totalResults']}")
        
        # Сохраняем полный ответ в файл
        with open('/home/ubuntu/europeana_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nПолный ответ сохранен в файл: /home/ubuntu/europeana_response.json")
        
    else:
        print(f"Ошибка запроса: {response.status_code}")
        print(f"Текст ошибки: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
except json.JSONDecodeError as e:
    print(f"Ошибка при парсинге JSON: {e}")
    print(f"Ответ сервера: {response.text}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")

