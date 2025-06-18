"""
Демонстрационный код для работы с Amadeus City Search API

Этот код показывает:
1. Как получить access token через OAuth 2.0
2. Как выполнить поиск городов
3. Как обработать различные типы ответов
4. Как анализировать результаты

Для работы с реальным API замените DEMO_API_KEY и DEMO_API_SECRET 
на ваши настоящие ключи от Amadeus for Developers.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any

class AmadeusClient:
    """Клиент для работы с Amadeus API"""
    
    def __init__(self, api_key: str, api_secret: str, test_mode: bool = True):
        """
        Инициализация клиента
        
        Args:
            api_key: API ключ от Amadeus
            api_secret: API секрет от Amadeus  
            test_mode: Использовать тестовую среду (True) или продакшн (False)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.test_mode = test_mode
        
        # URLs для разных сред
        if test_mode:
            self.base_url = "https://test.api.amadeus.com/v1"
        else:
            self.base_url = "https://api.amadeus.com/v1"
            
        self.token_url = f"{self.base_url}/security/oauth2/token"
        self.city_search_url = f"{self.base_url}/reference-data/locations/cities"
        
        # Токен и время его истечения
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self) -> Optional[str]:
        """
        Получение access token через OAuth 2.0
        
        Returns:
            Access token или None в случае ошибки
        """
        print("🔐 Получение access token...")
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        
        try:
            response = requests.post(
                self.token_url,
                headers=headers,
                data=data,
                timeout=10
            )
            
            print(f"Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 1800)  # По умолчанию 30 минут
                
                # Вычисляем время истечения токена
                self.token_expires_at = time.time() + expires_in - 60  # Обновляем за минуту до истечения
                
                print("✅ Токен успешно получен")
                print(f"Тип токена: {token_data.get('token_type')}")
                print(f"Истекает через: {expires_in} секунд")
                print(f"Токен: {self.access_token[:20]}...")
                
                return self.access_token
            else:
                print("❌ Ошибка получения токена:")
                print(f"Статус: {response.status_code}")
                print(f"Ответ: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Исключение при получении токена: {e}")
            return None
    
    def is_token_valid(self) -> bool:
        """Проверка валидности токена"""
        if not self.access_token or not self.token_expires_at:
            return False
        return time.time() < self.token_expires_at
    
    def ensure_valid_token(self) -> bool:
        """Обеспечение наличия валидного токена"""
        if not self.is_token_valid():
            return self.get_access_token() is not None
        return True
    
    def search_cities(self, 
                     keyword: str, 
                     country_code: Optional[str] = None,
                     max_results: int = 10,
                     include_airports: bool = False) -> Dict[str, Any]:
        """
        Поиск городов по ключевому слову
        
        Args:
            keyword: Ключевое слово для поиска (обязательно)
            country_code: Код страны ISO 3166 Alpha-2 (опционально)
            max_results: Максимальное количество результатов
            include_airports: Включать информацию об аэропортах
            
        Returns:
            Словарь с результатами поиска
        """
        print(f"\n🔍 Поиск городов по ключевому слову: '{keyword}'")
        
        # Проверяем токен
        if not self.ensure_valid_token():
            return {"error": "Не удалось получить валидный токен"}
        
        # Подготавливаем параметры запроса
        params = {
            "keyword": keyword,
            "max": max_results
        }
        
        if country_code:
            params["countryCode"] = country_code
            
        if include_airports:
            params["include"] = "AIRPORTS"
        
        # Заголовки запроса
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.amadeus+json"
        }
        
        print(f"Параметры: {params}")
        
        try:
            response = requests.get(
                self.city_search_url,
                params=params,
                headers=headers,
                timeout=10
            )
            
            print(f"Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Поиск выполнен успешно")
                return {
                    "success": True,
                    "data": data,
                    "request_params": params
                }
            else:
                print("❌ Ошибка поиска:")
                error_data = response.json() if response.content else {}
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": error_data,
                    "request_params": params
                }
                
        except Exception as e:
            print(f"❌ Исключение при поиске: {e}")
            return {
                "success": False,
                "error": str(e),
                "request_params": params
            }
    
    def analyze_results(self, search_result: Dict[str, Any]) -> None:
        """Анализ результатов поиска"""
        print("\n📊 АНАЛИЗ РЕЗУЛЬТАТОВ")
        print("=" * 50)
        
        if not search_result.get("success"):
            print("❌ Поиск завершился с ошибкой:")
            if "status_code" in search_result:
                print(f"Код ошибки: {search_result['status_code']}")
            if "error" in search_result:
                error = search_result["error"]
                if isinstance(error, dict) and "errors" in error:
                    for err in error["errors"]:
                        print(f"- Код: {err.get('code')}")
                        print(f"- Заголовок: {err.get('title')}")
                        print(f"- Детали: {err.get('detail')}")
                else:
                    print(f"Ошибка: {error}")
            return
        
        data = search_result.get("data", {})
        cities = data.get("data", [])
        
        print(f"Найдено городов: {len(cities)}")
        print(f"Параметры запроса: {search_result.get('request_params', {})}")
        
        if not cities:
            print("Города не найдены")
            return
        
        print("\nНайденные города:")
        print("-" * 30)
        
        for i, city in enumerate(cities, 1):
            print(f"\n{i}. {city.get('name', 'Неизвестно')}")
            print(f"   Тип: {city.get('subType', 'Неизвестно')}")
            
            # Адрес
            address = city.get('address', {})
            if address:
                country = address.get('countryCode', 'Неизвестно')
                print(f"   Страна: {country}")
            
            # Координаты
            geo_code = city.get('geoCode', {})
            if geo_code:
                lat = geo_code.get('latitude', 'Неизвестно')
                lon = geo_code.get('longitude', 'Неизвестно')
                print(f"   Координаты: {lat}, {lon}")
            
            # IATA код
            iata_code = city.get('iataCode')
            if iata_code:
                print(f"   IATA код: {iata_code}")
            
            # Связанные аэропорты
            relationships = city.get('relationships', [])
            if relationships:
                airports = [rel.get('id') for rel in relationships if rel.get('type') == 'Airport']
                if airports:
                    print(f"   Аэропорты: {', '.join(airports)}")


def demo_city_search():
    """Демонстрация работы с City Search API"""
    print("🚀 ДЕМОНСТРАЦИЯ AMADEUS CITY SEARCH API")
    print("=" * 60)
    
    # ВНИМАНИЕ: Это демонстрационные ключи!
    # Для реальной работы замените на ваши ключи от Amadeus for Developers
    DEMO_API_KEY = "YOUR_API_KEY_HERE"
    DEMO_API_SECRET = "YOUR_API_SECRET_HERE"
    
    print("⚠️  ВНИМАНИЕ: Используются демонстрационные ключи!")
    print("Для реальной работы замените DEMO_API_KEY и DEMO_API_SECRET")
    print("на ваши настоящие ключи от Amadeus for Developers\n")
    
    # Создаем клиент
    client = AmadeusClient(DEMO_API_KEY, DEMO_API_SECRET, test_mode=True)
    
    # Примеры поисковых запросов
    test_cases = [
        {
            "name": "Поиск городов, начинающихся с 'PAR'",
            "keyword": "PAR",
            "max_results": 5,
            "include_airports": True
        },
        {
            "name": "Поиск городов 'LON' в Великобритании",
            "keyword": "LON", 
            "country_code": "GB",
            "max_results": 3,
            "include_airports": True
        },
        {
            "name": "Поиск городов 'NEW'",
            "keyword": "NEW",
            "max_results": 7,
            "include_airports": False
        },
        {
            "name": "Поиск городов 'MOS' в России",
            "keyword": "MOS",
            "country_code": "RU", 
            "max_results": 5,
            "include_airports": True
        }
    ]
    
    # Выполняем тестовые запросы
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*20} ТЕСТ {i}: {test_case['name']} {'='*20}")
        
        result = client.search_cities(
            keyword=test_case["keyword"],
            country_code=test_case.get("country_code"),
            max_results=test_case["max_results"],
            include_airports=test_case["include_airports"]
        )
        
        client.analyze_results(result)
        
        # Пауза между запросами
        if i < len(test_cases):
            print("\n⏳ Пауза 2 секунды...")
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print("✅ Демонстрация завершена!")
    print("\nДля работы с реальным API:")
    print("1. Зарегистрируйтесь на https://developers.amadeus.com/")
    print("2. Создайте приложение и получите API ключи")
    print("3. Замените DEMO_API_KEY и DEMO_API_SECRET на ваши ключи")
    print("4. Запустите код снова")


if __name__ == "__main__":
    demo_city_search()

