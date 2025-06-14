#!/usr/bin/env python3
"""
Тестовый скрипт для исследования API Avis без аутентификации
Проверяем доступные endpoints и их ответы
"""

import requests
import json

# Конфигурация API
BASE_URL = "https://stage.abgapiservices.com"
LOCATIONS_ENDPOINT = f"{BASE_URL}/cars/locations/v1/"

def test_endpoint_without_auth():
    """
    Тестирование endpoint без аутентификации
    """
    print("🔍 Тестирование API без аутентификации...")
    
    # Параметры запроса
    params = {
        'country_code': 'US',
        'brand': 'Avis',
        'keyword': 'Denver'
    }
    
    try:
        print(f"📍 Запрос к: {LOCATIONS_ENDPOINT}")
        print(f"📋 Параметры: {params}")
        
        response = requests.get(LOCATIONS_ENDPOINT, params=params)
        print(f"📡 Статус ответа: {response.status_code}")
        print(f"📄 Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            print(f"📝 Тело ответа: {response.text}")
            
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                print("⚠️ Ответ не является валидным JSON")
                return response.text
        else:
            print("📭 Пустой ответ")
            return None
            
    except Exception as e:
        print(f"❌ Исключение при запросе: {e}")
        return None

def test_base_url():
    """
    Тестирование базового URL
    """
    print("\n🌐 Тестирование базового URL...")
    
    try:
        response = requests.get(BASE_URL)
        print(f"📡 Статус ответа: {response.status_code}")
        print(f"📄 Заголовки ответа: {dict(response.headers)}")
        
        if response.text:
            print(f"📝 Тело ответа (первые 500 символов): {response.text[:500]}")
        
    except Exception as e:
        print(f"❌ Исключение при запросе к базовому URL: {e}")

def test_oauth_endpoint():
    """
    Тестирование OAuth endpoint без учетных данных
    """
    print("\n🔐 Тестирование OAuth endpoint...")
    
    oauth_url = f"{BASE_URL}/oauth/token/v1"
    
    try:
        response = requests.get(oauth_url)
        print(f"📡 Статус ответа: {response.status_code}")
        
        if response.text:
            print(f"📝 Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Исключение при запросе к OAuth: {e}")

def explore_api_structure():
    """
    Исследование структуры API
    """
    print("\n🔬 Исследование структуры API...")
    
    # Список возможных endpoints для тестирования
    endpoints_to_test = [
        "/cars/locations/v1/",
        "/cars/availability/v1/",
        "/cars/reservation/v1/",
        "/cars/terms_and_conditions/v1/",
        "/cars/",
        "/api/",
        "/docs/",
        "/swagger/",
        "/openapi/"
    ]
    
    for endpoint in endpoints_to_test:
        url = f"{BASE_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            print(f"📍 {endpoint}: {response.status_code}")
            
            if response.status_code not in [404, 500]:
                print(f"   📄 Content-Type: {response.headers.get('content-type', 'неизвестно')}")
                if response.text and len(response.text) < 200:
                    print(f"   📝 Ответ: {response.text}")
                    
        except Exception as e:
            print(f"📍 {endpoint}: ❌ {e}")

def main():
    """
    Основная функция
    """
    print("🔍 Исследование API Avis без аутентификации")
    print("=" * 60)
    
    # Тестируем базовый URL
    test_base_url()
    
    # Тестируем OAuth endpoint
    test_oauth_endpoint()
    
    # Тестируем основной endpoint без аутентификации
    result = test_endpoint_without_auth()
    
    # Исследуем структуру API
    explore_api_structure()
    
    # Сохраняем результат
    if result:
        with open('/home/ubuntu/api_test_result.json', 'w', encoding='utf-8') as f:
            if isinstance(result, dict):
                json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                f.write(str(result))
        print("\n💾 Результат сохранен в api_test_result.json")
    
    print("\n" + "=" * 60)
    print("✅ Исследование завершено")

if __name__ == "__main__":
    main()

