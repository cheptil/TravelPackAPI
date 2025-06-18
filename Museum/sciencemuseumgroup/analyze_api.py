import requests
import json

print("=== Детальный анализ API Science Museum Group ===\n")

# Теперь проанализируем найденные рабочие endpoints более подробно
def analyze_api_response(url, description):
    print(f"=== {description} ===")
    print(f"URL: {url}")
    
    try:
        headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✓ Успешный ответ")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Размер ответа: {len(response.text)} символов")
            
            # Анализируем структуру
            print(f"\nСтруктура ответа:")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"  {key}: список из {len(value)} элементов")
                        if value and isinstance(value[0], dict):
                            print(f"    Ключи первого элемента: {list(value[0].keys())[:5]}...")
                    elif isinstance(value, dict):
                        print(f"  {key}: словарь с ключами {list(value.keys())[:5]}...")
                    else:
                        print(f"  {key}: {type(value).__name__} = {str(value)[:50]}...")
            
            # Сохраняем полный ответ в файл для анализа
            filename = f"/home/ubuntu/api_response_{description.lower().replace(' ', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Полный ответ сохранен в: {filename}")
            
            return data
            
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    
    print("-" * 60)

# Анализируем разные типы запросов
responses = {}

# 1. Общий поиск без параметров
responses['general_search'] = analyze_api_response(
    "https://collection.sciencemuseumgroup.org.uk/search?format=json",
    "Общий поиск без параметров"
)

# 2. Поиск объектов
responses['objects_search'] = analyze_api_response(
    "https://collection.sciencemuseumgroup.org.uk/search/objects?format=json",
    "Поиск объектов"
)

# 3. Поиск по ключевому слову
responses['keyword_search'] = analyze_api_response(
    "https://collection.sciencemuseumgroup.org.uk/search?q=telescope&format=json",
    "Поиск по ключевому слову telescope"
)

# 4. Конкретный объект
responses['specific_object'] = analyze_api_response(
    "https://collection.sciencemuseumgroup.org.uk/objects/co62245",
    "Конкретный объект co62245"
)

# 5. Попробуем поиск людей
responses['people_search'] = analyze_api_response(
    "https://collection.sciencemuseumgroup.org.uk/search/people?format=json",
    "Поиск людей"
)

# 6. Попробуем поиск документов
responses['documents_search'] = analyze_api_response(
    "https://collection.sciencemuseumgroup.org.uk/search/documents?format=json",
    "Поиск документов"
)

print("\n" + "="*80)
print("СВОДКА РЕЗУЛЬТАТОВ")
print("="*80)

for key, data in responses.items():
    if data:
        print(f"\n✓ {key.replace('_', ' ').title()}:")
        if 'data' in data:
            if isinstance(data['data'], list):
                print(f"  - Найдено записей: {len(data['data'])}")
                if data['data']:
                    first_item = data['data'][0]
                    if 'type' in first_item:
                        print(f"  - Тип записей: {first_item['type']}")
                    if 'attributes' in first_item:
                        attrs = first_item['attributes']
                        if 'title' in attrs:
                            print(f"  - Пример названия: {attrs['title'][:50]}...")
            elif isinstance(data['data'], dict):
                if 'type' in data['data']:
                    print(f"  - Тип записи: {data['data']['type']}")
                if 'attributes' in data['data']:
                    attrs = data['data']['attributes']
                    if 'title' in attrs:
                        print(f"  - Название: {attrs['title'][:50]}...")
        
        if 'meta' in data:
            meta = data['meta']
            if 'count' in meta:
                print(f"  - Общее количество: {meta['count']}")
            if 'pages' in meta:
                print(f"  - Страниц: {meta['pages']}")
    else:
        print(f"\n✗ {key.replace('_', ' ').title()}: ошибка")

print(f"\nВсе ответы сохранены в файлы /home/ubuntu/api_response_*.json для детального изучения.")

