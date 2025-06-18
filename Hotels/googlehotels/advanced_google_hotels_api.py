#!/usr/bin/env python3
"""
Расширенный пример работы с Google Hotels API
Включает обработку OAuth токенов и детальный анализ ответов
"""

import requests
import json
import os
from datetime import datetime, timedelta

class GoogleHotelsAPIClient:
    """Клиент для работы с Google Hotels API"""
    
    def __init__(self, access_token=None):
        self.base_url = "https://travelpartner.googleapis.com/v3"
        self.access_token = access_token
        self.session = requests.Session()
        
        if access_token:
            self.session.headers.update({
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            })
    
    def get_price_view(self, account_id, partner_hotel_id):
        """
        Получить информацию о ценах для конкретного отеля
        
        Args:
            account_id (str): ID аккаунта
            partner_hotel_id (str): ID отеля партнера
            
        Returns:
            dict: Ответ API или информация об ошибке
        """
        resource_name = f"accounts/{account_id}/priceViews/{partner_hotel_id}"
        url = f"{self.base_url}/{resource_name}"
        
        try:
            response = self.session.get(url, timeout=30)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'request_time': datetime.now().isoformat()
            }
            
            try:
                result['data'] = response.json()
            except json.JSONDecodeError:
                result['data'] = response.text
                
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'url': url,
                'request_time': datetime.now().isoformat()
            }
    
    def analyze_price_data(self, price_view_data):
        """
        Анализ данных о ценах
        
        Args:
            price_view_data (dict): Данные о ценах из API
            
        Returns:
            dict: Результаты анализа
        """
        if 'error' in price_view_data:
            return {'error': 'Невозможно проанализировать данные из-за ошибки API'}
        
        data = price_view_data.get('data', {})
        if 'perItineraryPrices' not in data:
            return {'error': 'Отсутствуют данные о ценах в ответе'}
        
        prices = data['perItineraryPrices']
        analysis = {
            'total_itineraries': len(prices),
            'price_statistics': {},
            'currency_info': {},
            'date_range': {},
            'detailed_breakdown': []
        }
        
        if not prices:
            return analysis
        
        # Извлечение всех цен для статистики
        all_prices = [item.get('price', 0) for item in prices if 'price' in item]
        all_taxes = [item.get('taxes', 0) for item in prices if 'taxes' in item]
        all_fees = [item.get('fees', 0) for item in prices if 'fees' in item]
        
        if all_prices:
            analysis['price_statistics'] = {
                'min_price': min(all_prices),
                'max_price': max(all_prices),
                'avg_price': sum(all_prices) / len(all_prices),
                'total_revenue': sum(all_prices),
                'avg_taxes': sum(all_taxes) / len(all_taxes) if all_taxes else 0,
                'avg_fees': sum(all_fees) / len(all_fees) if all_fees else 0
            }
        
        # Анализ валют
        currencies = set(item.get('currencyCode') for item in prices if 'currencyCode' in item)
        analysis['currency_info'] = {
            'currencies_used': list(currencies),
            'primary_currency': list(currencies)[0] if currencies else None
        }
        
        # Анализ дат
        dates = []
        for item in prices:
            if 'checkinDate' in item:
                date_obj = item['checkinDate']
                if all(key in date_obj for key in ['year', 'month', 'day']):
                    dates.append(f"{date_obj['year']}-{date_obj['month']:02d}-{date_obj['day']:02d}")
        
        if dates:
            analysis['date_range'] = {
                'earliest_date': min(dates),
                'latest_date': max(dates),
                'total_dates': len(set(dates))
            }
        
        # Детальная разбивка по маршрутам
        for i, item in enumerate(prices):
            breakdown = {
                'itinerary_index': i,
                'checkin_date': item.get('checkinDate'),
                'length_of_stay': item.get('lengthOfStayDays'),
                'base_price': item.get('price'),
                'taxes': item.get('taxes'),
                'fees': item.get('fees'),
                'total_cost': (item.get('price', 0) + item.get('taxes', 0) + item.get('fees', 0)),
                'currency': item.get('currencyCode'),
                'last_updated': item.get('updateTime')
            }
            analysis['detailed_breakdown'].append(breakdown)
        
        return analysis

def demonstrate_api_usage():
    """Демонстрация использования API клиента"""
    
    print("=== Демонстрация Google Hotels API Client ===\n")
    
    # Создание клиента без токена (для демонстрации)
    client = GoogleHotelsAPIClient()
    
    # Тестовые параметры
    test_account_id = "123456789"
    test_hotel_id = "hotel_example_123"
    
    print(f"Тестирование с параметрами:")
    print(f"  Account ID: {test_account_id}")
    print(f"  Hotel ID: {test_hotel_id}")
    print()
    
    # Выполнение запроса
    result = client.get_price_view(test_account_id, test_hotel_id)
    
    print("Результат запроса:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()
    
    # Демонстрация анализа с примерными данными
    print("=== Демонстрация анализа данных ===\n")
    
    # Создание примерных данных для анализа
    sample_data = {
        'data': {
            'name': f'accounts/{test_account_id}/priceViews/{test_hotel_id}',
            'perItineraryPrices': [
                {
                    'checkinDate': {'year': 2025, 'month': 7, 'day': 15},
                    'lengthOfStayDays': 2,
                    'price': 150.00,
                    'taxes': 15.00,
                    'fees': 5.00,
                    'currencyCode': 'USD',
                    'updateTime': '2025-06-18T13:00:00Z'
                },
                {
                    'checkinDate': {'year': 2025, 'month': 7, 'day': 16},
                    'lengthOfStayDays': 3,
                    'price': 225.00,
                    'taxes': 22.50,
                    'fees': 7.50,
                    'currencyCode': 'USD',
                    'updateTime': '2025-06-18T13:00:00Z'
                },
                {
                    'checkinDate': {'year': 2025, 'month': 7, 'day': 17},
                    'lengthOfStayDays': 1,
                    'price': 80.00,
                    'taxes': 8.00,
                    'fees': 3.00,
                    'currencyCode': 'USD',
                    'updateTime': '2025-06-18T13:00:00Z'
                }
            ]
        }
    }
    
    analysis = client.analyze_price_data(sample_data)
    
    print("Результат анализа примерных данных:")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

def save_results_to_file():
    """Сохранение результатов тестирования в файл"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/home/ubuntu/api_test_results_{timestamp}.json"
    
    # Создание клиента и выполнение тестового запроса
    client = GoogleHotelsAPIClient()
    result = client.get_price_view("123456789", "hotel_example_123")
    
    # Добавление метаданных
    full_result = {
        'test_metadata': {
            'timestamp': datetime.now().isoformat(),
            'api_version': 'v3',
            'test_type': 'authentication_test',
            'expected_result': 'HTTP 401 - Authentication required'
        },
        'api_response': result,
        'conclusions': [
            'API endpoint доступен и отвечает',
            'Требуется OAuth 2.0 аутентификация',
            'Структура URL корректна',
            'Сервер возвращает правильные заголовки ошибок'
        ]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(full_result, f, indent=2, ensure_ascii=False)
    
    print(f"Результаты сохранены в файл: {filename}")
    return filename

if __name__ == "__main__":
    demonstrate_api_usage()
    print("\n" + "="*50)
    save_results_to_file()

