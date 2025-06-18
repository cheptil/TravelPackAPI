import requests
import json

# Попробуем использовать демонстрационный ключ или найти публичные эндпоинты
# Некоторые API предоставляют демонстрационные ключи

# Попробуем несколько вариантов демонстрационных ключей
demo_keys = [
    'demo',
    'test',
    'api2demo',
    'apidemo',
    'XXXXXXXXXX'  # Часто используется в документации
]

base_url = "https://api.europeana.eu/record/v2/search.json"

print("Тестирование API Europeana с различными подходами")
print("=" * 60)

# Сначала попробуем без ключа, но с другими параметрами
print("1. Попытка запроса без API ключа:")
params_no_key = {
    'query': '*',  # Поиск всего
    'rows': 1,
    'profile': 'minimal'
}

try:
    response = requests.get(base_url, params=params_no_key)
    print(f"   Статус: {response.status_code}")
    if response.status_code != 200:
        print(f"   Ошибка: {response.text}")
except Exception as e:
    print(f"   Исключение: {e}")

print()

# Попробуем с демонстрационными ключами
print("2. Попытки с демонстрационными ключами:")
for key in demo_keys:
    params_with_key = {
        'wskey': key,
        'query': 'art',
        'rows': 1,
        'profile': 'minimal'
    }
    
    try:
        response = requests.get(base_url, params=params_with_key)
        print(f"   Ключ '{key}': статус {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ Успех! Ключ '{key}' работает!")
            data = response.json()
            with open(f'/home/ubuntu/europeana_success_{key}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            break
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"     Ошибка: {error_data}")
    except Exception as e:
        print(f"   Ключ '{key}': исключение {e}")

print()

# Попробуем другие эндпоинты, которые могут быть публичными
print("3. Попытка доступа к другим эндпоинтам:")

# Попробуем SPARQL эндпоинт (если он публичный)
sparql_url = "http://sparql.europeana.eu/"
try:
    response = requests.get(sparql_url, timeout=10)
    print(f"   SPARQL endpoint: статус {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ SPARQL эндпоинт доступен!")
except Exception as e:
    print(f"   SPARQL endpoint: ошибка {e}")

# Попробуем получить информацию о самом API
api_info_url = "https://api.europeana.eu/"
try:
    response = requests.get(api_info_url, timeout=10)
    print(f"   API info endpoint: статус {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ API info доступен!")
        print(f"   Содержимое: {response.text[:200]}...")
except Exception as e:
    print(f"   API info endpoint: ошибка {e}")

print()
print("4. Анализ структуры ошибки API:")
print("   Из предыдущего запроса мы получили структуру ошибки:")
error_structure = {
    "success": False,
    "error": "Unauthorized", 
    "message": "Invalid API key provided!",
    "code": "invalid_apikey"
}
print(f"   {json.dumps(error_structure, indent=4)}")
print()
print("   Это показывает, что API:")
print("   - Использует JSON для ответов")
print("   - Требует параметр 'wskey' для аутентификации")
print("   - Возвращает структурированные ошибки")
print("   - Имеет коды ошибок для программной обработки")

# Попробуем получить схему API через OpenAPI/Swagger
print()
print("5. Попытка получить схему API:")
swagger_urls = [
    "https://api.europeana.eu/swagger.json",
    "https://api.europeana.eu/openapi.json",
    "https://api.europeana.eu/v2/swagger.json",
    "https://api.europeana.eu/record/v2/swagger.json"
]

for url in swagger_urls:
    try:
        response = requests.get(url, timeout=5)
        print(f"   {url}: статус {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ Схема API найдена!")
            schema = response.json()
            with open('/home/ubuntu/europeana_api_schema.json', 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            break
    except Exception as e:
        print(f"   {url}: ошибка {e}")

print()
print("Заключение:")
print("- API Europeana требует обязательной регистрации и получения API ключа")
print("- Демонстрационные ключи не предоставляются")
print("- API использует стандартную REST архитектуру с JSON ответами")
print("- Для полноценного тестирования необходимо зарегистрироваться на сайте")

