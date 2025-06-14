#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Strapi REST API
"""

import requests
import json

# Базовый URL для API
BASE_URL = "http://localhost:1337/api"

def test_restaurants_api():
    """Тестирует API ресторанов"""
    
    print("=== Тестирование Strapi REST API ===\n")
    
    # Тест 1: Получение списка всех ресторанов
    print("1. Получение списка всех ресторанов:")
    try:
        response = requests.get(f"{BASE_URL}/restaurants")
        print(f"   Статус: {response.status_code}")
        print(f"   URL: {response.url}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # Сохраняем ID первого ресторана для следующего теста
            if data.get('data') and len(data['data']) > 0:
                restaurant_id = data['data'][0]['id']
                print(f"   Найден ресторан с ID: {restaurant_id}")
                
                # Тест 2: Получение конкретного ресторана
                print(f"\n2. Получение ресторана с ID {restaurant_id}:")
                response2 = requests.get(f"{BASE_URL}/restaurants/{restaurant_id}")
                print(f"   Статус: {response2.status_code}")
                print(f"   URL: {response2.url}")
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    print(f"   Ответ: {json.dumps(data2, indent=2, ensure_ascii=False)}")
                else:
                    print(f"   Ошибка: {response2.text}")
            else:
                print("   Нет данных для тестирования отдельного ресторана")
        else:
            print(f"   Ошибка: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"   Ошибка соединения: {e}")
    
    print("\n=== Тестирование завершено ===")

if __name__ == "__main__":
    test_restaurants_api()

