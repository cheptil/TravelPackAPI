#!/usr/bin/env python3
"""
Тестовый скрипт для API Cleveland Museum of Art
Выполняет запрос к эндпоинту /api/artworks с поиском по слову "painting"
"""

import requests
import json
from datetime import datetime

def test_cleveland_api():
    """Выполняет тестовый запрос к API Cleveland Museum of Art"""
    
    # Базовый URL API
    base_url = "https://openaccess-api.clevelandart.org"
    endpoint = "/api/artworks"
    
    # Параметры запроса
    params = {
        "search": "painting",
        "limit": 5,
        "skip": 0
    }
    
    print("=== Тестирование API Cleveland Museum of Art ===")
    print(f"URL: {base_url}{endpoint}")
    print(f"Параметры: {params}")
    print("-" * 50)
    
    try:
        # Выполнение запроса
        response = requests.get(f"{base_url}{endpoint}", params=params)
        
        # Проверка статуса ответа
        print(f"Статус ответа: {response.status_code}")
        print(f"Время ответа: {response.elapsed.total_seconds():.2f} секунд")
        
        if response.status_code == 200:
            # Парсинг JSON ответа
            data = response.json()
            
            # Анализ структуры ответа
            print("\n=== Анализ ответа ===")
            print(f"Тип данных: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Ключи верхнего уровня: {list(data.keys())}")
                
                # Информация о запросе
                if 'info' in data:
                    info = data['info']
                    print(f"\nИнформация о запросе:")
                    print(f"  - Общее количество: {info.get('total', 'N/A')}")
                    print(f"  - Параметры: {info.get('parameters', {})}")
                
                # Данные произведений искусства
                if 'data' in data:
                    artworks = data['data']
                    print(f"\nКоличество возвращенных произведений: {len(artworks)}")
                    
                    # Анализ первого произведения
                    if artworks:
                        first_artwork = artworks[0]
                        print(f"\nПример произведения (первое в списке):")
                        print(f"  - ID: {first_artwork.get('id', 'N/A')}")
                        print(f"  - Номер поступления: {first_artwork.get('accession_number', 'N/A')}")
                        print(f"  - Название: {first_artwork.get('title', 'N/A')}")
                        print(f"  - Художники: {first_artwork.get('artists_tags', 'N/A')}")
                        print(f"  - Культура: {first_artwork.get('culture', 'N/A')}")
                        print(f"  - Техника: {first_artwork.get('technique', 'N/A')}")
                        print(f"  - Дата создания: {first_artwork.get('creation_date', 'N/A')}")
                        print(f"  - Отдел: {first_artwork.get('department', 'N/A')}")
                        print(f"  - Коллекция: {first_artwork.get('collection', 'N/A')}")
                        
                        # Проверка наличия изображений
                        if 'images' in first_artwork and first_artwork['images']:
                            print(f"  - Изображения: Доступны ({len(first_artwork['images'])} шт.)")
                        else:
                            print(f"  - Изображения: Недоступны")
                        
                        print(f"\nВсе доступные поля для первого произведения:")
                        for key in sorted(first_artwork.keys()):
                            value = first_artwork[key]
                            if isinstance(value, (str, int, float, bool)) and value:
                                print(f"  - {key}: {value}")
                            elif isinstance(value, list) and value:
                                print(f"  - {key}: [список из {len(value)} элементов]")
                            elif isinstance(value, dict) and value:
                                print(f"  - {key}: [словарь с ключами: {list(value.keys())}]")
            
            # Сохранение полного ответа в файл
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/home/ubuntu/api_response_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"\nПолный ответ сохранен в файл: {filename}")
            
            return data
            
        else:
            print(f"Ошибка запроса: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None

if __name__ == "__main__":
    result = test_cleveland_api()
    
    if result:
        print("\n=== Тест завершен успешно ===")
    else:
        print("\n=== Тест завершен с ошибкой ===")

