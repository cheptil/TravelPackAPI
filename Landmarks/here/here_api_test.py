#!/usr/bin/env python3
"""
Тестовый скрипт для HERE Geocoder API - поиск достопримечательностей
Демонстрирует структуру запроса и обработку ответа
"""

import requests
import json
from typing import Dict, Any, Optional

class HereGeocoderAPI:
    """Класс для работы с HERE Geocoder API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json"
    
    def search_landmarks(self, latitude: float, longitude: float, radius: int = 1000) -> Optional[Dict[str, Any]]:
        """
        Поиск достопримечательностей вокруг указанной точки
        
        Args:
            latitude: Широта
            longitude: Долгота  
            radius: Радиус поиска в метрах (по умолчанию 1000)
            
        Returns:
            Словарь с результатами или None в случае ошибки
        """
        params = {
            'apiKey': self.api_key,
            'mode': 'retrieveLandmarks',
            'prox': f"{latitude},{longitude},{radius}"
        }
        
        try:
            print(f"Выполняю запрос к HERE Geocoder API...")
            print(f"URL: {self.base_url}")
            print(f"Параметры: {params}")
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
    
    def analyze_response(self, response_data: Dict[str, Any]) -> None:
        """Анализ и вывод результатов ответа API"""
        
        if not response_data:
            print("Нет данных для анализа")
            return
            
        print("\n=== АНАЛИЗ ОТВЕТА HERE GEOCODER API ===")
        
        # Метаинформация
        meta_info = response_data.get('Response', {}).get('MetaInfo', {})
        if meta_info:
            print(f"\nМетаинформация:")
            print(f"  Временная метка: {meta_info.get('Timestamp', 'N/A')}")
            if 'NextPageInformation' in meta_info:
                print(f"  Информация о следующей странице: {meta_info['NextPageInformation']}")
        
        # Результаты
        views = response_data.get('Response', {}).get('View', [])
        if not views:
            print("Результаты не найдены")
            return
            
        view = views[0]
        results = view.get('Result', [])
        
        print(f"\nНайдено результатов: {len(results)}")
        print(f"Тип представления: {view.get('_type', 'N/A')}")
        print(f"ID представления: {view.get('ViewId', 'N/A')}")
        
        # Анализ каждого результата
        for i, result in enumerate(results, 1):
            print(f"\n--- Результат {i} ---")
            print(f"Релевантность: {result.get('Relevance', 'N/A')}")
            print(f"Расстояние: {result.get('Distance', 'N/A')} м")
            print(f"Уровень совпадения: {result.get('MatchLevel', 'N/A')}")
            
            # Информация о локации
            location = result.get('Location', {})
            if location:
                print(f"\nИнформация о локации:")
                print(f"  Название: {location.get('Name', 'N/A')}")
                print(f"  Тип: {location.get('LocationType', 'N/A')}")
                print(f"  ID локации: {location.get('LocationId', 'N/A')}")
                
                # Координаты
                display_pos = location.get('DisplayPosition', {})
                if display_pos:
                    print(f"  Координаты: {display_pos.get('Latitude', 'N/A')}, {display_pos.get('Longitude', 'N/A')}")
                
                # Адрес
                address = location.get('Address', {})
                if address:
                    print(f"  Адрес: {address.get('Label', 'N/A')}")
                    print(f"  Страна: {address.get('Country', 'N/A')}")
                    print(f"  Штат: {address.get('State', 'N/A')}")
                    print(f"  Округ: {address.get('County', 'N/A')}")
                    print(f"  Город: {address.get('City', 'N/A')}")
                    print(f"  Улица: {address.get('Street', 'N/A')}")
                    print(f"  Почтовый код: {address.get('PostalCode', 'N/A')}")

def demo_request():
    """Демонстрация запроса без реального API ключа"""
    
    print("=== ДЕМОНСТРАЦИЯ HERE GEOCODER API ===")
    print("\nВНИМАНИЕ: Для реального использования требуется действующий HERE API Key")
    print("Получить ключ можно на: https://developer.here.com/")
    
    # Параметры из документации
    latitude = 37.7442
    longitude = -119.5931
    radius = 1000
    
    print(f"\nПараметры тестового запроса:")
    print(f"  Широта: {latitude}")
    print(f"  Долгота: {longitude}")
    print(f"  Радиус: {radius} метров")
    print(f"  Локация: Йосемитский национальный парк")
    
    # Создаем экземпляр API с демо-ключом
    api = HereGeocoderAPI("DEMO_API_KEY")
    
    # Формируем URL запроса для демонстрации
    demo_url = f"{api.base_url}?apiKey=YOUR_API_KEY&mode=retrieveLandmarks&prox={latitude},{longitude},{radius}"
    print(f"\nПример URL запроса:")
    print(demo_url)
    
    # Демонстрируем анализ с примером ответа из документации
    demo_response = {
        "Response": {
            "MetaInfo": {
                "Timestamp": "2016-11-07T12:07:13.023+0000",
                "NextPageInformation": "2"
            },
            "View": [{
                "_type": "SearchResultsViewType",
                "ViewId": 0,
                "Result": [
                    {
                        "Relevance": 1,
                        "Distance": -14382.7,
                        "MatchLevel": "landmark",
                        "MatchQuality": {
                            "Country": 1,
                            "State": 1,
                            "County": 1,
                            "City": 1,
                            "Street": [1],
                            "PostalCode": 1,
                            "Name": 1
                        },
                        "Location": {
                            "LocationId": "NT_7U3RMtjyjRsEmGe.YC4S8D_p_Kgfqf4tWl9AGlk04wpQ81B",
                            "LocationType": "park",
                            "Name": "Yosemite National Park",
                            "DisplayPosition": {
                                "Latitude": 37.74896,
                                "Longitude": -119.58851
                            },
                            "MapView": {
                                "TopLeft": {
                                    "Latitude": 38.18491,
                                    "Longitude": -119.88604
                                },
                                "BottomRight": {
                                    "Latitude": 37.49379,
                                    "Longitude": -119.19545
                                }
                            },
                            "Address": {
                                "Label": "Village Dr, Yosemite National Park, CA 95389, United States",
                                "Country": "USA",
                                "State": "CA",
                                "County": "Mariposa",
                                "City": "Yosemite National Park",
                                "Street": "Village Dr",
                                "PostalCode": "95389",
                                "AdditionalData": [
                                    {
                                        "value": "United States",
                                        "key": "CountryName"
                                    },
                                    {
                                        "value": "California",
                                        "key": "StateName"
                                    },
                                    {
                                        "value": "Mariposa",
                                        "key": "CountyName"
                                    },
                                    {
                                        "value": "N",
                                        "key": "PostalCodeType"
                                    }
                                ]
                            },
                            "MapReference": {
                                "CountryId": "21000001",
                                "StateId": "21009408",
                                "CountyId": "21009811",
                                "CityId": "21570523",
                                "PlaceId": "17552007"
                            }
                        }
                    }
                ]
            }]
        }
    }
    
    print("\n=== АНАЛИЗ ПРИМЕРА ОТВЕТА ИЗ ДОКУМЕНТАЦИИ ===")
    api.analyze_response(demo_response)

if __name__ == "__main__":
    demo_request()

