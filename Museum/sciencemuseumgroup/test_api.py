import requests
import json

# Попробуем различные возможные API endpoints для Science Museum Group
base_urls = [
    "https://collection.sciencemuseumgroup.org.uk/api",
    "https://api.sciencemuseumgroup.org.uk",
    "https://collection.sciencemuseumgroup.org.uk/search",
]

# Попробуем также endpoints, основанные на структуре сайта
endpoints_to_test = [
    "/objects",
    "/people", 
    "/documents",
    "/search",
    "/object",
    "/person",
    "/document"
]

print("=== Тестирование API endpoints Science Museum Group ===\n")

# Функция для тестирования endpoint
def test_endpoint(url, timeout=10):
    try:
        print(f"Тестирую: {url}")
        response = requests.get(url, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        print(f"Статус код: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'не указан')}")
        
        if response.status_code == 200:
            # Попробуем распарсить как JSON
            try:
                data = response.json()
                print(f"JSON ответ получен, размер: {len(str(data))} символов")
                print("Первые 500 символов ответа:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                return True, data
            except:
                # Если не JSON, покажем первые символы как текст
                text = response.text[:500]
                print(f"Текстовый ответ (первые 500 символов):\n{text}")
                return True, text
        else:
            print(f"Ошибка: {response.status_code}")
            if response.text:
                print(f"Сообщение об ошибке: {response.text[:200]}")
                
    except requests.exceptions.Timeout:
        print("Таймаут запроса")
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("-" * 50)
    return False, None

# Тестируем базовые URLs
successful_endpoints = []

for base_url in base_urls:
    success, data = test_endpoint(base_url)
    if success:
        successful_endpoints.append((base_url, data))

# Тестируем endpoints с базовыми URL
for base_url in base_urls:
    for endpoint in endpoints_to_test:
        url = base_url + endpoint
        success, data = test_endpoint(url)
        if success:
            successful_endpoints.append((url, data))

print(f"\n=== РЕЗУЛЬТАТЫ ===")
print(f"Найдено работающих endpoints: {len(successful_endpoints)}")

for url, data in successful_endpoints:
    print(f"\nРаботающий endpoint: {url}")
    if isinstance(data, dict):
        print("Тип данных: JSON")
        print(f"Ключи верхнего уровня: {list(data.keys()) if data else 'пусто'}")
    else:
        print("Тип данных: текст/HTML")

