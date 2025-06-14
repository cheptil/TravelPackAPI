#!/usr/bin/env python3
"""
Демонстрация примера ответа Sabre Geo Search API
Показывает структуру ответа и методы анализа данных
"""

import json
from datetime import datetime

def create_sample_response():
    """
    Создает пример ответа API на основе документации
    """
    sample_response = {
        "GeoSearchRS": {
            "ApplicationResults": {
                "Success": {
                    "TimeStamp": "2024-06-14T15:17:54.123Z"
                }
            },
            "GeoSearchResults": {
                "Radius": 10,
                "UOM": "KM",
                "Category": "HOTEL",
                "Latitude": 55.7558,
                "Longitude": 37.6176,
                "MaxSearchResults": 50,
                "OffSet": 0,
                "GeoSearchResult": [
                    {
                        "Distance": 1.2,
                        "Direction": "NE",
                        "HotelCode": "100066952",
                        "HotelName": "Москва Отель",
                        "Address": {
                            "Street": "Тверская улица 15",
                            "City": "Москва",
                            "StateProv": "MOW",
                            "CountryCode": "RU",
                            "PostalCode": "125009"
                        },
                        "GeoCode": {
                            "Latitude": 55.7647,
                            "Longitude": 37.6122
                        },
                        "ChainCode": "RT",
                        "ChainName": "Radisson Hotels",
                        "StarRating": 4
                    },
                    {
                        "Distance": 2.8,
                        "Direction": "SW",
                        "HotelCode": "100066953",
                        "HotelName": "Гранд Отель Европа",
                        "Address": {
                            "Street": "Красная площадь 1",
                            "City": "Москва",
                            "StateProv": "MOW",
                            "CountryCode": "RU",
                            "PostalCode": "109012"
                        },
                        "GeoCode": {
                            "Latitude": 55.7539,
                            "Longitude": 37.6208
                        },
                        "ChainCode": "LX",
                        "ChainName": "Luxury Collection",
                        "StarRating": 5
                    },
                    {
                        "Distance": 4.5,
                        "Direction": "N",
                        "HotelCode": "100066954",
                        "HotelName": "Бизнес Отель Центр",
                        "Address": {
                            "Street": "Новый Арбат 26",
                            "City": "Москва",
                            "StateProv": "MOW",
                            "CountryCode": "RU",
                            "PostalCode": "121099"
                        },
                        "GeoCode": {
                            "Latitude": 55.7522,
                            "Longitude": 37.5991
                        },
                        "ChainCode": "HI",
                        "ChainName": "Holiday Inn",
                        "StarRating": 3
                    }
                ]
            }
        }
    }
    
    return sample_response

def analyze_geo_search_response(response_data):
    """
    Подробный анализ ответа Geo Search API
    """
    print("ДЕТАЛЬНЫЙ АНАЛИЗ ОТВЕТА SABRE GEO SEARCH API")
    print("=" * 60)
    
    if not response_data or "GeoSearchRS" not in response_data:
        print("Ошибка: Неверная структура ответа")
        return
    
    geo_search_rs = response_data["GeoSearchRS"]
    
    # 1. Анализ ApplicationResults
    print("\n1. РЕЗУЛЬТАТЫ ПРИЛОЖЕНИЯ:")
    print("-" * 30)
    
    if "ApplicationResults" in geo_search_rs:
        app_results = geo_search_rs["ApplicationResults"]
        
        if "Success" in app_results:
            success = app_results["Success"]
            print(f"✓ Статус: Успешно")
            
            if "TimeStamp" in success:
                timestamp = success["TimeStamp"]
                print(f"✓ Временная метка: {timestamp}")
                
                # Парсинг времени
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    print(f"✓ Время выполнения: {dt.strftime('%d.%m.%Y %H:%M:%S UTC')}")
                except:
                    print(f"✓ Время выполнения: {timestamp}")
        
        if "Error" in app_results:
            error = app_results["Error"]
            print(f"✗ Ошибка: {error}")
    
    # 2. Анализ параметров поиска
    print("\n2. ПАРАМЕТРЫ ПОИСКА:")
    print("-" * 30)
    
    if "GeoSearchResults" in geo_search_rs:
        search_results = geo_search_rs["GeoSearchResults"]
        
        print(f"📍 Центр поиска:")
        print(f"   Широта: {search_results.get('Latitude', 'N/A')}")
        print(f"   Долгота: {search_results.get('Longitude', 'N/A')}")
        
        print(f"🔍 Параметры:")
        print(f"   Радиус: {search_results.get('Radius', 'N/A')} {search_results.get('UOM', 'N/A')}")
        print(f"   Категория: {search_results.get('Category', 'N/A')}")
        print(f"   Макс. результатов: {search_results.get('MaxSearchResults', 'N/A')}")
        print(f"   Смещение: {search_results.get('OffSet', 'N/A')}")
        
        # 3. Анализ найденных результатов
        if "GeoSearchResult" in search_results:
            results = search_results["GeoSearchResult"]
            
            print(f"\n3. НАЙДЕННЫЕ ЛОКАЦИИ:")
            print("-" * 30)
            print(f"📊 Общее количество: {len(results)}")
            
            # Статистика по расстояниям
            distances = [r.get('Distance', 0) for r in results if 'Distance' in r]
            if distances:
                print(f"📏 Расстояния:")
                print(f"   Минимальное: {min(distances)} {search_results.get('UOM', 'KM')}")
                print(f"   Максимальное: {max(distances)} {search_results.get('UOM', 'KM')}")
                print(f"   Среднее: {sum(distances)/len(distances):.1f} {search_results.get('UOM', 'KM')}")
            
            # Статистика по направлениям
            directions = [r.get('Direction', '') for r in results if 'Direction' in r]
            if directions:
                direction_count = {}
                for direction in directions:
                    direction_count[direction] = direction_count.get(direction, 0) + 1
                
                print(f"🧭 Распределение по направлениям:")
                for direction, count in sorted(direction_count.items()):
                    print(f"   {direction}: {count}")
            
            # Детальная информация о каждой локации
            print(f"\n4. ДЕТАЛИ ЛОКАЦИЙ:")
            print("-" * 30)
            
            for i, result in enumerate(results, 1):
                print(f"\n🏨 Локация {i}:")
                
                # Основная информация
                if 'HotelName' in result:
                    print(f"   Название: {result['HotelName']}")
                if 'HotelCode' in result:
                    print(f"   Код отеля: {result['HotelCode']}")
                
                # Расстояние и направление
                distance = result.get('Distance', 'N/A')
                direction = result.get('Direction', 'N/A')
                uom = search_results.get('UOM', 'KM')
                print(f"   Расположение: {distance} {uom} на {direction}")
                
                # Адрес
                if 'Address' in result:
                    address = result['Address']
                    print(f"   Адрес:")
                    if 'Street' in address:
                        print(f"     Улица: {address['Street']}")
                    if 'City' in address:
                        print(f"     Город: {address['City']}")
                    if 'StateProv' in address:
                        print(f"     Регион: {address['StateProv']}")
                    if 'CountryCode' in address:
                        print(f"     Страна: {address['CountryCode']}")
                    if 'PostalCode' in address:
                        print(f"     Индекс: {address['PostalCode']}")
                
                # Координаты
                if 'GeoCode' in result:
                    geocode = result['GeoCode']
                    lat = geocode.get('Latitude', 'N/A')
                    lon = geocode.get('Longitude', 'N/A')
                    print(f"   Координаты: {lat}, {lon}")
                
                # Информация о сети
                if 'ChainName' in result:
                    print(f"   Сеть: {result['ChainName']}")
                if 'ChainCode' in result:
                    print(f"   Код сети: {result['ChainCode']}")
                
                # Рейтинг
                if 'StarRating' in result:
                    stars = "⭐" * result['StarRating']
                    print(f"   Рейтинг: {stars} ({result['StarRating']} звезд)")
                
                # Дополнительные поля
                additional_fields = {k: v for k, v in result.items() 
                                   if k not in ['HotelName', 'HotelCode', 'Distance', 'Direction', 
                                              'Address', 'GeoCode', 'ChainName', 'ChainCode', 'StarRating']}
                
                if additional_fields:
                    print(f"   Дополнительно:")
                    for key, value in additional_fields.items():
                        print(f"     {key}: {value}")
    
    print(f"\n{'=' * 60}")

def demonstrate_different_search_types():
    """
    Демонстрация различных типов поиска
    """
    print("\nПРИМЕРЫ РАЗЛИЧНЫХ ТИПОВ ПОИСКА:")
    print("=" * 50)
    
    search_examples = [
        {
            "name": "Поиск отелей по координатам (Москва)",
            "request": {
                "GeoRef": {
                    "Radius": 10,
                    "UOM": "KM",
                    "Category": "HOTEL",
                    "GeoCode": {
                        "Latitude": 55.7558,
                        "Longitude": 37.6176
                    }
                }
            }
        },
        {
            "name": "Поиск аэропортов по коду города",
            "request": {
                "GeoRef": {
                    "Radius": 50,
                    "UOM": "KM",
                    "Category": "AIR",
                    "AirportCode": "MOW"
                }
            }
        },
        {
            "name": "Поиск мест аренды автомобилей по адресу",
            "request": {
                "GeoRef": {
                    "Radius": 15,
                    "UOM": "MI",
                    "Category": "CAR",
                    "Address": "Red Square, Moscow, Russia"
                }
            }
        },
        {
            "name": "Поиск отелей сети Radisson в радиусе 20 км",
            "request": {
                "GeoRef": {
                    "Radius": 20,
                    "UOM": "KM",
                    "Category": "HOTEL",
                    "GeoCode": {
                        "Latitude": 55.7558,
                        "Longitude": 37.6176
                    },
                    "GeoAttributes": {
                        "Attributes": [
                            {
                                "Name": "CHAIN",
                                "Value": "RT"
                            }
                        ]
                    }
                }
            }
        },
        {
            "name": "Поиск по точке интереса (POI)",
            "request": {
                "GeoRef": {
                    "Radius": 5,
                    "UOM": "KM",
                    "Category": "HOTEL",
                    "POI": "Red Square"
                }
            }
        }
    ]
    
    for i, example in enumerate(search_examples, 1):
        print(f"\n{i}. {example['name']}:")
        print(json.dumps(example['request'], indent=2, ensure_ascii=False))

def main():
    """
    Основная функция демонстрации
    """
    print("ДЕМОНСТРАЦИЯ SABRE GEO SEARCH API")
    print("=" * 50)
    
    # Создаем пример ответа
    sample_response = create_sample_response()
    
    # Показываем JSON структуру ответа
    print("\nПРИМЕР JSON ОТВЕТА:")
    print("-" * 30)
    print(json.dumps(sample_response, indent=2, ensure_ascii=False))
    
    # Анализируем ответ
    analyze_geo_search_response(sample_response)
    
    # Показываем примеры различных типов поиска
    demonstrate_different_search_types()
    
    print(f"\n{'=' * 50}")
    print("ЗАКЛЮЧЕНИЕ:")
    print("- API возвращает структурированные данные о локациях")
    print("- Поддерживает различные типы поиска (координаты, коды, адреса)")
    print("- Предоставляет детальную информацию о каждой найденной локации")
    print("- Позволяет фильтровать результаты по различным критериям")
    print("- Включает расстояние и направление от центра поиска")

if __name__ == "__main__":
    main()

