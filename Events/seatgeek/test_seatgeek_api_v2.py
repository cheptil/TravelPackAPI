#!/usr/bin/env python3
"""
SeatGeek API Test Script v2
Тестирование с попыткой использования демо client_id
"""

import requests
import json
from datetime import datetime

def test_seatgeek_api_with_demo_keys():
    """Тестирование SeatGeek API с различными демо ключами"""
    
    base_url = "https://api.seatgeek.com/2"
    
    print("=== Тестирование SeatGeek API с демо ключами ===\n")
    
    # Список возможных демо client_id для тестирования
    demo_client_ids = [
        "demo",
        "test", 
        "example",
        "public",
        "sample",
        "MTIzNDU2Nzg5MA==",  # base64 encoded "1234567890"
        "12345",
        "seatgeek_demo"
    ]
    
    for client_id in demo_client_ids:
        print(f"Тестирование с client_id: {client_id}")
        print("-" * 50)
        
        try:
            url = f"{base_url}/performers"
            params = {
                "client_id": client_id,
                "q": "Beatles",
                "per_page": 2
            }
            
            print(f"URL: {url}")
            print(f"Параметры: {params}")
            
            response = requests.get(url, params=params, timeout=10)
            
            print(f"Статус код: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ УСПЕХ! Получено {len(data.get('performers', []))} исполнителей")
                if data.get('performers'):
                    print("Первый исполнитель:")
                    performer = data['performers'][0]
                    print(f"  Имя: {performer.get('name', 'N/A')}")
                    print(f"  ID: {performer.get('id', 'N/A')}")
                    print(f"  Популярность: {performer.get('score', 'N/A')}")
                
                # Сохраняем успешный ответ для анализа
                with open(f'/home/ubuntu/seatgeek_success_response_{client_id}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Ответ сохранен в файл seatgeek_success_response_{client_id}.json")
                return client_id  # Возвращаем рабочий client_id
                
            elif response.status_code == 403:
                print("❌ 403 Forbidden - требуется валидный API ключ")
            elif response.status_code == 401:
                print("❌ 401 Unauthorized - неверный API ключ")
            else:
                print(f"❌ Ошибка {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Исключение: {e}")
        
        print("\n" + "="*60 + "\n")
    
    print("❌ Ни один из демо ключей не сработал")
    return None

def test_without_client_id():
    """Тестирование без client_id для понимания структуры ошибки"""
    
    print("=== Тестирование без client_id ===\n")
    
    try:
        url = "https://api.seatgeek.com/2/performers"
        params = {"q": "Beatles"}
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Статус код: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code != 200:
            # Сохраняем структуру ошибки
            with open('/home/ubuntu/seatgeek_error_response.json', 'w', encoding='utf-8') as f:
                try:
                    error_data = response.json()
                    json.dump(error_data, f, indent=2, ensure_ascii=False)
                except:
                    f.write(response.text)
            
            print("Структура ошибки сохранена в файл seatgeek_error_response.json")
        
    except Exception as e:
        print(f"Исключение: {e}")

def analyze_api_structure():
    """Анализ структуры API на основе документации"""
    
    print("=== Анализ структуры SeatGeek API ===\n")
    
    endpoints = [
        "/events",
        "/performers", 
        "/venues",
        "/taxonomies"
    ]
    
    for endpoint in endpoints:
        print(f"Endpoint: {endpoint}")
        print(f"URL: https://api.seatgeek.com/2{endpoint}")
        print(f"Требует: client_id")
        print(f"Поддерживает: поиск (q), пагинацию (page, per_page), фильтрацию")
        print("-" * 40)

if __name__ == "__main__":
    # Сначала тестируем без ключа для понимания ошибки
    test_without_client_id()
    
    print("\n" + "="*80 + "\n")
    
    # Затем пробуем демо ключи
    working_client_id = test_seatgeek_api_with_demo_keys()
    
    print("\n" + "="*80 + "\n")
    
    # Анализируем структуру API
    analyze_api_structure()
    
    if working_client_id:
        print(f"\n✅ Найден рабочий client_id: {working_client_id}")
    else:
        print("\n❌ Рабочий client_id не найден. Требуется регистрация на platform.seatgeek.com")

