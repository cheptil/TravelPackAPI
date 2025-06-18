"""
Дополнительные примеры использования Amadeus City Search API

Этот файл содержит:
1. Примеры успешных ответов API
2. Примеры обработки ошибок
3. Утилиты для работы с результатами
4. Рекомендации по использованию
"""

import json
from typing import Dict, List, Any

# Пример успешного ответа API для поиска "PAR"
EXAMPLE_SUCCESS_RESPONSE = {
    "meta": {
        "count": 3,
        "links": {
            "self": "https://test.api.amadeus.com/v1/reference-data/locations/cities?keyword=PAR&max=5&include=AIRPORTS"
        }
    },
    "data": [
        {
            "type": "location",
            "subType": "city",
            "name": "PARIS",
            "iataCode": "PAR",
            "address": {
                "countryCode": "FR"
            },
            "geoCode": {
                "latitude": "48.85341",
                "longitude": "2.3488"
            },
            "relationships": [
                {
                    "id": "CDG",
                    "type": "Airport",
                    "href": "#/included/airports/CDG"
                },
                {
                    "id": "ORY",
                    "type": "Airport", 
                    "href": "#/included/airports/ORY"
                },
                {
                    "id": "BVA",
                    "type": "Airport",
                    "href": "#/included/airports/BVA"
                }
            ]
        },
        {
            "type": "location",
            "subType": "city",
            "name": "PARMA",
            "address": {
                "countryCode": "IT"
            },
            "geoCode": {
                "latitude": "44.80107",
                "longitude": "10.32875"
            }
        },
        {
            "type": "location",
            "subType": "city", 
            "name": "PARADISE",
            "address": {
                "countryCode": "US"
            },
            "geoCode": {
                "latitude": "36.09719",
                "longitude": "-115.14666"
            }
        }
    ],
    "included": {
        "airports": [
            {
                "type": "location",
                "subType": "airport",
                "id": "CDG",
                "name": "CHARLES DE GAULLE",
                "iataCode": "CDG",
                "address": {
                    "countryCode": "FR"
                },
                "geoCode": {
                    "latitude": "49.01278",
                    "longitude": "2.55"
                }
            },
            {
                "type": "location",
                "subType": "airport",
                "id": "ORY",
                "name": "ORLY",
                "iataCode": "ORY",
                "address": {
                    "countryCode": "FR"
                },
                "geoCode": {
                    "latitude": "48.72333",
                    "longitude": "2.37944"
                }
            },
            {
                "type": "location",
                "subType": "airport",
                "id": "BVA",
                "name": "BEAUVAIS TILLE",
                "iataCode": "BVA",
                "address": {
                    "countryCode": "FR"
                },
                "geoCode": {
                    "latitude": "49.45444",
                    "longitude": "2.11278"
                }
            }
        ]
    }
}

# Примеры различных ошибок API
EXAMPLE_ERROR_RESPONSES = {
    "missing_keyword": {
        "errors": [
            {
                "status": 400,
                "code": 32171,
                "title": "MANDATORY DATA MISSING",
                "detail": "Missing mandatory query parameter"
            }
        ]
    },
    "invalid_country_code": {
        "errors": [
            {
                "status": 400,
                "code": 477,
                "title": "INVALID FORMAT",
                "detail": "Invalid country code format"
            }
        ]
    },
    "unauthorized": {
        "errors": [
            {
                "status": 401,
                "code": 38191,
                "title": "Invalid HTTP header",
                "detail": "Missing or invalid format for mandatory Authorization header"
            }
        ]
    },
    "rate_limit": {
        "errors": [
            {
                "status": 429,
                "code": 61,
                "title": "Rate limit exceeded",
                "detail": "You have exceeded the rate limit"
            }
        ]
    }
}

class CitySearchAnalyzer:
    """Утилиты для анализа результатов поиска городов"""
    
    @staticmethod
    def extract_city_info(city_data: Dict[str, Any]) -> Dict[str, Any]:
        """Извлечение основной информации о городе"""
        return {
            "name": city_data.get("name"),
            "country": city_data.get("address", {}).get("countryCode"),
            "iata_code": city_data.get("iataCode"),
            "latitude": city_data.get("geoCode", {}).get("latitude"),
            "longitude": city_data.get("geoCode", {}).get("longitude"),
            "airports": [
                rel.get("id") for rel in city_data.get("relationships", [])
                if rel.get("type") == "Airport"
            ]
        }
    
    @staticmethod
    def group_by_country(cities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Группировка городов по странам"""
        grouped = {}
        for city in cities:
            country = city.get("address", {}).get("countryCode", "Unknown")
            if country not in grouped:
                grouped[country] = []
            grouped[country].append(city)
        return grouped
    
    @staticmethod
    def find_cities_with_airports(cities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Поиск городов с аэропортами"""
        return [
            city for city in cities 
            if city.get("relationships") and 
            any(rel.get("type") == "Airport" for rel in city.get("relationships", []))
        ]
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Вычисление расстояния между двумя точками (упрощенная формула)"""
        import math
        
        # Преобразование в радианы
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Формула гаверсинуса
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Радиус Земли в километрах
        r = 6371
        
        return c * r

def demo_response_analysis():
    """Демонстрация анализа ответов API"""
    print("📊 ДЕМОНСТРАЦИЯ АНАЛИЗА ОТВЕТОВ AMADEUS CITY SEARCH API")
    print("=" * 70)
    
    analyzer = CitySearchAnalyzer()
    
    # Анализ успешного ответа
    print("\n✅ АНАЛИЗ УСПЕШНОГО ОТВЕТА")
    print("-" * 40)
    
    cities = EXAMPLE_SUCCESS_RESPONSE["data"]
    print(f"Всего найдено городов: {len(cities)}")
    
    # Извлечение информации о каждом городе
    print("\nИнформация о городах:")
    for i, city in enumerate(cities, 1):
        info = analyzer.extract_city_info(city)
        print(f"\n{i}. {info['name']}")
        print(f"   Страна: {info['country']}")
        if info['iata_code']:
            print(f"   IATA код: {info['iata_code']}")
        if info['latitude'] and info['longitude']:
            print(f"   Координаты: {info['latitude']}, {info['longitude']}")
        if info['airports']:
            print(f"   Аэропорты: {', '.join(info['airports'])}")
    
    # Группировка по странам
    print("\n🌍 ГРУППИРОВКА ПО СТРАНАМ")
    print("-" * 30)
    grouped = analyzer.group_by_country(cities)
    for country, country_cities in grouped.items():
        print(f"{country}: {len(country_cities)} город(ов)")
        for city in country_cities:
            print(f"  - {city['name']}")
    
    # Города с аэропортами
    print("\n✈️ ГОРОДА С АЭРОПОРТАМИ")
    print("-" * 25)
    cities_with_airports = analyzer.find_cities_with_airports(cities)
    print(f"Найдено {len(cities_with_airports)} город(ов) с аэропортами:")
    for city in cities_with_airports:
        airports = [rel["id"] for rel in city.get("relationships", []) if rel.get("type") == "Airport"]
        print(f"- {city['name']}: {', '.join(airports)}")
    
    # Информация об аэропортах
    if "included" in EXAMPLE_SUCCESS_RESPONSE and "airports" in EXAMPLE_SUCCESS_RESPONSE["included"]:
        print("\n🛫 ИНФОРМАЦИЯ ОБ АЭРОПОРТАХ")
        print("-" * 30)
        airports = EXAMPLE_SUCCESS_RESPONSE["included"]["airports"]
        for airport in airports:
            print(f"\n{airport['name']} ({airport['iataCode']})")
            print(f"  Страна: {airport['address']['countryCode']}")
            print(f"  Координаты: {airport['geoCode']['latitude']}, {airport['geoCode']['longitude']}")
    
    # Анализ ошибок
    print(f"\n\n❌ ПРИМЕРЫ ОБРАБОТКИ ОШИБОК")
    print("-" * 35)
    
    for error_type, error_response in EXAMPLE_ERROR_RESPONSES.items():
        print(f"\n{error_type.upper().replace('_', ' ')}:")
        error = error_response["errors"][0]
        print(f"  Код: {error['code']}")
        print(f"  Статус: {error['status']}")
        print(f"  Заголовок: {error['title']}")
        print(f"  Детали: {error['detail']}")

def usage_recommendations():
    """Рекомендации по использованию API"""
    print("\n\n💡 РЕКОМЕНДАЦИИ ПО ИСПОЛЬЗОВАНИЮ")
    print("=" * 45)
    
    recommendations = [
        {
            "title": "Оптимизация запросов",
            "tips": [
                "Используйте параметр 'max' для ограничения количества результатов",
                "Добавляйте 'countryCode' для более точного поиска",
                "Включайте 'AIRPORTS' только когда нужна информация об аэропортах"
            ]
        },
        {
            "title": "Обработка ошибок",
            "tips": [
                "Всегда проверяйте статус код ответа",
                "Обрабатывайте ошибки авторизации (401)",
                "Учитывайте лимиты запросов (429)",
                "Валидируйте входные параметры перед отправкой"
            ]
        },
        {
            "title": "Управление токенами",
            "tips": [
                "Кешируйте токены до истечения срока действия",
                "Обновляйте токен заранее (за 1-2 минуты до истечения)",
                "Храните API ключи в безопасности",
                "Используйте переменные окружения для ключей"
            ]
        },
        {
            "title": "Производительность",
            "tips": [
                "Используйте пулы соединений для множественных запросов",
                "Добавляйте таймауты к запросам",
                "Реализуйте retry логику для временных ошибок",
                "Кешируйте результаты поиска когда это возможно"
            ]
        }
    ]
    
    for rec in recommendations:
        print(f"\n🔸 {rec['title']}:")
        for tip in rec['tips']:
            print(f"  • {tip}")

def create_usage_examples():
    """Создание примеров использования"""
    print("\n\n📝 ПРИМЕРЫ КОДА ДЛЯ РАЗЛИЧНЫХ СЦЕНАРИЕВ")
    print("=" * 55)
    
    examples = {
        "simple_search": '''
# Простой поиск городов
client = AmadeusClient(api_key, api_secret)
result = client.search_cities("LON", max_results=5)
''',
        
        "country_specific": '''
# Поиск в конкретной стране
result = client.search_cities(
    keyword="BER", 
    country_code="DE", 
    max_results=3
)
''',
        
        "with_airports": '''
# Поиск с информацией об аэропортах
result = client.search_cities(
    keyword="NYC", 
    include_airports=True,
    max_results=5
)
''',
        
        "error_handling": '''
# Обработка ошибок
result = client.search_cities("INVALID")
if not result.get("success"):
    if result.get("status_code") == 401:
        print("Ошибка авторизации")
    elif result.get("status_code") == 400:
        print("Неверные параметры запроса")
    else:
        print(f"Ошибка: {result.get('error')}")
''',
        
        "batch_processing": '''
# Пакетная обработка запросов
keywords = ["PAR", "LON", "NYC", "TOK"]
results = []

for keyword in keywords:
    result = client.search_cities(keyword, max_results=3)
    if result.get("success"):
        results.append(result)
    time.sleep(0.1)  # Пауза между запросами
'''
    }
    
    for name, code in examples.items():
        print(f"\n🔹 {name.replace('_', ' ').title()}:")
        print(code.strip())

if __name__ == "__main__":
    demo_response_analysis()
    usage_recommendations()
    create_usage_examples()
    
    print(f"\n{'='*70}")
    print("✅ Демонстрация анализа завершена!")
    print("\nЭтот файл показывает:")
    print("• Структуру успешных ответов API")
    print("• Различные типы ошибок и их обработку")
    print("• Утилиты для анализа результатов")
    print("• Рекомендации по использованию")
    print("• Примеры кода для различных сценариев")

