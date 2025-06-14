#!/usr/bin/env python3
import requests
import json

# Информация об API, собранная с RapidAPI
url = "https://trawex-car-rental.p.rapidapi.com/test"

headers = {
    "X-RapidAPI-Host": "trawex-car-rental.p.rapidapi.com"
}

print("=== Тестирование Trawex Car Rental API ===")
print(f"URL: {url}")
print(f"Заголовки: {headers}")
print()

try:
    print("Выполняю GET запрос...")
    response = requests.get(url, headers=headers)
    
    print(f"Статус код: {response.status_code}")
    print(f"Заголовки ответа:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nТекст ответа:")
    print(response.text)
    
    # Попробуем распарсить как JSON
    try:
        json_data = response.json()
        print(f"\nJSON ответ (форматированный):")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("\nОтвет не является валидным JSON")
        
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")

print("\n=== Анализ API ===")
print("Этот API требует только один параметр 'CarRental' в пути URL")
print("Заголовок X-RapidAPI-Host обязателен для RapidAPI")
print("Дополнительная авторизация не требуется согласно документации")

