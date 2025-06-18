#!/usr/bin/env python3
"""
Тестовый скрипт для работы с API GetYourGuide
Демонстрирует структуру запросов и обработку ответов
"""

import requests
import json
from typing import Dict, Any, Optional

class GetYourGuideAPI:
    """Класс для работы с API GetYourGuide"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.getyourguide.com"):
        """
        Инициализация клиента API
        
        Args:
            api_key: API ключ для аутентификации
            base_url: Базовый URL API (по умолчанию production)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'X-ACCESS-TOKEN': api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_categories(self, 
                      version: str = "1",
                      language: str = "en", 
                      currency: str = "USD",
                      limit: int = 10,
                      offset: int = 0) -> Dict[str, Any]:
        """
        Получить список категорий туров
        
        Args:
            version: Версия API
            language: Язык ответа (en, de, fr, etc.)
            currency: Валюта (USD, EUR, etc.)
            limit: Количество результатов
            offset: Смещение для пагинации
            
        Returns:
            Словарь с данными категорий или информацией об ошибке
        """
        url = f"{self.base_url}/{version}/categories"
        params = {
            'cnt_language': language,
            'currency': currency,
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            result = {
                'status_code': response.status_code,
                'url': response.url,
                'headers': dict(response.headers),
                'success': response.status_code == 200
            }
            
            try:
                result['data'] = response.json()
            except json.JSONDecodeError:
                result['data'] = response.text
                
            return result
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': None
            }
    
    def get_tours(self,
                  version: str = "1",
                  language: str = "en",
                  currency: str = "USD",
                  limit: int = 10,
                  offset: int = 0,
                  **kwargs) -> Dict[str, Any]:
        """
        Поиск туров
        
        Args:
            version: Версия API
            language: Язык ответа
            currency: Валюта
            limit: Количество результатов
            offset: Смещение для пагинации
            **kwargs: Дополнительные параметры поиска
            
        Returns:
            Словарь с данными туров или информацией об ошибке
        """
        url = f"{self.base_url}/{version}/tours"
        params = {
            'cnt_language': language,
            'currency': currency,
            'limit': limit,
            'offset': offset,
            **kwargs
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            result = {
                'status_code': response.status_code,
                'url': response.url,
                'success': response.status_code == 200
            }
            
            try:
                result['data'] = response.json()
            except json.JSONDecodeError:
                result['data'] = response.text
                
            return result
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': None
            }

def test_api_without_token():
    """Тестирование API без токена (демонстрация ошибки аутентификации)"""
    print("=== Тест без API токена ===")
    
    # Создаем клиент с пустым токеном
    client = GetYourGuideAPI("")
    
    # Пытаемся получить категории
    result = client.get_categories()
    
    print(f"Статус код: {result['status_code']}")
    print(f"URL запроса: {result['url']}")
    print(f"Успешно: {result['success']}")
    
    if 'data' in result:
        print("Ответ API:")
        print(json.dumps(result['data'], indent=2, ensure_ascii=False))
    
    return result

def test_api_with_token(api_key: str):
    """Тестирование API с валидным токеном"""
    print(f"\n=== Тест с API токеном ===")
    
    # Создаем клиент с токеном
    client = GetYourGuideAPI(api_key)
    
    # Тестируем получение категорий
    print("\n--- Получение категорий ---")
    result = client.get_categories(limit=5)
    
    print(f"Статус код: {result['status_code']}")
    print(f"URL запроса: {result['url']}")
    print(f"Успешно: {result['success']}")
    
    if result['success'] and 'data' in result:
        data = result['data']
        if 'data' in data and 'categories' in data['data']:
            categories = data['data']['categories']
            print(f"Найдено категорий: {len(categories)}")
            for cat in categories[:3]:  # Показываем первые 3
                print(f"- {cat.get('name', 'N/A')} (ID: {cat.get('category_id', 'N/A')})")
    else:
        print("Ошибка при получении категорий:")
        if 'data' in result:
            print(json.dumps(result['data'], indent=2, ensure_ascii=False))
    
    return result

if __name__ == "__main__":
    print("Тестирование API GetYourGuide")
    print("=" * 50)
    
    # Тест без токена (покажет ошибку аутентификации)
    result_no_token = test_api_without_token()
    
    # Для тестирования с токеном нужен реальный API ключ
    print("\n" + "=" * 50)
    print("Для тестирования с валидным токеном:")
    print("api_key = 'ваш_реальный_api_ключ'")
    print("result_with_token = test_api_with_token(api_key)")
    
    # Пример использования:
    # api_key = "your_real_api_key_here"
    # result_with_token = test_api_with_token(api_key)

