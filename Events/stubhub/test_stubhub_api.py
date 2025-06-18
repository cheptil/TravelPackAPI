import requests
import json
import base64

# Тестирование StubHub API

print("=== Тестирование StubHub API ===\n")

# 1. Попробуем сделать запрос без аутентификации к sandbox API
sandbox_base_url = "https://sandbox.api.stubhub.net"

print("1. Тестовый запрос без аутентификации:")
try:
    response = requests.get(f"{sandbox_base_url}/")
    print(f"Статус: {response.status_code}")
    print(f"Заголовки ответа: {dict(response.headers)}")
    print(f"Тело ответа: {response.text[:500]}...")
except Exception as e:
    print(f"Ошибка: {e}")

print("\n" + "="*50 + "\n")

# 2. Попробуем запрос к эндпоинту событий без аутентификации
print("2. Тестовый запрос к эндпоинту событий без аутентификации:")
try:
    response = requests.get(f"{sandbox_base_url}/events")
    print(f"Статус: {response.status_code}")
    print(f"Заголовки ответа: {dict(response.headers)}")
    print(f"Тело ответа: {response.text[:500]}...")
except Exception as e:
    print(f"Ошибка: {e}")

print("\n" + "="*50 + "\n")

# 3. Попробуем запрос к эндпоинту поиска событий
print("3. Тестовый запрос к эндпоинту поиска событий:")
try:
    response = requests.get(f"{sandbox_base_url}/search/events")
    print(f"Статус: {response.status_code}")
    print(f"Заголовки ответа: {dict(response.headers)}")
    print(f"Тело ответа: {response.text[:500]}...")
except Exception as e:
    print(f"Ошибка: {e}")

print("\n" + "="*50 + "\n")

# 4. Тестируем OAuth endpoint для получения токена (без реальных credentials)
print("4. Тестирование OAuth endpoint:")
oauth_url = "https://sandbox.account.stubhub.com/oauth2/token"

# Создаем фиктивные credentials для демонстрации процесса
fake_client_id = "test_client_id"
fake_client_secret = "test_client_secret"

# Создаем Basic Auth header
credentials = f"{fake_client_id}:{fake_client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "client_credentials",
    "scope": "read:events"
}

try:
    response = requests.post(oauth_url, headers=headers, data=data)
    print(f"Статус: {response.status_code}")
    print(f"Заголовки ответа: {dict(response.headers)}")
    print(f"Тело ответа: {response.text}")
except Exception as e:
    print(f"Ошибка: {e}")

print("\n" + "="*50 + "\n")

# 5. Попробуем различные эндпоинты для поиска публичных
print("5. Тестирование различных эндпоинтов:")
endpoints_to_test = [
    "/",
    "/events",
    "/search/events",
    "/venues",
    "/categories",
    "/health",
    "/status",
    "/api",
    "/v1",
    "/v2",
    "/v3"
]

for endpoint in endpoints_to_test:
    try:
        response = requests.get(f"{sandbox_base_url}{endpoint}")
        print(f"GET {endpoint}: {response.status_code}")
        if response.status_code != 404:
            print(f"  Ответ: {response.text[:100]}...")
    except Exception as e:
        print(f"GET {endpoint}: Ошибка - {e}")

print("\nТестирование завершено!")

