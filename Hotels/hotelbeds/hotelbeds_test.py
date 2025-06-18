#!/usr/bin/env python3
"""
Тестовый скрипт для работы с Hotelbeds Booking API
Демонстрирует структуру запросов и аутентификацию
"""

import requests
import hashlib
import time
import json
from datetime import datetime, timedelta

class HotelbedsAPI:
    def __init__(self, api_key, secret, test_mode=True):
        """
        Инициализация клиента Hotelbeds API
        
        Args:
            api_key (str): API ключ
            secret (str): Секретный ключ
            test_mode (bool): Использовать тестовую среду
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = "https://api.test.hotelbeds.com" if test_mode else "https://api.hotelbeds.com"
        
    def _generate_signature(self):
        """Генерация X-Signature для аутентификации"""
        timestamp = str(int(time.time()))
        signature_string = self.api_key + self.secret + timestamp
        signature = hashlib.sha256(signature_string.encode()).hexdigest()
        return signature
    
    def _get_headers(self):
        """Получение заголовков для запроса"""
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Api-key': self.api_key,
            'X-Signature': self._generate_signature()
        }
    
    def check_status(self):
        """Проверка статуса API"""
        url = f"{self.base_url}/hotel-api/1.0/status"
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            return {
                'status_code': response.status_code,
                'response': response.text,
                'headers': dict(response.headers)
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def search_hotels(self, destination, checkin_date, checkout_date, adults=2, children=0):
        """
        Поиск отелей (метод /hotels)
        
        Args:
            destination (str): Код назначения
            checkin_date (str): Дата заезда (YYYY-MM-DD)
            checkout_date (str): Дата выезда (YYYY-MM-DD)
            adults (int): Количество взрослых
            children (int): Количество детей
        """
        url = f"{self.base_url}/hotel-api/1.0/hotels"
        headers = self._get_headers()
        
        payload = {
            "stay": {
                "checkIn": checkin_date,
                "checkOut": checkout_date
            },
            "occupancies": [
                {
                    "rooms": 1,
                    "adults": adults,
                    "children": children
                }
            ],
            "destination": {
                "code": destination
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            return {
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text,
                'headers': dict(response.headers)
            }
        except Exception as e:
            return {
                'error': str(e)
            }

def demo_without_credentials():
    """Демонстрация структуры запросов без реальных учетных данных"""
    print("=== Демонстрация Hotelbeds API ===\n")
    
    # Создаем экземпляр с демо-данными
    api = HotelbedsAPI("DEMO_API_KEY", "DEMO_SECRET")
    
    print("1. Структура аутентификации:")
    print(f"   Base URL: {api.base_url}")
    print(f"   API Key: {api.api_key}")
    print(f"   Signature: {api._generate_signature()}")
    print(f"   Headers: {json.dumps(api._get_headers(), indent=2)}")
    
    print("\n2. Пример запроса статуса:")
    status_result = api.check_status()
    print(f"   Status Code: {status_result.get('status_code', 'N/A')}")
    print(f"   Response: {status_result.get('response', status_result.get('error', 'N/A'))}")
    
    print("\n3. Пример поиска отелей:")
    # Даты для примера (завтра и послезавтра)
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    day_after = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    search_result = api.search_hotels("BCN", tomorrow, day_after, adults=2)
    print(f"   Status Code: {search_result.get('status_code', 'N/A')}")
    print(f"   Response: {search_result.get('response', search_result.get('error', 'N/A'))}")
    
    return {
        'api_structure': api._get_headers(),
        'status_check': status_result,
        'hotel_search': search_result
    }

if __name__ == "__main__":
    results = demo_without_credentials()
    
    # Сохраняем результаты в файл
    with open('/home/ubuntu/hotelbeds_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nРезультаты сохранены в hotelbeds_test_results.json")

