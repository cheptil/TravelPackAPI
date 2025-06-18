import requests
import json
from datetime import datetime

def create_mock_successful_response():
    """Создает имитацию успешного ответа на основе документации API"""
    mock_response = {
        "_links": {
            "self": {
                "href": "/discovery/v2/events.json?size=1&countryCode=US&page=0"
            },
            "next": {
                "href": "/discovery/v2/events.json?size=1&countryCode=US&page=1"
            }
        },
        "_embedded": {
            "events": [
                {
                    "name": "Example Concert",
                    "type": "event",
                    "id": "G5vYZ9p8kZfUb",
                    "test": False,
                    "url": "https://www.ticketmaster.com/example-concert-tickets/event/G5vYZ9p8kZfUb",
                    "locale": "en-us",
                    "images": [
                        {
                            "ratio": "16_9",
                            "url": "https://s1.ticketm.net/dam/a/123/example-image.jpg",
                            "width": 1024,
                            "height": 576,
                            "fallback": False
                        }
                    ],
                    "sales": {
                        "public": {
                            "startDateTime": "2025-01-15T10:00:00Z",
                            "startTBD": False,
                            "endDateTime": "2025-06-20T19:00:00Z"
                        }
                    },
                    "dates": {
                        "start": {
                            "localDate": "2025-06-20",
                            "localTime": "19:00:00",
                            "dateTime": "2025-06-20T19:00:00Z",
                            "dateTBD": False,
                            "dateTBA": False,
                            "timeTBA": False,
                            "noSpecificTime": False
                        },
                        "timezone": "America/New_York",
                        "status": {
                            "code": "onsale"
                        }
                    },
                    "classifications": [
                        {
                            "primary": True,
                            "segment": {
                                "id": "KZFzniwnSyZfZ7v7nJ",
                                "name": "Music"
                            },
                            "genre": {
                                "id": "KnvZfZ7vAeA",
                                "name": "Rock"
                            },
                            "subGenre": {
                                "id": "KZazBEonSMnZiA",
                                "name": "Alternative Rock"
                            }
                        }
                    ],
                    "_embedded": {
                        "venues": [
                            {
                                "name": "Example Arena",
                                "type": "venue",
                                "id": "KovZpZAJdlpA",
                                "test": False,
                                "locale": "en-us",
                                "postalCode": "10001",
                                "timezone": "America/New_York",
                                "city": {
                                    "name": "New York"
                                },
                                "state": {
                                    "name": "New York",
                                    "stateCode": "NY"
                                },
                                "country": {
                                    "name": "United States Of America",
                                    "countryCode": "US"
                                },
                                "address": {
                                    "line1": "123 Example Street"
                                },
                                "location": {
                                    "longitude": "-73.9857",
                                    "latitude": "40.7484"
                                }
                            }
                        ],
                        "attractions": [
                            {
                                "name": "Example Band",
                                "type": "attraction",
                                "id": "K8vZ917G1V0",
                                "test": False,
                                "locale": "en-us",
                                "images": [
                                    {
                                        "ratio": "4_3",
                                        "url": "https://s1.ticketm.net/dam/a/456/example-artist.jpg",
                                        "width": 305,
                                        "height": 225,
                                        "fallback": False
                                    }
                                ],
                                "classifications": [
                                    {
                                        "primary": True,
                                        "segment": {
                                            "id": "KZFzniwnSyZfZ7v7nJ",
                                            "name": "Music"
                                        },
                                        "genre": {
                                            "id": "KnvZfZ7vAeA",
                                            "name": "Rock"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        },
        "page": {
            "size": 1,
            "totalElements": 15432,
            "totalPages": 15432,
            "number": 0
        }
    }
    return mock_response

def analyze_api_structure():
    """Анализирует структуру API на основе документации и тестовых запросов"""
    
    print("=== АНАЛИЗ API TICKETMASTER DISCOVERY ===")
    print(f"Время анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Демонстрация ошибок аутентификации
    print("1. ТЕСТИРОВАНИЕ АУТЕНТИФИКАЦИИ")
    print("-" * 40)
    
    base_url = "https://app.ticketmaster.com/discovery/v2"
    
    # Тест без API ключа
    try:
        response = requests.get(f"{base_url}/events.json", params={'size': 1})
        print(f"Запрос без API ключа:")
        print(f"  Статус: {response.status_code}")
        print(f"  Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"  Ошибка: {e}")
    
    print()
    
    # Тест с неверным API ключом
    try:
        response = requests.get(f"{base_url}/events.json", params={'apikey': 'invalid_key', 'size': 1})
        print(f"Запрос с неверным API ключом:")
        print(f"  Статус: {response.status_code}")
        print(f"  Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"  Ошибка: {e}")
    
    print()
    print("2. ИМИТАЦИЯ УСПЕШНОГО ОТВЕТА")
    print("-" * 40)
    print("На основе документации API, успешный ответ имеет следующую структуру:")
    
    mock_response = create_mock_successful_response()
    print(json.dumps(mock_response, indent=2, ensure_ascii=False))
    
    print()
    print("3. АНАЛИЗ СТРУКТУРЫ ДАННЫХ")
    print("-" * 40)
    
    # Анализ структуры события
    event = mock_response["_embedded"]["events"][0]
    venue = event["_embedded"]["venues"][0]
    attraction = event["_embedded"]["attractions"][0]
    
    print("Основные поля события:")
    print(f"  - ID: {event['id']}")
    print(f"  - Название: {event['name']}")
    print(f"  - URL: {event['url']}")
    print(f"  - Дата: {event['dates']['start']['localDate']} {event['dates']['start']['localTime']}")
    print(f"  - Статус: {event['dates']['status']['code']}")
    print(f"  - Категория: {event['classifications'][0]['segment']['name']} -> {event['classifications'][0]['genre']['name']}")
    
    print()
    print("Информация о площадке:")
    print(f"  - Название: {venue['name']}")
    print(f"  - Город: {venue['city']['name']}, {venue['state']['stateCode']}")
    print(f"  - Адрес: {venue['address']['line1']}")
    print(f"  - Координаты: {venue['location']['latitude']}, {venue['location']['longitude']}")
    
    print()
    print("Информация об исполнителе:")
    print(f"  - Название: {attraction['name']}")
    print(f"  - ID: {attraction['id']}")
    print(f"  - Жанр: {attraction['classifications'][0]['genre']['name']}")
    
    print()
    print("4. ИНФОРМАЦИЯ О ПАГИНАЦИИ")
    print("-" * 40)
    page_info = mock_response["page"]
    print(f"  - Размер страницы: {page_info['size']}")
    print(f"  - Общее количество элементов: {page_info['totalElements']}")
    print(f"  - Общее количество страниц: {page_info['totalPages']}")
    print(f"  - Текущая страница: {page_info['number']}")
    
    print()
    print("5. ССЫЛКИ НА СВЯЗАННЫЕ РЕСУРСЫ")
    print("-" * 40)
    links = mock_response["_links"]
    for link_name, link_data in links.items():
        print(f"  - {link_name}: {link_data['href']}")

if __name__ == "__main__":
    analyze_api_structure()

