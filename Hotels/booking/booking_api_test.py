#!/usr/bin/env python3
"""
Тестовый скрипт для работы с Booking.com Demand API
Основан на официальной документации: https://developers.booking.com/demand/docs/

ВАЖНО: Для работы этого скрипта требуются реальные API ключи от Booking.com,
которые можно получить только после регистрации в качестве партнера.
"""

import requests
import json
from datetime import datetime, timedelta
import os

class BookingAPIClient:
    def __init__(self, api_key=None, affiliate_id=None, sandbox=True):
        """
        Инициализация клиента для работы с Booking.com API
        
        Args:
            api_key (str): API ключ (Bearer token)
            affiliate_id (str): Affiliate ID
            sandbox (bool): Использовать sandbox (True) или production (False)
        """
        self.api_key = api_key or os.getenv('BOOKING_API_KEY', 'DEMO_API_KEY')
        self.affiliate_id = affiliate_id or os.getenv('BOOKING_AFFILIATE_ID', 'DEMO_AFFILIATE_ID')
        
        if sandbox:
            self.base_url = "https://demandapi-sandbox.booking.com/3.1"
        else:
            self.base_url = "https://demandapi.booking.com/3.1"
    
    def _get_headers(self):
        """Получить заголовки для аутентификации"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'X-Affiliate-Id': self.affiliate_id,
            'Content-Type': 'application/json',
            'User-Agent': 'BookingAPITestClient/1.0'
        }
    
    def search_accommodations(self, city_id, checkin_date, checkout_date, 
                            country='us', platform='desktop', 
                            num_rooms=1, num_adults=2, num_children=0):
        """
        Поиск отелей
        
        Args:
            city_id (int): ID города (например, -2140479 для Амстердама)
            checkin_date (str): Дата заезда в формате YYYY-MM-DD
            checkout_date (str): Дата выезда в формате YYYY-MM-DD
            country (str): Код страны в нижнем регистре
            platform (str): Платформа (desktop, mobile, tablet, android, ios)
            num_rooms (int): Количество номеров
            num_adults (int): Количество взрослых
            num_children (int): Количество детей
        
        Returns:
            dict: Ответ API или None в случае ошибки
        """
        url = f"{self.base_url}/accommodations/search"
        
        payload = {
            "city": city_id,
            "booker": {
                "country": country.lower(),
                "platform": platform
            },
            "checkin": checkin_date,
            "checkout": checkout_date,
            "guests": {
                "number_of_rooms": num_rooms,
                "number_of_adults": num_adults
            }
        }
        
        if num_children > 0:
            payload["guests"]["children"] = [{"age": 10}] * num_children
        
        try:
            print(f"Отправка запроса к: {url}")
            print(f"Заголовки: {json.dumps(self._get_headers(), indent=2)}")
            print(f"Тело запроса: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                url, 
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            
            print(f"Статус ответа: {response.status_code}")
            print(f"Заголовки ответа: {dict(response.headers)}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("Ошибка 401: Неверные учетные данные API")
                print("Проверьте API key и Affiliate ID")
            elif response.status_code == 403:
                print("Ошибка 403: Доступ запрещен")
                print("API пользователь не имеет прав доступа к этому эндпоинту")
            else:
                print(f"Ошибка {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
        
        return None
    
    def get_accommodation_details(self, accommodation_ids, extras=None, languages=None):
        """
        Получить детали отелей
        
        Args:
            accommodation_ids (list): Список ID отелей
            extras (list): Дополнительная информация ['description', 'facilities', 'rooms', 'photos', 'policies']
            languages (list): Языки ['en-gb', 'ru-ru', etc.]
        
        Returns:
            dict: Ответ API или None в случае ошибки
        """
        url = f"{self.base_url}/accommodations/details"
        
        payload = {
            "accommodations": accommodation_ids
        }
        
        if extras:
            payload["extras"] = extras
        
        if languages:
            payload["languages"] = languages
        
        try:
            print(f"Получение деталей для отелей: {accommodation_ids}")
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка получения деталей: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Ошибка при получении деталей: {e}")
        
        return None

def demo_search():
    """Демонстрация поиска отелей"""
    print("=== Демонстрация работы с Booking.com API ===\n")
    
    # Создание клиента (с демо-ключами)
    client = BookingAPIClient(sandbox=True)
    
    # Параметры поиска
    city_id = -2140479  # Амстердам
    checkin = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    checkout = (datetime.now() + timedelta(days=32)).strftime('%Y-%m-%d')
    
    print(f"Поиск отелей в Амстердаме:")
    print(f"Заезд: {checkin}")
    print(f"Выезд: {checkout}")
    print(f"Гости: 2 взрослых, 1 номер\n")
    
    # Поиск отелей
    search_result = client.search_accommodations(
        city_id=city_id,
        checkin_date=checkin,
        checkout_date=checkout,
        country='nl',
        platform='desktop'
    )
    
    if search_result:
        print("✅ Поиск выполнен успешно!")
        print(f"Найдено отелей: {len(search_result.get('accommodations', []))}")
        
        # Получение деталей для первых 3 отелей
        accommodation_ids = [acc['id'] for acc in search_result.get('accommodations', [])[:3]]
        if accommodation_ids:
            details = client.get_accommodation_details(
                accommodation_ids,
                extras=['description', 'facilities', 'photos'],
                languages=['en-gb']
            )
            
            if details:
                print("✅ Детали отелей получены успешно!")
    else:
        print("❌ Поиск не удался")
        print("\nВозможные причины:")
        print("1. Отсутствуют реальные API ключи")
        print("2. Нет доступа к Booking.com Partner Centre")
        print("3. Проблемы с сетью")

def demo_sandbox_hotel():
    """Демонстрация работы с тестовым отелем из Sandbox"""
    print("\n=== Тестирование с Sandbox отелем ===\n")
    
    client = BookingAPIClient(sandbox=True)
    
    # ID тестового отеля из документации
    sandbox_hotel_id = 10507360  # Demand API sandbox Hotel Orion
    
    print(f"Получение информации о тестовом отеле ID: {sandbox_hotel_id}")
    
    details = client.get_accommodation_details(
        accommodation_ids=[sandbox_hotel_id],
        extras=['description', 'facilities', 'rooms', 'photos'],
        languages=['en-gb']
    )
    
    if details:
        print("✅ Информация о тестовом отеле получена!")
        # Здесь можно было бы обработать и показать данные
    else:
        print("❌ Не удалось получить информацию о тестовом отеле")

if __name__ == "__main__":
    print("Booking.com API Test Client")
    print("=" * 50)
    
    # Проверка наличия реальных API ключей
    api_key = os.getenv('BOOKING_API_KEY')
    affiliate_id = os.getenv('BOOKING_AFFILIATE_ID')
    
    if api_key and affiliate_id and api_key != 'DEMO_API_KEY':
        print("✅ Найдены API ключи в переменных окружения")
    else:
        print("⚠️  Используются демо-ключи")
        print("Для реального тестирования установите переменные окружения:")
        print("export BOOKING_API_KEY='your_api_key'")
        print("export BOOKING_AFFILIATE_ID='your_affiliate_id'")
        print()
    
    # Запуск демонстрации
    demo_search()
    demo_sandbox_hotel()
    
    print("\n" + "=" * 50)
    print("Демонстрация завершена")

