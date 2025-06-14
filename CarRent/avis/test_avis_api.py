#!/usr/bin/env python3
"""
Тестовый скрипт для работы с API Avis
Выполняет получение access token и тестовый запрос к Car Locations API
"""

import requests
import json
import time

# Конфигурация API
BASE_URL = "https://stage.abgapiservices.com"
TOKEN_ENDPOINT = f"{BASE_URL}/oauth/token/v1"
LOCATIONS_ENDPOINT = f"{BASE_URL}/cars/locations/v1/"

# Тестовые учетные данные из документации
CLIENT_ID = "7bc7af29041645fe80aa5d16e71876e5"
CLIENT_SECRET = "7bc7af29041645fe80aa5d16e71876e5"

def get_access_token():
    """
    Получение access token для аутентификации
    """
    print("🔑 Получение access token...")
    
    headers = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    try:
        response = requests.get(TOKEN_ENDPOINT, headers=headers)
        print(f"📡 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Access token успешно получен")
            print(f"🕒 Срок действия: {token_data.get('expires_in', 'неизвестно')} секунд")
            return token_data.get('access_token')
        else:
            print("❌ Ошибка при получении токена:")
            print(f"Статус: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Исключение при получении токена: {e}")
        return None

def test_car_locations_api(access_token):
    """
    Тестовый запрос к Car Locations API
    """
    print("\n🚗 Тестирование Car Locations API...")
    
    # Параметры запроса
    params = {
        'country_code': 'US',
        'brand': 'Avis',
        'keyword': 'Denver'
    }
    
    headers = {
        'client_id': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        print(f"📍 Поиск локаций Avis в Denver, США...")
        response = requests.get(LOCATIONS_ENDPOINT, headers=headers, params=params)
        print(f"📡 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            locations_data = response.json()
            print("✅ Данные успешно получены")
            return locations_data
        else:
            print("❌ Ошибка при запросе локаций:")
            print(f"Статус: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Исключение при запросе локаций: {e}")
        return None

def analyze_response(data):
    """
    Анализ полученных данных
    """
    print("\n📊 Анализ полученных данных:")
    
    if not data:
        print("❌ Нет данных для анализа")
        return
    
    print(f"📄 Тип данных: {type(data)}")
    
    if isinstance(data, dict):
        print(f"🔑 Ключи в ответе: {list(data.keys())}")
        
        # Проверяем наличие локаций
        if 'locations' in data:
            locations = data['locations']
            print(f"📍 Количество найденных локаций: {len(locations)}")
            
            if locations:
                print("\n🏢 Первая локация:")
                first_location = locations[0]
                for key, value in first_location.items():
                    print(f"  {key}: {value}")
        
        # Проверяем наличие статуса
        if 'status' in data:
            status = data['status']
            print(f"\n📋 Статус запроса: {status}")
    
    # Сохраняем полный ответ в файл
    with open('/home/ubuntu/api_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("💾 Полный ответ сохранен в api_response.json")

def main():
    """
    Основная функция
    """
    print("🚀 Начинаем тестирование API Avis")
    print("=" * 50)
    
    # Получаем access token
    access_token = get_access_token()
    
    if not access_token:
        print("❌ Не удалось получить access token. Завершение.")
        return
    
    # Тестируем Car Locations API
    locations_data = test_car_locations_api(access_token)
    
    # Анализируем результат
    analyze_response(locations_data)
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено")

if __name__ == "__main__":
    main()

