import requests
import json
from datetime import datetime

def test_europeana_api_detailed():
    """
    Расширенное тестирование API Europeana с демонстрационным ключом
    """
    
    print("=== РАСШИРЕННОЕ ТЕСТИРОВАНИЕ API EUROPEANA ===")
    print(f"Время тестирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Базовые параметры
    base_url = "https://api.europeana.eu/record/v2/search.json"
    api_key = "api2demo"
    
    # Тест 1: Базовый поиск
    print("1. БАЗОВЫЙ ПОИСК")
    print("-" * 30)
    
    params = {
        'wskey': api_key,
        'query': 'Van Gogh',
        'rows': 3,
        'profile': 'rich'
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Найдено объектов: {data['totalResults']}")
            print(f"✓ Возвращено: {data['itemsCount']}")
            
            # Анализ первого объекта
            if data['items']:
                item = data['items'][0]
                print(f"✓ Первый объект: {item.get('title', ['Без названия'])[0]}")
                print(f"✓ Тип: {item.get('type', 'Неизвестно')}")
                print(f"✓ Провайдер: {item.get('dataProvider', ['Неизвестно'])[0]}")
                
                # Сохраняем результат
                with open('/home/ubuntu/van_gogh_search.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            print(f"✗ Ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Исключение: {e}")
    
    print()
    
    # Тест 2: Поиск с фильтрами
    print("2. ПОИСК С ФИЛЬТРАМИ")
    print("-" * 30)
    
    params_filtered = {
        'wskey': api_key,
        'query': 'painting',
        'qf': 'TYPE:IMAGE',  # Только изображения
        'rows': 5,
        'profile': 'standard'
    }
    
    try:
        response = requests.get(base_url, params=params_filtered)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Найдено картин (изображений): {data['totalResults']}")
            
            # Анализ типов объектов
            types = {}
            for item in data['items']:
                item_type = item.get('type', 'Unknown')
                types[item_type] = types.get(item_type, 0) + 1
            
            print(f"✓ Типы объектов: {types}")
            
        else:
            print(f"✗ Ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Исключение: {e}")
    
    print()
    
    # Тест 3: Поиск по стране
    print("3. ПОИСК ПО СТРАНЕ")
    print("-" * 30)
    
    params_country = {
        'wskey': api_key,
        'query': '*',
        'qf': 'COUNTRY:russia',
        'rows': 3,
        'profile': 'minimal'
    }
    
    try:
        response = requests.get(base_url, params=params_country)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Объектов из России: {data['totalResults']}")
            
            for i, item in enumerate(data['items'], 1):
                title = item.get('title', ['Без названия'])[0]
                provider = item.get('dataProvider', ['Неизвестно'])[0]
                print(f"  {i}. {title} ({provider})")
                
        else:
            print(f"✗ Ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Исключение: {e}")
    
    print()
    
    # Тест 4: Тестирование Record API
    print("4. ТЕСТИРОВАНИЕ RECORD API")
    print("-" * 30)
    
    # Используем ID из предыдущего успешного запроса
    record_id = "/916100/GSM_event_682045"
    record_url = f"https://api.europeana.eu/record{record_id}.json"
    
    params_record = {
        'wskey': api_key
    }
    
    try:
        response = requests.get(record_url, params=params_record)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Получен объект: {record_id}")
            
            # Анализ структуры объекта
            if 'object' in data:
                obj = data['object']
                print(f"✓ Тип объекта: {obj.get('type', 'Неизвестно')}")
                
                # Подсчет полей метаданных
                metadata_fields = len([k for k in obj.keys() if not k.startswith('_')])
                print(f"✓ Полей метаданных: {metadata_fields}")
                
                # Сохраняем детальный объект
                with open('/home/ubuntu/detailed_record.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
        else:
            print(f"✗ Ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Исключение: {e}")
    
    print()
    
    # Тест 5: Анализ лимитов API
    print("5. АНАЛИЗ ЛИМИТОВ API")
    print("-" * 30)
    
    # Тестируем максимальное количество результатов
    max_rows_test = [10, 50, 100, 500, 1000]
    
    for rows in max_rows_test:
        params_limit = {
            'wskey': api_key,
            'query': 'art',
            'rows': rows,
            'profile': 'minimal'
        }
        
        try:
            response = requests.get(base_url, params=params_limit)
            if response.status_code == 200:
                data = response.json()
                actual_rows = data['itemsCount']
                print(f"✓ Запрошено: {rows}, получено: {actual_rows}")
                
                if actual_rows < rows:
                    print(f"  → Лимит достигнут на {actual_rows} объектах")
                    break
            else:
                print(f"✗ Ошибка при rows={rows}: {response.status_code}")
                break
                
        except Exception as e:
            print(f"✗ Исключение при rows={rows}: {e}")
            break
    
    print()
    
    # Тест 6: Тестирование различных профилей
    print("6. ТЕСТИРОВАНИЕ ПРОФИЛЕЙ ДАННЫХ")
    print("-" * 30)
    
    profiles = ['minimal', 'standard', 'rich']
    
    for profile in profiles:
        params_profile = {
            'wskey': api_key,
            'query': 'Mona Lisa',
            'rows': 1,
            'profile': profile
        }
        
        try:
            response = requests.get(base_url, params=params_profile)
            if response.status_code == 200:
                data = response.json()
                if data['items']:
                    item = data['items'][0]
                    field_count = len(item.keys())
                    print(f"✓ Профиль '{profile}': {field_count} полей")
                else:
                    print(f"✓ Профиль '{profile}': нет результатов")
            else:
                print(f"✗ Ошибка для профиля '{profile}': {response.status_code}")
                
        except Exception as e:
            print(f"✗ Исключение для профиля '{profile}': {e}")
    
    print()
    print("=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")

if __name__ == "__main__":
    test_europeana_api_detailed()

