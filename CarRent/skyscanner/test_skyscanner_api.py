#!/usr/bin/env python3
"""
Тестовый скрипт для Skyscanner Car Hire Autosuggest API
"""

import requests
import json

def test_skyscanner_carhire_autosuggest():
    """
    Тестирует Skyscanner Car Hire Autosuggest API
    """
    
    # URL эндпоинта
    url = "https://partners.api.skyscanner.net/apiservices/v3/autosuggest/carhire"
    
    # Заголовки запроса
    headers = {
        "Content-Type": "application/json",
        # Здесь должен быть ваш API ключ
        "X-API-Key": "YOUR_API_KEY_HERE"
    }
    
    # Тестовые данные для запроса
    test_cases = [
        {
            "name": "Поиск по 'Lond' (London)",
            "data": {
                "query": {
                    "market": "UK",
                    "locale": "en-GB", 
                    "searchTerm": "Lond"
                }
            }
        },
        {
            "name": "Поиск по 'Pari' (Paris)",
            "data": {
                "query": {
                    "market": "UK",
                    "locale": "en-GB",
                    "searchTerm": "Pari"
                }
            }
        },
        {
            "name": "Популярные места (пустой searchTerm)",
            "data": {
                "query": {
                    "market": "UK",
                    "locale": "en-GB",
                    "searchTerm": ""
                }
            }
        },
        {
            "name": "Поиск с русской локалью",
            "data": {
                "query": {
                    "market": "RU",
                    "locale": "ru-RU",
                    "searchTerm": "Моск"
                }
            }
        }
    ]
    
    print("=== Тестирование Skyscanner Car Hire Autosuggest API ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Тест {i}: {test_case['name']}")
        print(f"URL: {url}")
        print(f"Метод: POST")
        print(f"Заголовки: {json.dumps(headers, indent=2, ensure_ascii=False)}")
        print(f"Тело запроса: {json.dumps(test_case['data'], indent=2, ensure_ascii=False)}")
        
        try:
            # Выполняем запрос
            response = requests.post(url, headers=headers, json=test_case['data'])
            
            print(f"Статус ответа: {response.status_code}")
            print(f"Заголовки ответа: {dict(response.headers)}")
            
            if response.status_code == 200:
                response_data = response.json()
                print("Успешный ответ!")
                print(f"Количество найденных мест: {len(response_data.get('places', []))}")
                
                # Выводим первые несколько результатов
                places = response_data.get('places', [])
                for j, place in enumerate(places[:3]):
                    print(f"  Место {j+1}:")
                    print(f"    Название: {place.get('name', 'N/A')}")
                    print(f"    Тип: {place.get('type', 'N/A')}")
                    print(f"    Координаты: {place.get('location', 'N/A')}")
                    print(f"    Иерархия: {place.get('hierarchy', 'N/A')}")
                    print(f"    Entity ID: {place.get('entityId', 'N/A')}")
                    if 'highlight' in place:
                        print(f"    Выделение: {place['highlight']}")
                    print()
                
                # Сохраняем полный ответ в файл
                filename = f"skyscanner_response_test_{i}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(response_data, f, indent=2, ensure_ascii=False)
                print(f"Полный ответ сохранен в файл: {filename}")
                
            elif response.status_code == 401:
                print("Ошибка авторизации: Необходим действительный API ключ")
                print("Получите API ключ на https://developers.skyscanner.net/")
                
            else:
                print(f"Ошибка: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Детали ошибки: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"Текст ошибки: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            
        print("-" * 80)
        print()

def analyze_response_structure():
    """
    Анализирует структуру ожидаемого ответа
    """
    print("=== Анализ структуры ответа ===\n")
    
    expected_structure = {
        "places": [
            {
                "name": "Название места (например, 'London')",
                "type": "Тип места (PLACE_TYPE_CITY, PLACE_TYPE_AIRPORT, и т.д.)",
                "entityId": "Уникальный внутренний ID",
                "location": "Координаты в формате 'широта,долгота'",
                "hierarchy": "Иерархия мест",
                "highlight": {
                    "description": "Объект для выделения совпадающих символов"
                }
            }
        ]
    }
    
    print("Ожидаемая структура ответа:")
    print(json.dumps(expected_structure, indent=2, ensure_ascii=False))
    print()
    
    print("Возможные типы мест:")
    place_types = [
        "PLACE_TYPE_UNSPECIFIED",
        "PLACE_TYPE_TRAIN_STATION", 
        "PLACE_TYPE_DISTRICT",
        "PLACE_TYPE_AIRPORT",
        "PLACE_TYPE_CITY"
    ]
    
    for place_type in place_types:
        print(f"  - {place_type}")
    print()

if __name__ == "__main__":
    print("ВНИМАНИЕ: Для выполнения реальных запросов необходим API ключ от Skyscanner!")
    print("Получите его на https://developers.skyscanner.net/\n")
    
    analyze_response_structure()
    
    # Раскомментируйте следующую строку после получения API ключа
    # test_skyscanner_carhire_autosuggest()
    
    print("Скрипт готов к использованию после добавления API ключа.")

