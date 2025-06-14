#!/usr/bin/env python3

import urllib.request
import urllib.parse
import json

def simple_foursquare_test():
    """Простой тест Foursquare API без внешних библиотек"""
    
    # Параметры
    base_url = "https://api.foursquare.com/v3/places/search"
    params = {
        "query": "coffee",
        "ll": "55.7558,37.6176",
        "limit": "3"
    }
    
    # Создаем URL с параметрами
    url = base_url + "?" + urllib.parse.urlencode(params)
    
    print("=== Простой тест Foursquare API ===")
    print(f"URL: {url}")
    
    try:
        # Создаем запрос
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/json')
        
        print("Выполняю запрос...")
        
        # Выполняем запрос
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            data = response.read().decode('utf-8')
            
            print(f"Статус код: {status_code}")
            print("Ответ:")
            print(data[:500] + "..." if len(data) > 500 else data)
            
    except urllib.error.HTTPError as e:
        print(f"HTTP ошибка: {e.code}")
        print(f"Сообщение: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"URL ошибка: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")

if __name__ == "__main__":
    simple_foursquare_test()

