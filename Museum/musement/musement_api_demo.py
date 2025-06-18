#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования API Musement
Показывает, как бы выполнялись запросы к API при наличии credentials
"""

import requests
import json
from datetime import datetime

class MusementAPIClient:
    def __init__(self, base_url, application_value, client_id, client_secret):
        self.base_url = base_url.rstrip('/')
        self.application_value = application_value
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None
    
    def get_headers(self, include_auth=True):
        """Получить стандартные заголовки для запросов"""
        headers = {
            'X-Musement-Application': self.application_value,
            'X-Musement-Version': '3.4.0',
            'Content-Type': 'application/json'
        }
        
        if include_auth and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
            
        return headers
    
    def authenticate(self):
        """Получить access token через OAuth 2.0"""
        url = f"{self.base_url}/login"
        
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        headers = self.get_headers(include_auth=False)
        
        try:
            print(f"Отправляем запрос аутентификации на: {url}")
            print(f"Заголовки: {json.dumps(headers, indent=2)}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(url, json=payload, headers=headers)
            
            print(f"Статус ответа: {response.status_code}")
            print(f"Заголовки ответа: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                expires_in = data.get('expires_in', 3600)
                
                # Вычисляем время истечения токена
                from datetime import datetime, timedelta
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                print(f"Аутентификация успешна!")
                print(f"Access token получен (истекает в {self.token_expires_at})")
                return True
            else:
                print(f"Ошибка аутентификации: {response.text}")
                return False
                
        except requests.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return False
    
    def search_activities(self, **params):
        """Поиск активностей"""
        if not self.access_token:
            print("Необходимо сначала выполнить аутентификацию")
            return None
            
        url = f"{self.base_url}/activities"
        headers = self.get_headers()
        
        try:
            print(f"Отправляем запрос поиска активностей: {url}")
            print(f"Параметры: {params}")
            
            response = requests.get(url, headers=headers, params=params)
            
            print(f"Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Получено активностей: {len(data.get('data', []))}")
                return data
            else:
                print(f"Ошибка при поиске активностей: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
    
    def get_activity(self, activity_uuid):
        """Получить информацию об активности"""
        if not self.access_token:
            print("Необходимо сначала выполнить аутентификацию")
            return None
            
        url = f"{self.base_url}/activities/{activity_uuid}"
        headers = self.get_headers()
        
        try:
            print(f"Получаем информацию об активности: {url}")
            
            response = requests.get(url, headers=headers)
            
            print(f"Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Получена информация об активности: {data.get('title', 'N/A')}")
                return data
            else:
                print(f"Ошибка при получении активности: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

def demo_api_usage():
    """Демонстрация использования API"""
    print("=== ДЕМОНСТРАЦИЯ API MUSEMENT ===\n")
    
    # Примерные параметры (реальные значения предоставляются после подписания контракта)
    SANDBOX_BASE_URL = "https://sandbox-api.musement.com"  # Примерный URL
    APPLICATION_VALUE = "your-application-value"  # Предоставляется командой API distribution
    CLIENT_ID = "your-client-id"  # Предоставляется командой API distribution  
    CLIENT_SECRET = "your-client-secret"  # Предоставляется командой API distribution
    
    print("ВАЖНО: Для реального использования API необходимо:")
    print("1. Подписать контракт с Musement")
    print("2. Получить sandbox credentials от команды API distribution")
    print("3. Заменить примерные значения на реальные credentials\n")
    
    # Создаем клиент
    client = MusementAPIClient(
        base_url=SANDBOX_BASE_URL,
        application_value=APPLICATION_VALUE,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    
    print("1. АУТЕНТИФИКАЦИЯ")
    print("-" * 50)
    # В реальном случае здесь бы выполнялась аутентификация
    print("Попытка аутентификации...")
    print("(В демо-режиме - показываем только структуру запроса)")
    
    # Показываем, как выглядел бы запрос аутентификации
    auth_request_example = {
        "url": f"{SANDBOX_BASE_URL}/login",
        "method": "POST",
        "headers": {
            "X-Musement-Application": APPLICATION_VALUE,
            "X-Musement-Version": "3.4.0",
            "Content-Type": "application/json"
        },
        "body": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
    }
    
    print("Структура запроса аутентификации:")
    print(json.dumps(auth_request_example, indent=2))
    
    print("\n2. ПОИСК АКТИВНОСТЕЙ")
    print("-" * 50)
    
    # Показываем, как выглядел бы запрос поиска активностей
    search_request_example = {
        "url": f"{SANDBOX_BASE_URL}/activities",
        "method": "GET",
        "headers": {
            "X-Musement-Application": APPLICATION_VALUE,
            "X-Musement-Version": "3.4.0",
            "Authorization": "Bearer {access_token}"
        },
        "params": {
            "city_in": [1],  # Например, Рим
            "available_from": "2025-07-01",
            "available_to": "2025-07-31",
            "limit": 10
        }
    }
    
    print("Структура запроса поиска активностей:")
    print(json.dumps(search_request_example, indent=2))
    
    print("\n3. ПОЛУЧЕНИЕ ИНФОРМАЦИИ ОБ АКТИВНОСТИ")
    print("-" * 50)
    
    activity_request_example = {
        "url": f"{SANDBOX_BASE_URL}/activities/{{activity_uuid}}",
        "method": "GET", 
        "headers": {
            "X-Musement-Application": APPLICATION_VALUE,
            "X-Musement-Version": "3.4.0",
            "Authorization": "Bearer {access_token}"
        }
    }
    
    print("Структура запроса информации об активности:")
    print(json.dumps(activity_request_example, indent=2))
    
    print("\n=== РЕЗУЛЬТАТ ДЕМОНСТРАЦИИ ===")
    print("Демонстрационный скрипт показал структуру запросов к API Musement.")
    print("Для реального тестирования необходимы credentials от Musement.")

if __name__ == "__main__":
    demo_api_usage()

