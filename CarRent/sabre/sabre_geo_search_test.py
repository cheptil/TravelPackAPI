#!/usr/bin/env python3
"""
Тестовый скрипт для Sabre Geo Search API
Демонстрирует структуру запроса и обработку ответа
"""

import requests
import json
import base64
from datetime import datetime

class SabreGeoSearchAPI:
    def __init__(self):
        # Тестовые URL endpoints
        self.auth_url = "https://api.cert.platform.sabre.com/v3/auth/token"
        self.geo_search_url = "https://api.cert.platform.sabre.com/v2/geo/search"
        
        # Заголовки для запросов
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        self.access_token = None
    
    def get_access_token(self, client_id, client_secret, username, password):
        """
        Получение токена доступа для аутентификации
        """
        # Кодирование client_id:client_secret в base64
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        auth_headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        auth_data = {
            "grant_type": "password",
            "username": username,
            "password": password
        }
        
        try:
            print("Попытка получения токена доступа...")
            response = requests.post(self.auth_url, headers=auth_headers, data=auth_data)
            
            print(f"Статус ответа аутентификации: {response.status_code}")
            print(f"Заголовки ответа: {dict(response.headers)}")
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                print(f"Токен получен успешно: {self.access_token[:20]}...")
                return True
            else:
                print(f"Ошибка получения токена: {response.text}")
                return False
                
        except Exception as e:
            print(f"Исключение при получении токена: {e}")
            return False
    
    def search_by_coordinates(self, latitude, longitude, radius=10, category="HOTEL", uom="KM"):
        """
        Поиск по географическим координатам
        """
        request_data = {
            "GeoRef": {
                "Radius": radius,
                "UOM": uom,
                "Category": category,
                "GeoCode": {
                    "Latitude": latitude,
                    "Longitude": longitude
                }
            }
        }
        
        return self._make_request(request_data, "координатам")
    
    def search_by_airport_code(self, airport_code, radius=10, category="HOTEL", uom="KM"):
        """
        Поиск по коду аэропорта
        """
        request_data = {
            "GeoRef": {
                "Radius": radius,
                "UOM": uom,
                "Category": category,
                "AirportCode": airport_code
            }
        }
        
        return self._make_request(request_data, f"коду аэропорта {airport_code}")
    
    def search_by_city_name(self, city_name, radius=10, category="HOTEL", uom="KM"):
        """
        Поиск по названию города через RefPoint
        """
        request_data = {
            "GeoRef": {
                "Radius": radius,
                "UOM": uom,
                "Category": category,
                "RefPoint": {
                    "Value": city_name,
                    "ValueContext": "NAME",
                    "RefPointType": "5"  # CITY
                }
            }
        }
        
        return self._make_request(request_data, f"названию города {city_name}")
    
    def _make_request(self, request_data, search_type):
        """
        Выполнение запроса к Geo Search API
        """
        if not self.access_token:
            print("Ошибка: токен доступа не получен")
            return None
        
        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            print(f"\nВыполнение поиска по {search_type}...")
            print(f"URL: {self.geo_search_url}")
            print(f"Данные запроса: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
            
            response = requests.post(self.geo_search_url, headers=headers, json=request_data)
            
            print(f"Статус ответа: {response.status_code}")
            print(f"Заголовки ответа: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("Запрос выполнен успешно!")
                return result
            else:
                print(f"Ошибка API: {response.text}")
                return None
                
        except Exception as e:
            print(f"Исключение при выполнении запроса: {e}")
            return None
    
    def analyze_response(self, response_data):
        """
        Анализ ответа API
        """
        if not response_data:
            print("Нет данных для анализа")
            return
        
        print("\n" + "="*50)
        print("АНАЛИЗ ОТВЕТА API")
        print("="*50)
        
        # Проверяем структуру ответа
        if "GeoSearchRS" in response_data:
            geo_search_rs = response_data["GeoSearchRS"]
            
            # Анализируем ApplicationResults
            if "ApplicationResults" in geo_search_rs:
                app_results = geo_search_rs["ApplicationResults"]
                if "Success" in app_results:
                    success = app_results["Success"]
                    print(f"Статус: Успешно")
                    if "TimeStamp" in success:
                        print(f"Временная метка: {success['TimeStamp']}")
            
            # Анализируем GeoSearchResults
            if "GeoSearchResults" in geo_search_rs:
                search_results = geo_search_rs["GeoSearchResults"]
                
                print(f"Радиус поиска: {search_results.get('Radius', 'N/A')}")
                print(f"Единица измерения: {search_results.get('UOM', 'N/A')}")
                print(f"Категория: {search_results.get('Category', 'N/A')}")
                print(f"Широта: {search_results.get('Latitude', 'N/A')}")
                print(f"Долгота: {search_results.get('Longitude', 'N/A')}")
                print(f"Максимум результатов: {search_results.get('MaxSearchResults', 'N/A')}")
                
                # Анализируем найденные результаты
                if "GeoSearchResult" in search_results:
                    results = search_results["GeoSearchResult"]
                    print(f"\nНайдено результатов: {len(results)}")
                    
                    for i, result in enumerate(results[:5]):  # Показываем первые 5
                        print(f"\nРезультат {i+1}:")
                        print(f"  Расстояние: {result.get('Distance', 'N/A')}")
                        print(f"  Направление: {result.get('Direction', 'N/A')}")
                        
                        # Дополнительная информация о локации
                        for key, value in result.items():
                            if key not in ['Distance', 'Direction']:
                                print(f"  {key}: {value}")
                    
                    if len(results) > 5:
                        print(f"\n... и еще {len(results) - 5} результатов")
        
        print("\n" + "="*50)

def main():
    """
    Основная функция для демонстрации работы с API
    """
    print("Sabre Geo Search API - Тестовый запрос")
    print("="*50)
    
    # Создаем экземпляр API клиента
    api = SabreGeoSearchAPI()
    
    # Демонстрационные учетные данные (не рабочие)
    demo_credentials = {
        "client_id": "V1:your_client_id:DEVCENTER:EXT",
        "client_secret": "your_client_secret",
        "username": "your_username",
        "password": "your_password"
    }
    
    print("ВНИМАНИЕ: Используются демонстрационные учетные данные!")
    print("Для реального тестирования необходимо:")
    print("1. Зарегистрироваться на https://developer.sabre.com")
    print("2. Получить реальные Client ID и Client Secret")
    print("3. Получить тестовые EPR учетные данные")
    print()
    
    # Попытка получения токена (ожидается ошибка с демо-данными)
    success = api.get_access_token(
        demo_credentials["client_id"],
        demo_credentials["client_secret"],
        demo_credentials["username"],
        demo_credentials["password"]
    )
    
    if success:
        print("\nТокен получен! Выполняем тестовые запросы...")
        
        # Тест 1: Поиск отелей по координатам (Москва)
        result1 = api.search_by_coordinates(
            latitude=55.7558,
            longitude=37.6176,
            radius=5,
            category="HOTEL"
        )
        if result1:
            api.analyze_response(result1)
        
        # Тест 2: Поиск по коду аэропорта
        result2 = api.search_by_airport_code(
            airport_code="SVO",
            radius=10,
            category="HOTEL"
        )
        if result2:
            api.analyze_response(result2)
        
        # Тест 3: Поиск по названию города
        result3 = api.search_by_city_name(
            city_name="Moscow",
            radius=15,
            category="HOTEL"
        )
        if result3:
            api.analyze_response(result3)
    
    else:
        print("\nНе удалось получить токен доступа.")
        print("Это ожидаемо при использовании демонстрационных учетных данных.")
        print("\nПример структуры запроса:")
        
        # Показываем примеры структур запросов
        example_requests = [
            {
                "name": "Поиск по координатам",
                "data": {
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
                "name": "Поиск по коду аэропорта",
                "data": {
                    "GeoRef": {
                        "Radius": 10,
                        "UOM": "KM",
                        "Category": "HOTEL",
                        "AirportCode": "SVO"
                    }
                }
            },
            {
                "name": "Поиск по названию города",
                "data": {
                    "GeoRef": {
                        "Radius": 10,
                        "UOM": "KM",
                        "Category": "HOTEL",
                        "RefPoint": {
                            "Value": "Moscow",
                            "ValueContext": "NAME",
                            "RefPointType": "5"
                        }
                    }
                }
            }
        ]
        
        for example in example_requests:
            print(f"\n{example['name']}:")
            print(json.dumps(example['data'], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

