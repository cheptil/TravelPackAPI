#!/usr/bin/env python3
"""
Тестирование найденного AXS API endpoint
"""

import requests
import json

def test_discovered_endpoint():
    """Тестирование найденного endpoint из JavaScript кода"""
    
    # Endpoint найденный в JavaScript коде
    url = "https://api.axs.com/proxy/v2/users/ipcheck"
    
    # Параметры из JavaScript
    params = {
        'access_token': '4f2be33d835e7197e245c54ff00e5fb4',
        'client_id': '18_50d269328df8a48be955f18831d1057e8937cc06213bd4644dcb6768a674c886',
        'client_secret': '0b0e17d487d53c3c9bc7ada7b97bc0e9b3afa08fee34c431f9c21f5fa7ffc260'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://api.axs.com/'
    }
    
    print("Тестирование найденного AXS API endpoint")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Параметры: {params}")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"\nСтатус код: {response.status_code}")
        print(f"Заголовки ответа:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print(f"\nТело ответа:")
        print(response.text)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\nJSON данные:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except:
                print("Не удалось декодировать JSON")
                
        # Попробуем без параметров аутентификации
        print(f"\n" + "=" * 40)
        print("Тестирование без параметров аутентификации")
        
        response_no_auth = requests.get(url, headers=headers, timeout=10)
        print(f"Статус без аутентификации: {response_no_auth.status_code}")
        print(f"Ответ: {response_no_auth.text[:200]}...")
        
    except Exception as e:
        print(f"Ошибка при запросе: {e}")

def explore_api_structure():
    """Исследование структуры API на основе найденного endpoint"""
    
    base_url = "https://api.axs.com/proxy/v2/"
    
    # Возможные endpoints на основе найденного паттерна
    endpoints = [
        "users/profile",
        "users/info", 
        "events",
        "events/search",
        "venues",
        "venues/search",
        "tickets",
        "tickets/search"
    ]
    
    # Параметры аутентификации из найденного запроса
    auth_params = {
        'access_token': '4f2be33d835e7197e245c54ff00e5fb4',
        'client_id': '18_50d269328df8a48be955f18831d1057e8937cc06213bd4644dcb6768a674c886',
        'client_secret': '0b0e17d487d53c3c9bc7ada7b97bc0e9b3afa08fee34c431f9c21f5fa7ffc260'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    print(f"\n" + "=" * 60)
    print("Исследование структуры API")
    print("=" * 60)
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            response = requests.get(url, params=auth_params, headers=headers, timeout=5)
            print(f"{response.status_code}: {url}")
            
            if response.status_code not in [403, 404]:
                print(f"  Ответ: {response.text[:100]}...")
                
        except Exception as e:
            print(f"Ошибка {url}: {e}")

if __name__ == "__main__":
    test_discovered_endpoint()
    explore_api_structure()

