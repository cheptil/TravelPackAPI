#!/usr/bin/env python3
"""
Детальный анализ AXS API endpoint
"""

import requests
import json

def detailed_api_analysis():
    """Детальный анализ API endpoint с ошибкой 403"""
    
    url = "https://api.axs.com/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    
    print("Детальный анализ AXS API")
    print("=" * 50)
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Статус код: {response.status_code}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print(f"\nТело ответа:")
        print(response.text)
        
        # Попробуем разные методы HTTP
        methods = ['POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
        print(f"\nТестирование других HTTP методов:")
        
        for method in methods:
            try:
                resp = requests.request(method, url, headers=headers, timeout=5)
                print(f"  {method}: {resp.status_code}")
                if resp.status_code != 403:
                    print(f"    Ответ: {resp.text[:100]}")
            except Exception as e:
                print(f"  {method}: Ошибка - {e}")
        
        # Попробуем с разными заголовками аутентификации
        print(f"\nТестирование с заголовками аутентификации:")
        
        auth_headers = [
            {'Authorization': 'Bearer test'},
            {'Authorization': 'Basic test'},
            {'X-API-Key': 'test'},
            {'X-Auth-Token': 'test'},
            {'API-Key': 'test'}
        ]
        
        for auth_header in auth_headers:
            test_headers = {**headers, **auth_header}
            try:
                resp = requests.get(url, headers=test_headers, timeout=5)
                auth_type = list(auth_header.keys())[0]
                print(f"  {auth_type}: {resp.status_code}")
                if resp.status_code != 403:
                    print(f"    Ответ: {resp.text[:100]}")
            except Exception as e:
                print(f"  {auth_type}: Ошибка - {e}")
                
    except Exception as e:
        print(f"Ошибка при запросе: {e}")

def test_public_endpoints():
    """Тестирование возможных публичных endpoints"""
    
    public_endpoints = [
        "https://www.axs.com/",
        "https://www.axs.com/events",
        "https://www.axs.com/venues", 
        "https://www.axs.com/search",
        "https://api.axs.com/public/events",
        "https://api.axs.com/public/venues"
    ]
    
    print("\n" + "=" * 50)
    print("Тестирование публичных endpoints")
    print("=" * 50)
    
    for endpoint in public_endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            print(f"{response.status_code}: {endpoint}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        print(f"  JSON данные найдены: {len(str(data))} символов")
                        print(f"  Превью: {str(data)[:200]}...")
                    except:
                        print("  Не удалось декодировать JSON")
                else:
                    print(f"  HTML/текст: {len(response.text)} символов")
                    
        except Exception as e:
            print(f"Ошибка {endpoint}: {e}")

if __name__ == "__main__":
    detailed_api_analysis()
    test_public_endpoints()

