#!/usr/bin/env python3
"""
Тестовый скрипт для работы с Nominatim API
"""

import requests
import json
import time

def test_nominatim_search():
    """Выполняет тестовый запрос к Nominatim API"""
    
    # Базовый URL для API
    base_url = "https://nominatim.openstreetmap.org/search"
    
    # Параметры запроса
    params = {
        'q': 'Красная площадь, Москва',  # Поиск известного места
        'format': 'json',               # Формат ответа JSON
        'addressdetails': 1,            # Включить детали адреса
        'limit': 5,                     # Ограничить количество результатов
        'extratags': 1,                 # Включить дополнительные теги
        'namedetails': 1,               # Включить детали названий
        'accept-language': 'ru,en'      # Предпочитаемые языки
    }
    
    print("=== Тестовый запрос к Nominatim API ===")
    print(f"URL: {base_url}")
    print(f"Параметры: {params}")
    print()
    
    # Добавляем пользовательский User-Agent (требование API)
    headers = {
        'User-Agent': 'NominatimTestScript/1.0 (educational purpose)'
    }
    
    try:
        # Выполняем запрос
        print("Выполняю запрос...")
        response = requests.get(base_url, params=params, headers=headers)
        
        # Проверяем статус ответа
        print(f"Статус ответа: {response.status_code}")
        print(f"URL запроса: {response.url}")
        print()
        
        if response.status_code == 200:
            # Парсим JSON ответ
            data = response.json()
            
            print(f"Количество найденных результатов: {len(data)}")
            print()
            
            # Выводим информацию о каждом результате
            for i, result in enumerate(data, 1):
                print(f"--- Результат {i} ---")
                print(f"Place ID: {result.get('place_id', 'N/A')}")
                print(f"OSM Type: {result.get('osm_type', 'N/A')}")
                print(f"OSM ID: {result.get('osm_id', 'N/A')}")
                print(f"Display Name: {result.get('display_name', 'N/A')}")
                print(f"Class: {result.get('class', 'N/A')}")
                print(f"Type: {result.get('type', 'N/A')}")
                print(f"Importance: {result.get('importance', 'N/A')}")
                print(f"Latitude: {result.get('lat', 'N/A')}")
                print(f"Longitude: {result.get('lon', 'N/A')}")
                
                # Выводим адресные детали если есть
                if 'address' in result:
                    print("Адресные детали:")
                    for key, value in result['address'].items():
                        print(f"  {key}: {value}")
                
                print()
            
            # Сохраняем полный ответ в файл
            with open('/home/ubuntu/nominatim_response.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("Полный ответ сохранен в файл: nominatim_response.json")
            
        else:
            print(f"Ошибка запроса: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

def test_structured_search():
    """Выполняет тестовый структурированный запрос"""
    
    base_url = "https://nominatim.openstreetmap.org/search"
    
    # Структурированный запрос
    params = {
        'city': 'Moscow',
        'country': 'Russia',
        'format': 'json',
        'addressdetails': 1,
        'limit': 3
    }
    
    print("\n=== Тестовый структурированный запрос ===")
    print(f"Параметры: {params}")
    
    headers = {
        'User-Agent': 'NominatimTestScript/1.0 (educational purpose)'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено результатов: {len(data)}")
            
            for i, result in enumerate(data[:2], 1):  # Показываем только первые 2
                print(f"\n--- Структурированный результат {i} ---")
                print(f"Display Name: {result.get('display_name', 'N/A')}")
                print(f"Type: {result.get('type', 'N/A')}")
                print(f"Coordinates: {result.get('lat', 'N/A')}, {result.get('lon', 'N/A')}")
                
    except Exception as e:
        print(f"Ошибка в структурированном запросе: {e}")

if __name__ == "__main__":
    # Выполняем тесты
    test_nominatim_search()
    
    # Небольшая пауза между запросами (хорошая практика)
    time.sleep(1)
    
    test_structured_search()
    
    print("\n=== Тестирование завершено ===")

