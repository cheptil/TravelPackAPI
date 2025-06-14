import requests
import json

# API endpoint from documentation
base_url = "https://4eea5d2b-607c-48f0-bf61-19ac4e7b4111.mock.pstmn.io/restaurants"

# Test with the example ID from documentation
restaurant_id = "abc1"
url = f"{base_url}/{restaurant_id}"

print(f"Выполняю тестовый запрос к: {url}")
print("-" * 50)

try:
    # Выполняем GET запрос
    response = requests.get(url)
    
    print(f"Статус код: {response.status_code}")
    print(f"Заголовки ответа:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
    
    print(f"\nТело ответа:")
    print("-" * 30)
    
    # Пытаемся распарсить JSON
    try:
        json_data = response.json()
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Ответ не является валидным JSON:")
        print(response.text)
    
    # Сохраняем результат в файл
    with open('/home/ubuntu/api_response.json', 'w', encoding='utf-8') as f:
        if response.headers.get('content-type', '').startswith('application/json'):
            json.dump(response.json(), f, indent=2, ensure_ascii=False)
        else:
            f.write(response.text)
    
    print(f"\nРезультат сохранен в файл: /home/ubuntu/api_response.json")
    
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")

# Попробуем также запрос без ID для получения списка ресторанов
print("\n" + "="*60)
print("Пробуем запрос для получения списка ресторанов:")
print("="*60)

try:
    list_url = base_url
    print(f"Выполняю запрос к: {list_url}")
    
    response = requests.get(list_url)
    print(f"Статус код: {response.status_code}")
    
    if response.status_code == 200:
        try:
            json_data = response.json()
            print("Список ресторанов:")
            print(json.dumps(json_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Ответ:")
            print(response.text)
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")

