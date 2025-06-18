#!/usr/bin/env python3
"""
SeatGeek API Test Script
Тестирование различных endpoints SeatGeek API
"""

import requests
import json
from datetime import datetime

def test_seatgeek_api():
    """Тестирование SeatGeek API"""
    
    base_url = "https://api.seatgeek.com/2"
    
    print("=== Тестирование SeatGeek API ===\n")
    
    # Тест 1: Поиск исполнителей без API ключа
    print("1. Тестирование endpoint /performers без API ключа")
    print("-" * 50)
    
    try:
        url = f"{base_url}/performers"
        params = {"q": "Taylor Swift"}
        
        print(f"URL: {url}")
        print(f"Параметры: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Статус код: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный ответ! Получено {len(data.get('performers', []))} исполнителей")
            print("Первые 2 исполнителя:")
            for i, performer in enumerate(data.get('performers', [])[:2]):
                print(f"  {i+1}. {performer.get('name', 'N/A')} (ID: {performer.get('id', 'N/A')})")
        else:
            print(f"Ошибка: {response.text}")
            
    except Exception as e:
        print(f"Исключение: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 2: Поиск событий без API ключа
    print("2. Тестирование endpoint /events без API ключа")
    print("-" * 50)
    
    try:
        url = f"{base_url}/events"
        params = {"q": "concert", "per_page": 5}
        
        print(f"URL: {url}")
        print(f"Параметры: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный ответ! Получено {len(data.get('events', []))} событий")
            print("Первые 3 события:")
            for i, event in enumerate(data.get('events', [])[:3]):
                print(f"  {i+1}. {event.get('title', 'N/A')} - {event.get('datetime_local', 'N/A')}")
        else:
            print(f"Ошибка: {response.text}")
            
    except Exception as e:
        print(f"Исключение: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 3: Поиск мест проведения без API ключа
    print("3. Тестирование endpoint /venues без API ключа")
    print("-" * 50)
    
    try:
        url = f"{base_url}/venues"
        params = {"q": "Madison Square Garden"}
        
        print(f"URL: {url}")
        print(f"Параметры: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный ответ! Получено {len(data.get('venues', []))} мест")
            print("Первые 2 места:")
            for i, venue in enumerate(data.get('venues', [])[:2]):
                print(f"  {i+1}. {venue.get('name', 'N/A')} - {venue.get('city', 'N/A')}")
        else:
            print(f"Ошибка: {response.text}")
            
    except Exception as e:
        print(f"Исключение: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 4: Детальный анализ одного успешного ответа
    print("4. Детальный анализ структуры ответа")
    print("-" * 50)
    
    try:
        url = f"{base_url}/performers"
        params = {"q": "Beatles", "per_page": 1}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("Полная структура ответа:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Не удалось получить детальный ответ: {response.status_code}")
            
    except Exception as e:
        print(f"Исключение при детальном анализе: {e}")

if __name__ == "__main__":
    test_seatgeek_api()

