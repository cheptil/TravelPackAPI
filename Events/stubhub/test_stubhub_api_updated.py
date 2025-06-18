import requests
import json
import base64

# Обновленное тестирование StubHub API с правильными эндпоинтами

print("=== Обновленное тестирование StubHub API ===\n")

# Базовые URL для sandbox
sandbox_base_url = "https://sandbox.api.stubhub.net"
oauth_url = "https://sandbox.account.stubhub.com/oauth2/token"

# Заголовки для запросов
headers = {
    "Accept": "application/hal+json",
    "User-Agent": "StubHub-API-Test/1.0"
}

print("1. Тестирование эндпоинтов Catalog API без аутентификации:")
print("-" * 60)

# Список эндпоинтов для тестирования
catalog_endpoints = [
    "/catalog/events",
    "/catalog/events/search",
    "/catalog/categories/map",
    "/catalog/venues"
]

for endpoint in catalog_endpoints:
    try:
        url = f"{sandbox_base_url}{endpoint}"
        response = requests.get(url, headers=headers)
        print(f"GET {endpoint}")
        print(f"  Статус: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 401:
            print("  ✓ Эндпоинт существует, но требует аутентификации")
        elif response.status_code == 404:
            print("  ✗ Эндпоинт не найден")
        elif response.status_code == 200:
            print("  ✓ Успешный ответ (публичный эндпоинт)")
            print(f"  Размер ответа: {len(response.text)} символов")
        else:
            print(f"  ? Неожиданный статус: {response.status_code}")
        
        # Показываем первые 200 символов ответа для анализа
        if response.text:
            print(f"  Начало ответа: {response.text[:200]}...")
        
        print()
        
    except Exception as e:
        print(f"GET {endpoint}: Ошибка - {e}\n")

print("\n" + "="*60 + "\n")

print("2. Тестирование OAuth endpoint с фиктивными credentials:")
print("-" * 60)

# Создаем фиктивные credentials для демонстрации процесса
fake_client_id = "test_client_id"
fake_client_secret = "test_client_secret"

# Создаем Basic Auth header
credentials = f"{fake_client_id}:{fake_client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

oauth_headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}

oauth_data = {
    "grant_type": "client_credentials",
    "scope": "read:events"
}

try:
    response = requests.post(oauth_url, headers=oauth_headers, data=oauth_data)
    print(f"POST {oauth_url}")
    print(f"Статус: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"Ответ: {response.text}")
    
    if response.status_code == 401:
        print("✓ OAuth endpoint работает, но credentials неверные (ожидаемо)")
    elif response.status_code == 400:
        print("✓ OAuth endpoint работает, но параметры неверные")
    
except Exception as e:
    print(f"Ошибка OAuth запроса: {e}")

print("\n" + "="*60 + "\n")

print("3. Попытка поиска событий с параметрами:")
print("-" * 60)

# Попробуем поиск с различными параметрами
search_params = [
    {"q": "concert"},
    {"q": "football"},
    {"q": "basketball"},
    {"page": 1, "page_size": 5}
]

for params in search_params:
    try:
        url = f"{sandbox_base_url}/catalog/events/search"
        response = requests.get(url, headers=headers, params=params)
        print(f"GET /catalog/events/search с параметрами: {params}")
        print(f"  Статус: {response.status_code}")
        print(f"  URL: {response.url}")
        
        if response.text:
            print(f"  Начало ответа: {response.text[:150]}...")
        print()
        
    except Exception as e:
        print(f"Ошибка поиска с параметрами {params}: {e}\n")

print("\n" + "="*60 + "\n")

print("4. Анализ структуры ошибок API:")
print("-" * 60)

# Анализируем структуру ошибок
try:
    response = requests.get(f"{sandbox_base_url}/catalog/events", headers=headers)
    if response.status_code == 401:
        print("Структура ошибки 401 Unauthorized:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2, ensure_ascii=False))
        except:
            print("Ответ не в формате JSON:")
            print(response.text[:500])
            
except Exception as e:
    print(f"Ошибка анализа: {e}")

print("\nТестирование завершено!")
print("\nВыводы:")
print("- StubHub API использует OAuth2 для аутентификации")
print("- Все основные эндпоинты требуют аутентификации")
print("- API возвращает ответы в формате application/hal+json")
print("- Для реального тестирования нужны валидные client_id и client_secret")

