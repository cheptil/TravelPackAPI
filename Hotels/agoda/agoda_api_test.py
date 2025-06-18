#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации запроса к Agoda API
Этот скрипт показывает структуру запроса, но не может выполнить реальный запрос
без валидных учетных данных партнера Agoda.
"""

import requests
import json
from datetime import datetime, timedelta

class AgodaAPIClient:
    def __init__(self, site_id, api_key, is_sandbox=True):
        """
        Инициализация клиента Agoda API
        
        Args:
            site_id (str): ID сайта партнера
            api_key (str): API ключ
            is_sandbox (bool): Использовать sandbox окружение
        """
        self.site_id = site_id
        self.api_key = api_key
        
        # URL эндпоинты (предполагаемые на основе документации)
        if is_sandbox:
            self.json_search_url = "https://sandbox-distribution.agoda.com/api/search"
            self.xml_search_url = "https://sandbox-distribution.agoda.com/dsws/hotelapi.asmx"
        else:
            self.json_search_url = "https://distribution.agoda.com/api/search"
            self.xml_search_url = "https://distribution.agoda.com/dsws/hotelapi.asmx"
    
    def get_headers(self, content_type="application/json"):
        """Получить HTTP заголовки для запроса"""
        return {
            "Authorization": f"{self.site_id}:{self.api_key}",
            "Content-Type": content_type,
            "Accept-Encoding": "gzip,deflate",
            "User-Agent": "AgodaAPITestClient/1.0"
        }
    
    def create_json_search_request(self, property_ids, check_in, check_out, 
                                 rooms=1, adults=2, children=0, children_ages=None,
                                 language="en-us", currency="USD", user_country="US"):
        """
        Создать JSON запрос для поиска отелей
        
        Args:
            property_ids (list): Список ID отелей
            check_in (str): Дата заезда (YYYY-MM-DD)
            check_out (str): Дата выезда (YYYY-MM-DD)
            rooms (int): Количество номеров
            adults (int): Количество взрослых
            children (int): Количество детей
            children_ages (list): Возраст детей
            language (str): Язык ответа
            currency (str): Валюта
            user_country (str): Страна пользователя
        
        Returns:
            dict: JSON запрос
        """
        request_data = {
            "criteria": {
                "propertyIds": property_ids,
                "checkIn": check_in,
                "checkOut": check_out,
                "rooms": rooms,
                "adults": adults,
                "children": children,
                "language": language,
                "currency": currency,
                "userCountry": user_country
            },
            "features": {
                "ratesPerProperty": 25,
                "extra": [
                    "content",
                    "surchargeDetail",
                    "cancellationDetail",
                    "benefitDetail",
                    "dailyRate",
                    "taxDetail",
                    "rateDetail",
                    "promotionDetail"
                ]
            }
        }
        
        if children > 0 and children_ages:
            request_data["criteria"]["childrenAges"] = children_ages
            
        return request_data
    
    def search_hotels_json(self, property_ids, check_in, check_out, **kwargs):
        """
        Выполнить поиск отелей через JSON API
        
        Returns:
            dict: Ответ API или информация об ошибке
        """
        try:
            # Создаем запрос
            request_data = self.create_json_search_request(
                property_ids, check_in, check_out, **kwargs
            )
            
            # Получаем заголовки
            headers = self.get_headers("application/json")
            
            print("=== ДЕМОНСТРАЦИЯ ЗАПРОСА К AGODA JSON SEARCH API ===")
            print(f"URL: {self.json_search_url}")
            print(f"Headers: {json.dumps(headers, indent=2)}")
            print(f"Request Body: {json.dumps(request_data, indent=2)}")
            print()
            
            # Попытка выполнить запрос (ожидается ошибка без валидных учетных данных)
            response = requests.post(
                self.json_search_url,
                headers=headers,
                json=request_data,
                timeout=30
            )
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "Network error",
                "details": str(e),
                "note": "Это ожидаемо без валидных учетных данных"
            }

def demo_agoda_api():
    """Демонстрация использования Agoda API"""
    
    # Тестовые учетные данные (НЕ РЕАЛЬНЫЕ)
    # В реальном проекте эти данные предоставляются Agoda после регистрации
    DEMO_SITE_ID = "123456"
    DEMO_API_KEY = "00000000-0000-0000-0000-000000000000"
    
    # Создаем клиент
    client = AgodaAPIClient(DEMO_SITE_ID, DEMO_API_KEY, is_sandbox=True)
    
    # Параметры поиска
    property_ids = [12157, 69001]  # Примеры ID отелей из документации
    
    # Даты (завтра и послезавтра)
    tomorrow = datetime.now() + timedelta(days=1)
    day_after = datetime.now() + timedelta(days=2)
    
    check_in = tomorrow.strftime("%Y-%m-%d")
    check_out = day_after.strftime("%Y-%m-%d")
    
    print("=== ТЕСТИРОВАНИЕ AGODA API ===")
    print(f"Поиск отелей ID: {property_ids}")
    print(f"Заезд: {check_in}")
    print(f"Выезд: {check_out}")
    print(f"Номеров: 1, Взрослых: 2")
    print()
    
    # Выполняем тестовый запрос
    result = client.search_hotels_json(
        property_ids=property_ids,
        check_in=check_in,
        check_out=check_out,
        rooms=1,
        adults=2,
        children=0,
        language="en-us",
        currency="USD",
        user_country="US"
    )
    
    print("=== РЕЗУЛЬТАТ ЗАПРОСА ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

if __name__ == "__main__":
    result = demo_agoda_api()

