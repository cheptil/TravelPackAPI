import requests
import json

print("=== Поиск JSON API endpoints Science Museum Group ===\n")

# Попробуем найти JSON API endpoints
# Часто API endpoints имеют префикс /api/ или возвращают JSON при определенных параметрах

test_urls = [
    # Возможные API endpoints
    "https://collection.sciencemuseumgroup.org.uk/api/search",
    "https://collection.sciencemuseumgroup.org.uk/api/objects",
    "https://collection.sciencemuseumgroup.org.uk/api/people",
    "https://collection.sciencemuseumgroup.org.uk/api/documents",
    
    # Попробуем добавить параметры для получения JSON
    "https://collection.sciencemuseumgroup.org.uk/search?format=json",
    "https://collection.sciencemuseumgroup.org.uk/search/objects?format=json",
    "https://collection.sciencemuseumgroup.org.uk/search?q=telescope&format=json",
    
    # Попробуем с Accept header для JSON
    "https://collection.sciencemuseumgroup.org.uk/search?q=telescope",
    "https://collection.sciencemuseumgroup.org.uk/objects",
    
    # Попробуем прямой доступ к объекту (из GitHub кода видно, что есть /objects/{id})
    "https://collection.sciencemuseumgroup.org.uk/objects/co62245",
    "https://collection.sciencemuseumgroup.org.uk/objects/co8232239",
]

def test_json_endpoint(url, timeout=10):
    try:
        print(f"Тестирую: {url}")
        
        # Попробуем с разными заголовками
        headers_options = [
            {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        ]
        
        for i, headers in enumerate(headers_options):
            if i > 0:
                print(f"  Попытка {i+1} с другими заголовками...")
            
            response = requests.get(url, timeout=timeout, headers=headers)
            
            print(f"  Статус код: {response.status_code}")
            content_type = response.headers.get('content-type', '')
            print(f"  Content-Type: {content_type}")
            
            if response.status_code == 200:
                # Проверим, есть ли JSON в ответе
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        print(f"  ✓ JSON ответ получен!")
                        print(f"  Размер данных: {len(str(data))} символов")
                        if isinstance(data, dict):
                            print(f"  Ключи верхнего уровня: {list(data.keys())}")
                        print("  Первые 300 символов JSON:")
                        print("  " + json.dumps(data, indent=2, ensure_ascii=False)[:300])
                        return True, data
                    except:
                        print("  Ошибка парсинга JSON")
                
                # Проверим, может ли текст содержать JSON
                text = response.text.strip()
                if text.startswith('{') or text.startswith('['):
                    try:
                        data = json.loads(text)
                        print(f"  ✓ JSON найден в тексте!")
                        print(f"  Размер данных: {len(str(data))} символов")
                        if isinstance(data, dict):
                            print(f"  Ключи верхнего уровня: {list(data.keys())}")
                        print("  Первые 300 символов JSON:")
                        print("  " + json.dumps(data, indent=2, ensure_ascii=False)[:300])
                        return True, data
                    except:
                        pass
                
                # Если это HTML, попробуем найти JSON внутри
                if 'text/html' in content_type and 'window.INITIAL_STATE' in text:
                    print("  Найден возможный JSON в HTML (INITIAL_STATE)")
                    # Попробуем извлечь JSON из JavaScript
                    import re
                    json_match = re.search(r'window\.INITIAL_STATE\s*=\s*({.*?});', text, re.DOTALL)
                    if json_match:
                        try:
                            json_str = json_match.group(1)
                            data = json.loads(json_str)
                            print(f"  ✓ JSON извлечен из HTML!")
                            print(f"  Размер данных: {len(str(data))} символов")
                            if isinstance(data, dict):
                                print(f"  Ключи верхнего уровня: {list(data.keys())}")
                            return True, data
                        except Exception as e:
                            print(f"  Ошибка извлечения JSON: {e}")
                
                print(f"  HTML ответ, первые 200 символов: {text[:200]}")
                break  # Если получили 200, не пробуем другие заголовки
            else:
                print(f"  Ошибка: {response.status_code}")
                if i == len(headers_options) - 1:  # Последняя попытка
                    if response.text:
                        print(f"  Сообщение: {response.text[:100]}")
                
    except Exception as e:
        print(f"  Ошибка: {e}")
    
    print("-" * 60)
    return False, None

# Тестируем все URL
successful_json_endpoints = []

for url in test_urls:
    success, data = test_json_endpoint(url)
    if success:
        successful_json_endpoints.append((url, data))

print(f"\n=== ИТОГОВЫЕ РЕЗУЛЬТАТЫ ===")
print(f"Найдено JSON endpoints: {len(successful_json_endpoints)}")

for url, data in successful_json_endpoints:
    print(f"\n✓ Работающий JSON endpoint: {url}")
    if isinstance(data, dict):
        print(f"  Тип: словарь с ключами {list(data.keys())}")
        # Попробуем найти интересные данные
        if 'data' in data:
            print(f"  Найден ключ 'data' с типом: {type(data['data'])}")
        if 'results' in data:
            print(f"  Найден ключ 'results' с типом: {type(data['results'])}")
        if 'objects' in data:
            print(f"  Найден ключ 'objects' с типом: {type(data['objects'])}")
    elif isinstance(data, list):
        print(f"  Тип: список с {len(data)} элементами")
        if data and isinstance(data[0], dict):
            print(f"  Ключи первого элемента: {list(data[0].keys())}")

