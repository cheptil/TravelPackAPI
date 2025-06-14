#!/usr/bin/env python3
"""
Симуляция ответа Skyscanner Car Hire Autosuggest API для демонстрации
"""

import json

def simulate_api_response():
    """
    Создает симулированный ответ API для демонстрации структуры данных
    """
    
    # Симулированный ответ для поиска "Lond"
    simulated_response_london = {
        "places": [
            {
                "name": "London",
                "type": "PLACE_TYPE_CITY",
                "entityId": "27544008",
                "location": "51.5074, -0.1278",
                "hierarchy": "United Kingdom > England > London",
                "highlight": {
                    "name": [
                        {"start": 0, "end": 4}  # Выделение "Lond" в "London"
                    ]
                }
            },
            {
                "name": "London Heathrow Airport",
                "type": "PLACE_TYPE_AIRPORT",
                "entityId": "27539793",
                "location": "51.4700, -0.4543",
                "hierarchy": "United Kingdom > England > London > London Heathrow Airport",
                "highlight": {
                    "name": [
                        {"start": 0, "end": 4}  # Выделение "Lond" в "London"
                    ]
                }
            },
            {
                "name": "London Gatwick Airport",
                "type": "PLACE_TYPE_AIRPORT", 
                "entityId": "27539794",
                "location": "51.1481, -0.1903",
                "hierarchy": "United Kingdom > England > London > London Gatwick Airport",
                "highlight": {
                    "name": [
                        {"start": 0, "end": 4}  # Выделение "Lond" в "London"
                    ]
                }
            },
            {
                "name": "London Stansted Airport",
                "type": "PLACE_TYPE_AIRPORT",
                "entityId": "27539795",
                "location": "51.8860, 0.2389",
                "hierarchy": "United Kingdom > England > London > London Stansted Airport",
                "highlight": {
                    "name": [
                        {"start": 0, "end": 4}  # Выделение "Lond" в "London"
                    ]
                }
            },
            {
                "name": "London Bridge",
                "type": "PLACE_TYPE_DISTRICT",
                "entityId": "27544009",
                "location": "51.5045, -0.0865",
                "hierarchy": "United Kingdom > England > London > London Bridge",
                "highlight": {
                    "name": [
                        {"start": 0, "end": 4}  # Выделение "Lond" в "London"
                    ]
                }
            }
        ]
    }
    
    # Симулированный ответ для популярных мест (пустой searchTerm)
    simulated_response_popular = {
        "places": [
            {
                "name": "London",
                "type": "PLACE_TYPE_CITY",
                "entityId": "27544008",
                "location": "51.5074, -0.1278",
                "hierarchy": "United Kingdom > England > London"
            },
            {
                "name": "Manchester",
                "type": "PLACE_TYPE_CITY",
                "entityId": "27544010",
                "location": "53.4808, -2.2426",
                "hierarchy": "United Kingdom > England > Manchester"
            },
            {
                "name": "Birmingham",
                "type": "PLACE_TYPE_CITY",
                "entityId": "27544011",
                "location": "52.4862, -1.8904",
                "hierarchy": "United Kingdom > England > Birmingham"
            },
            {
                "name": "Edinburgh",
                "type": "PLACE_TYPE_CITY",
                "entityId": "27544012",
                "location": "55.9533, -3.1883",
                "hierarchy": "United Kingdom > Scotland > Edinburgh"
            },
            {
                "name": "Glasgow",
                "type": "PLACE_TYPE_CITY",
                "entityId": "27544013",
                "location": "55.8642, -4.2518",
                "hierarchy": "United Kingdom > Scotland > Glasgow"
            }
        ]
    }
    
    return simulated_response_london, simulated_response_popular

def analyze_simulated_response():
    """
    Анализирует симулированный ответ API
    """
    print("=== Анализ симулированного ответа Skyscanner Car Hire Autosuggest API ===\n")
    
    london_response, popular_response = simulate_api_response()
    
    # Анализ ответа для поиска "Lond"
    print("1. Ответ для поиска 'Lond':")
    print(f"   Количество найденных мест: {len(london_response['places'])}")
    print("   Найденные места:")
    
    for i, place in enumerate(london_response['places'], 1):
        print(f"   {i}. {place['name']}")
        print(f"      Тип: {place['type']}")
        print(f"      Координаты: {place['location']}")
        print(f"      Иерархия: {place['hierarchy']}")
        if 'highlight' in place:
            print(f"      Выделение: символы {place['highlight']['name'][0]['start']}-{place['highlight']['name'][0]['end']}")
        print()
    
    # Сохранение в файл
    with open('/home/ubuntu/simulated_response_london.json', 'w', encoding='utf-8') as f:
        json.dump(london_response, f, indent=2, ensure_ascii=False)
    
    print("2. Ответ для популярных мест (пустой searchTerm):")
    print(f"   Количество популярных мест: {len(popular_response['places'])}")
    print("   Популярные места:")
    
    for i, place in enumerate(popular_response['places'], 1):
        print(f"   {i}. {place['name']}")
        print(f"      Тип: {place['type']}")
        print(f"      Координаты: {place['location']}")
        print(f"      Иерархия: {place['hierarchy']}")
        print()
    
    # Сохранение в файл
    with open('/home/ubuntu/simulated_response_popular.json', 'w', encoding='utf-8') as f:
        json.dump(popular_response, f, indent=2, ensure_ascii=False)
    
    print("Симулированные ответы сохранены в файлы:")
    print("- simulated_response_london.json")
    print("- simulated_response_popular.json")
    
    # Анализ типов мест
    print("\n3. Анализ типов мест в ответах:")
    all_places = london_response['places'] + popular_response['places']
    place_types = {}
    
    for place in all_places:
        place_type = place['type']
        if place_type not in place_types:
            place_types[place_type] = []
        place_types[place_type].append(place['name'])
    
    for place_type, places in place_types.items():
        print(f"   {place_type}: {len(places)} мест")
        for place_name in places[:3]:  # Показываем первые 3
            print(f"     - {place_name}")
        if len(places) > 3:
            print(f"     ... и еще {len(places) - 3}")
        print()
    
    # Анализ структуры highlight
    print("4. Анализ функции выделения (highlight):")
    highlighted_places = [p for p in london_response['places'] if 'highlight' in p]
    print(f"   Мест с выделением: {len(highlighted_places)}")
    
    if highlighted_places:
        example = highlighted_places[0]
        print(f"   Пример: '{example['name']}'")
        highlight = example['highlight']['name'][0]
        highlighted_text = example['name'][highlight['start']:highlight['end']]
        print(f"   Выделенный текст: '{highlighted_text}' (позиции {highlight['start']}-{highlight['end']})")

if __name__ == "__main__":
    analyze_simulated_response()

