#!/usr/bin/env python3
"""
Пример работы с API SevenRooms
Основан на результатах тестирования и анализа
"""

import requests
import json
from datetime import datetime, timedelta

class SevenRoomsAPI:
    """
    Класс для работы с API SevenRooms
    """
    
    def __init__(self, base_url, client_id, client_secret, venue_group_id):
        """
        Инициализация API клиента
        
        Args:
            base_url (str): Базовый URL API (например, https://api.sevenrooms.com/api-ext/2_2)
            client_id (str): Идентификатор клиента
            client_secret (str): Секретный ключ клиента  
            venue_group_id (str): Идентификатор группы заведений
        """
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.venue_group_id = venue_group_id
        self.access_token = None
        
    def authenticate(self):
        """
        Выполняет аутентификацию и получает токен доступа
        
        Returns:
            bool: True если аутентификация успешна, False иначе
        """
        auth_url = f"{self.base_url}/auth"
        auth_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(auth_url, json=auth_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                return True
            else:
                print(f"Ошибка аутентификации: {response.status_code}")
                print(f"Ответ: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения при аутентификации: {e}")
            return False
    
    def _make_request(self, endpoint, params=None, method='GET'):
        """
        Выполняет запрос к API
        
        Args:
            endpoint (str): Эндпоинт API
            params (dict): Параметры запроса
            method (str): HTTP метод
            
        Returns:
            dict: Ответ API или None в случае ошибки
        """
        if not self.access_token:
            if not self.authenticate():
                return None
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Добавляем venue_group_id к параметрам если не указан
        if params is None:
            params = {}
        if 'venue_group_id' not in params:
            params['venue_group_id'] = self.venue_group_id
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, json=params, headers=headers, timeout=30)
            else:
                raise ValueError(f"Неподдерживаемый HTTP метод: {method}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Токен истек, попробуем переаутентифицироваться
                if self.authenticate():
                    headers['Authorization'] = f'Bearer {self.access_token}'
                    if method.upper() == 'GET':
                        response = requests.get(url, params=params, headers=headers, timeout=30)
                    else:
                        response = requests.post(url, json=params, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        return response.json()
            
            print(f"Ошибка API: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return None
    
    def get_venues(self):
        """
        Получает список заведений
        
        Returns:
            list: Список заведений
        """
        return self._make_request('venues')
    
    def get_reservations(self, start_date=None, end_date=None, limit=100):
        """
        Получает список бронирований
        
        Args:
            start_date (str): Начальная дата в формате YYYY-MM-DD
            end_date (str): Конечная дата в формате YYYY-MM-DD  
            limit (int): Максимальное количество записей
            
        Returns:
            list: Список бронирований
        """
        params = {'limit': limit}
        
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        return self._make_request('reservations', params)
    
    def get_clients(self, updated_since=None, limit=100):
        """
        Получает список клиентов
        
        Args:
            updated_since (str): Дата последнего обновления в формате YYYY-MM-DD
            limit (int): Максимальное количество записей
            
        Returns:
            list: Список клиентов
        """
        params = {'limit': limit}
        
        if updated_since:
            params['updated_since'] = updated_since
            
        return self._make_request('clients', params)

# Пример использования
def example_usage():
    """
    Пример использования API SevenRooms
    """
    
    # Инициализация API клиента
    api = SevenRoomsAPI(
        base_url="https://api.sevenrooms.com/api-ext/2_2",  # Замените на реальный URL
        client_id="ваш_client_id",  # Замените на реальный client_id
        client_secret="ваш_client_secret",  # Замените на реальный client_secret
        venue_group_id="ваш_venue_group_id"  # Замените на реальный venue_group_id
    )
    
    # Получение списка заведений
    print("Получение списка заведений...")
    venues = api.get_venues()
    if venues:
        print(f"Найдено заведений: {len(venues)}")
        print(json.dumps(venues[:2], indent=2))  # Показываем первые 2
    
    # Получение бронирований за последнюю неделю
    print("\nПолучение бронирований...")
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    reservations = api.get_reservations(start_date=start_date, end_date=end_date)
    if reservations:
        print(f"Найдено бронирований: {len(reservations)}")
        print(json.dumps(reservations[:2], indent=2))  # Показываем первые 2
    
    # Получение списка клиентов
    print("\nПолучение списка клиентов...")
    clients = api.get_clients(limit=50)
    if clients:
        print(f"Найдено клиентов: {len(clients)}")
        print(json.dumps(clients[:2], indent=2))  # Показываем первых 2

if __name__ == "__main__":
    print("=== Пример работы с API SevenRooms ===")
    print("ВНИМАНИЕ: Для работы требуются реальные учетные данные!")
    print("Получите их у представителя SevenRooms.")
    print()
    
    # Раскомментируйте следующую строку после получения реальных учетных данных
    # example_usage()

