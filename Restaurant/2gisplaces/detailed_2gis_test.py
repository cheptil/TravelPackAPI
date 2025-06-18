import requests
import json

def detailed_api_test():
    """Детальное тестирование API 2GIS с анализом результатов"""
    
    base_url = "https://catalog.api.2gis.com/3.0/items"
    
    # Тестовые запросы с разными параметрами
    test_cases = [
        {
            "name": "Поиск кафе в Москве",
            "params": {
                'q': 'cafe',
                'location': '37.630866,55.752256',
                'key': 'demo',
                'page_size': 5
            }
        },
        {
            "name": "Поиск ресторанов с дополнительными полями",
            "params": {
                'q': 'restaurant',
                'location': '37.630866,55.752256',
                'key': 'demo',
                'page_size': 3,
                'fields': 'items.point,items.contact_groups,items.schedule'
            }
        },
        {
            "name": "Поиск в радиусе с сортировкой по расстоянию",
            "params": {
                'q': 'pizza',
                'point': '37.630866,55.752256',
                'radius': '1000',
                'location': '37.630866,55.752256',
                'sort': 'distance',
                'key': 'demo',
                'page_size': 3
            }
        },
        {
            "name": "Поиск по типу объекта",
            "params": {
                'q': 'bank',
                'type': 'branch',
                'location': '37.630866,55.752256',
                'key': 'demo',
                'page_size': 3
            }
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"ТЕСТ: {test_case['name']}")
        print(f"{'='*60}")
        
        try:
            response = requests.get(base_url, params=test_case['params'])
            
            print(f"Статус ответа: {response.status_code}")
            print(f"URL запроса: {response.url}")
            
            if response.status_code == 200:
                json_response = response.json()
                
                # Анализируем структуру ответа
                meta = json_response.get('meta', {})
                result = json_response.get('result', {})
                items = result.get('items', [])
                total = result.get('total', 0)
                
                print(f"\nМетаданные:")
                print(f"  API версия: {meta.get('api_version')}")
                print(f"  Код ответа: {meta.get('code')}")
                print(f"  Дата выпуска: {meta.get('issue_date')}")
                
                print(f"\nРезультаты:")
                print(f"  Всего найдено: {total}")
                print(f"  Возвращено объектов: {len(items)}")
                
                # Анализируем первый объект детально
                if items:
                    first_item = items[0]
                    print(f"\nДетали первого объекта:")
                    print(f"  ID: {first_item.get('id')}")
                    print(f"  Название: {first_item.get('name')}")
                    print(f"  Тип: {first_item.get('type')}")
                    print(f"  Адрес: {first_item.get('address_name')}")
                    print(f"  Комментарий к адресу: {first_item.get('address_comment')}")
                    
                    # Проверяем наличие дополнительных полей
                    if 'point' in first_item:
                        point = first_item['point']
                        print(f"  Координаты: {point.get('lat')}, {point.get('lon')}")
                    
                    if 'contact_groups' in first_item:
                        print(f"  Контактная информация: Да")
                    
                    if 'schedule' in first_item:
                        print(f"  Расписание работы: Да")
                    
                    if 'ads' in first_item:
                        ads = first_item['ads']
                        print(f"  Реклама: {ads.get('text', 'Нет текста')}")
                
                # Сохраняем результат для анализа
                results.append({
                    'test_name': test_case['name'],
                    'status': 'success',
                    'total_found': total,
                    'items_returned': len(items),
                    'response': json_response
                })
                
                print(f"\n--- Полный JSON ответ ---")
                print(json.dumps(json_response, indent=2, ensure_ascii=False))
                
            else:
                error_response = response.json() if response.content else {}
                print(f"Ошибка: {response.status_code}")
                print(json.dumps(error_response, indent=2, ensure_ascii=False))
                
                results.append({
                    'test_name': test_case['name'],
                    'status': 'error',
                    'error_code': response.status_code,
                    'error_response': error_response
                })
                
        except Exception as e:
            print(f"Исключение при выполнении запроса: {e}")
            results.append({
                'test_name': test_case['name'],
                'status': 'exception',
                'error': str(e)
            })
    
    # Сводка результатов
    print(f"\n{'='*60}")
    print("СВОДКА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
    print(f"{'='*60}")
    
    for result in results:
        print(f"Тест: {result['test_name']}")
        print(f"Статус: {result['status']}")
        if result['status'] == 'success':
            print(f"  Найдено объектов: {result['total_found']}")
            print(f"  Возвращено: {result['items_returned']}")
        print()
    
    return results

if __name__ == "__main__":
    detailed_api_test()

