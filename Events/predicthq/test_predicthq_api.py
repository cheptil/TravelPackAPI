import requests
import json

# Тестовый запрос к PredictHQ Events API без токена
# Это покажет нам требования к аутентификации и структуру ошибки

print("=== Тестовый запрос к PredictHQ Events API ===\n")

# Базовый URL API
url = "https://api.predicthq.com/v1/events/"

# Заголовки запроса
headers = {
    "Accept": "application/json"
}

# Параметры запроса - поиск концертов в США
params = {
    "category": "concerts",
    "country": "US",
    "limit": 5  # Ограничиваем количество результатов
}

print(f"URL: {url}")
print(f"Параметры: {params}")
print(f"Заголовки: {headers}")
print("\n" + "="*50)

try:
    # Выполняем запрос
    response = requests.get(url, headers=headers, params=params)
    
    print(f"Статус код: {response.status_code}")
    print(f"Заголовки ответа:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nТело ответа:")
    
    # Пытаемся распарсить JSON
    try:
        response_data = response.json()
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Ответ не является валидным JSON:")
        print(response.text)
        
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")

print("\n" + "="*50)
print("Анализ результата:")

if response.status_code == 401:
    print("✓ API требует аутентификации (статус 401)")
    print("✓ Для работы с API необходим Bearer токен")
elif response.status_code == 200:
    print("✓ API доступен без аутентификации")
    print("✓ Получены данные о событиях")
else:
    print(f"✓ Получен статус {response.status_code}")
    print("✓ Требуется дополнительное исследование")

