import requests
import json

# Тестовый запрос к PredictHQ Events API с фиктивным токеном
# Это покажет нам, как API реагирует на неверный токен

print("=== Тестовый запрос к PredictHQ Events API с фиктивным токеном ===\n")

# Базовый URL API
url = "https://api.predicthq.com/v1/events/"

# Заголовки запроса с фиктивным токеном
headers = {
    "Authorization": "Bearer fake_token_for_testing",
    "Accept": "application/json"
}

# Параметры запроса - поиск концертов в США
params = {
    "category": "concerts",
    "country": "US", 
    "limit": 5
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
    print("✓ API отклонил фиктивный токен (статус 401)")
    print("✓ Требуется валидный Bearer токен от PredictHQ")
elif response.status_code == 403:
    print("✓ API распознал токен, но доступ запрещен (статус 403)")
    print("✓ Возможно, токен недействителен или истек")
elif response.status_code == 200:
    print("✓ Неожиданно: API принял фиктивный токен")
    print("✓ Получены данные о событиях")
else:
    print(f"✓ Получен статус {response.status_code}")
    print("✓ Требуется дополнительное исследование")

# Дополнительный тест - попробуем другие параметры
print("\n" + "="*50)
print("=== Дополнительный тест с другими параметрами ===")

# Попробуем запрос с текстовым поиском
params2 = {
    "q": "taylor swift",
    "limit": 3
}

print(f"Параметры поиска: {params2}")

try:
    response2 = requests.get(url, headers=headers, params=params2)
    print(f"Статус код: {response2.status_code}")
    
    if response2.status_code != 200:
        try:
            error_data = response2.json()
            print(f"Ошибка: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"Текст ошибки: {response2.text}")
    
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")

