#!/usr/bin/env python3
import requests
import json

print("=== Дополнительное тестирование с API ключом ===")

# Попробуем с фиктивным API ключом
url = "https://trawex-car-rental.p.rapidapi.com/test"
headers = {
    "X-RapidAPI-Host": "trawex-car-rental.p.rapidapi.com",
    "X-RapidAPI-Key": "fake-key-for-testing"
}

print(f"URL: {url}")
print(f"Заголовки: {headers}")
print()

try:
    print("Выполняю GET запрос с фиктивным API ключом...")
    response = requests.get(url, headers=headers)
    
    print(f"Статус код: {response.status_code}")
    print(f"Текст ответа:")
    print(response.text)
    
    try:
        json_data = response.json()
        print(f"\nJSON ответ (форматированный):")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("\nОтвет не является валидным JSON")
        
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")

print("\n" + "="*50)
print("Тестирование с другими параметрами пути")
print("="*50)

# Попробуем разные значения параметра CarRental
test_params = ["cars", "rental", "search", "booking", "vehicles"]

for param in test_params:
    test_url = f"https://trawex-car-rental.p.rapidapi.com/{param}"
    print(f"\nТестирую URL: {test_url}")
    
    try:
        response = requests.get(test_url, headers=headers)
        print(f"Статус код: {response.status_code}")
        if response.text:
            print(f"Ответ: {response.text[:200]}...")  # Первые 200 символов
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")

