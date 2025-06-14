#!/usr/bin/env python3
"""
Тестовый скрипт для TripAdvisor Content API
Демонстрирует, как выполнять запросы к API и обрабатывать ответы
"""

import requests
import json
from typing import Dict, Any, Optional

class TripAdvisorAPI:
    """Класс для работы с TripAdvisor Content API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.content.tripadvisor.com/api/v1"
        self.headers = {
            "accept": "application/json"
        }
    
    def get_location_details(self, location_id: int, language: str = "en", currency: str = "USD") -> Dict[str, Any]:
        """
        Получить детали локации по ID
        
        Args:
            location_id: Уникальный идентификатор локации
            language: Язык ответа (по умолчанию "en")
            currency: Код валюты (по умолчанию "USD")
            
        Returns:
            Словарь с данными локации или информацией об ошибке
        """
        url = f"{self.base_url}/location/{location_id}/details"
        params = {
            "key": self.api_key,
            "language": language,
            "currency": currency
        }
        
        try:
            print(f"Выполняю запрос к: {url}")
            print(f"Параметры: {params}")
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            print(f"Статус ответа: {response.status_code}")
            print(f"Заголовки ответа: {dict(response.headers)}")
            
            # Попытка получить JSON ответ
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"error": "Не удалось декодировать JSON", "text": response.text}
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response_data,
                "success": response.status_code == 200
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Ошибка запроса: {str(e)}",
                "success": False
            }

def test_api():
    """Тестирование API с демонстрационными данными"""
    
    # Используем тестовый API ключ (не рабочий)
    test_api_key = "TEST_API_KEY_DEMO"
    
    # Создаем экземпляр API клиента
    api = TripAdvisorAPI(test_api_key)
    
    # Тестовый location_id (например, для известного отеля)
    # В реальности нужно получить через Location Search API
    test_location_id = 60763
    
    print("=== Тестирование TripAdvisor Content API ===")
    print(f"API ключ: {test_api_key}")
    print(f"Тестовый location_id: {test_location_id}")
    print()
    
    # Выполняем тестовый запрос
    result = api.get_location_details(test_location_id)
    
    print("=== Результат запроса ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Анализ результата
    if result.get("success"):
        print("\n✅ Запрос выполнен успешно!")
        location_data = result["data"]
        print(f"Название: {location_data.get('name', 'Не указано')}")
        print(f"Описание: {location_data.get('description', 'Не указано')}")
        print(f"URL: {location_data.get('web_url', 'Не указано')}")
    else:
        print("\n❌ Запрос завершился с ошибкой")
        if result["status_code"] == 401:
            print("Ошибка аутентификации - неверный API ключ")
        elif result["status_code"] == 403:
            print("Доступ запрещен - проверьте права API ключа")
        elif result["status_code"] == 404:
            print("Локация не найдена - проверьте location_id")
        elif result["status_code"] == 429:
            print("Превышен лимит запросов - подождите перед следующим запросом")

if __name__ == "__main__":
    test_api()

