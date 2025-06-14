#!/usr/bin/env python3
"""
Рабочий пример для тестирования Foursquare Places API

Для использования:
1. Зарегистрируйтесь на https://foursquare.com/developer/
2. Создайте новый проект
3. Получите API ключ
4. Замените 'YOUR_API_KEY' на ваш реальный ключ
5. Запустите скрипт: python3 foursquare_example.py
"""

import requests
import json
import os
from typing import Dict, List, Optional

class FoursquareAPI:
    """Класс для работы с Foursquare Places API"""
    
    def __init__(self, api_key: str):
        """
        Инициализация клиента API
        
        Args:
            api_key: API ключ от Foursquare
        """
        self.api_key = api_key
        self.base_url = "https://api.foursquare.com/v3"
        self.headers = {
            "Accept": "application/json",
            "Authorization": api_key
        }
    
    def search_places(self, 
                     query: str = None,
                     ll: str = None,
                     near: str = None,
                     radius: int = 1000,
                     categories: str = None,
                     limit: int = 10) -> Dict:
        """
        Поиск мест
        
        Args:
            query: Поисковый запрос (например, "coffee")
            ll: Координаты "latitude,longitude"
            near: Название локации (например, "Moscow, Russia")
            radius: Радиус поиска в метрах
            categories: ID категорий через запятую
            limit: Количество результатов
            
        Returns:
            Словарь с результатами поиска
        """
        url = f"{self.base_url}/places/search"
        
        params = {}
        if query:
            params["query"] = query
        if ll:
            params["ll"] = ll
        if near:
            params["near"] = near
        if radius:
            params["radius"] = radius
        if categories:
            params["categories"] = categories
        if limit:
            params["limit"] = limit
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_place_details(self, fsq_id: str, fields: str = None) -> Dict:
        """
        Получение детальной информации о месте
        
        Args:
            fsq_id: ID места в Foursquare
            fields: Список полей через запятую
            
        Returns:
            Словарь с информацией о месте
        """
        url = f"{self.base_url}/places/{fsq_id}"
        
        params = {}
        if fields:
            params["fields"] = fields
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_place_photos(self, fsq_id: str, limit: int = 5) -> Dict:
        """
        Получение фотографий места
        
        Args:
            fsq_id: ID места в Foursquare
            limit: Количество фотографий
            
        Returns:
            Словарь с фотографиями
        """
        url = f"{self.base_url}/places/{fsq_id}/photos"
        
        params = {"limit": limit}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def autocomplete(self, text: str, ll: str = None, radius: int = 1000) -> Dict:
        """
        Автодополнение для поиска
        
        Args:
            text: Текст для автодополнения
            ll: Координаты "latitude,longitude"
            radius: Радиус поиска в метрах
            
        Returns:
            Словарь с предложениями
        """
        url = f"{self.base_url}/autocomplete"
        
        params = {"text": text}
        if ll:
            params["ll"] = ll
        if radius:
            params["radius"] = radius
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

def print_places(places_data: Dict):
    """Красивый вывод информации о местах"""
    
    if "results" not in places_data:
        print("Нет результатов")
        return
        
    places = places_data["results"]
    print(f"Найдено мест: {len(places)}")
    print("=" * 50)
    
    for i, place in enumerate(places, 1):
        print(f"{i}. {place.get('name', 'Без названия')}")
        
        # Адрес
        location = place.get('location', {})
        address = location.get('formatted_address', 'Адрес не указан')
        print(f"   Адрес: {address}")
        
        # Категории
        categories = place.get('categories', [])
        if categories:
            cat_names = [cat.get('name', '') for cat in categories]
            print(f"   Категории: {', '.join(cat_names)}")
        
        # Расстояние
        distance = place.get('distance')
        if distance is not None:
            print(f"   Расстояние: {distance} м")
        
        # ID для дальнейших запросов
        fsq_id = place.get('fsq_id')
        if fsq_id:
            print(f"   ID: {fsq_id}")
        
        print()

def main():
    """Основная функция с примерами использования"""
    
    # ВАЖНО: Замените на ваш реальный API ключ!
    api_key = os.getenv('FOURSQUARE_API_KEY', 'YOUR_API_KEY')
    
    if api_key == 'YOUR_API_KEY':
        print("⚠️  ВНИМАНИЕ: Замените 'YOUR_API_KEY' на ваш реальный API ключ!")
        print("Получить ключ можно на: https://foursquare.com/developer/")
        print("Или установите переменную окружения: export FOURSQUARE_API_KEY=ваш_ключ")
        return
    
    # Создаем клиент API
    client = FoursquareAPI(api_key)
    
    try:
        print("🔍 Тестирование Foursquare Places API")
        print("=" * 50)
        
        # Пример 1: Поиск кофеен в Москве
        print("1. Поиск кофеен в Москве:")
        moscow_coords = "55.7558,37.6176"  # Красная площадь
        
        coffee_results = client.search_places(
            query="coffee",
            ll=moscow_coords,
            radius=2000,
            limit=5
        )
        
        print_places(coffee_results)
        
        # Пример 2: Поиск ресторанов по категории
        print("2. Поиск ресторанов:")
        restaurant_results = client.search_places(
            categories="13065",  # Категория "Restaurant"
            ll=moscow_coords,
            radius=1500,
            limit=3
        )
        
        print_places(restaurant_results)
        
        # Пример 3: Автодополнение
        print("3. Автодополнение для 'пицц':")
        autocomplete_results = client.autocomplete(
            text="пицц",
            ll=moscow_coords
        )
        
        suggestions = autocomplete_results.get("results", [])
        for suggestion in suggestions[:3]:
            text = suggestion.get("text", {})
            primary = text.get("primary", "")
            secondary = text.get("secondary", "")
            print(f"   • {primary} {secondary}")
        
        print()
        
        # Пример 4: Детали места (если есть результаты)
        if coffee_results.get("results"):
            first_place = coffee_results["results"][0]
            fsq_id = first_place.get("fsq_id")
            
            if fsq_id:
                print(f"4. Детали места '{first_place.get('name')}':")
                
                details = client.get_place_details(
                    fsq_id,
                    fields="name,location,categories,hours,rating,price,website,tel"
                )
                
                print(f"   Название: {details.get('name', 'Не указано')}")
                print(f"   Рейтинг: {details.get('rating', 'Не указан')}")
                print(f"   Цена: {details.get('price', 'Не указана')}")
                print(f"   Телефон: {details.get('tel', 'Не указан')}")
                print(f"   Сайт: {details.get('website', 'Не указан')}")
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Ошибка авторизации: проверьте API ключ")
        elif e.response.status_code == 429:
            print("❌ Превышен лимит запросов")
        else:
            print(f"❌ HTTP ошибка: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()

