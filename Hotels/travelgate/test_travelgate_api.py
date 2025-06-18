#!/usr/bin/env python3
"""
Тестовый скрипт для выполнения запроса к TravelGate GraphQL API
"""

import requests
import json

# Конфигурация API
API_URL = "https://api.travelgate.com/graphql"
API_KEY = "test0000-0000-0000-0000-0000"

# GraphQL запрос для получения информации об отелях
QUERY = """
query {
  hotelX {
    hotels(criteria: {access: 7245}) {
      edges {
        node {
          hotelData {
            hotelName
            hotelCode
            categoryCode
            location {
              city
              country
              coordinates {
                latitude
                longitude
              }
            }
          }
        }
      }
    }
  }
}
"""

def make_graphql_request():
    """Выполняет GraphQL запрос к TravelGate API"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Apikey {API_KEY}"
    }
    
    payload = {
        "query": QUERY
    }
    
    try:
        print("Выполняю запрос к TravelGate API...")
        print(f"URL: {API_URL}")
        print(f"Headers: {headers}")
        print(f"Query: {QUERY}")
        print("-" * 50)
        
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            result = response.json()
            print("Успешный ответ:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        else:
            print(f"Ошибка HTTP {response.status_code}:")
            print(response.text)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        print(f"Ответ сервера: {response.text}")
        return None

def analyze_response(response_data):
    """Анализирует ответ от API"""
    if not response_data:
        return "Нет данных для анализа"
    
    analysis = []
    analysis.append("=== АНАЛИЗ ОТВЕТА API ===")
    
    # Проверяем наличие ошибок
    if "errors" in response_data:
        analysis.append("ОШИБКИ:")
        for error in response_data["errors"]:
            analysis.append(f"- {error.get('message', 'Неизвестная ошибка')}")
    
    # Анализируем данные
    if "data" in response_data:
        data = response_data["data"]
        if data and "hotelX" in data and data["hotelX"]:
            hotels_data = data["hotelX"].get("hotels", {})
            edges = hotels_data.get("edges", [])
            
            analysis.append(f"КОЛИЧЕСТВО ОТЕЛЕЙ: {len(edges)}")
            
            if edges:
                analysis.append("ПРИМЕРЫ ОТЕЛЕЙ:")
                for i, edge in enumerate(edges[:5]):  # Показываем первые 5
                    hotel = edge.get("node", {}).get("hotelData", {})
                    name = hotel.get("hotelName", "Не указано")
                    code = hotel.get("hotelCode", "Не указано")
                    category = hotel.get("categoryCode", "Не указано")
                    location = hotel.get("location", {})
                    city = location.get("city", "Не указано")
                    country = location.get("country", "Не указано")
                    
                    analysis.append(f"{i+1}. {name} ({code})")
                    analysis.append(f"   Категория: {category}")
                    analysis.append(f"   Местоположение: {city}, {country}")
        else:
            analysis.append("ДАННЫЕ: Нет данных об отелях")
    else:
        analysis.append("ДАННЫЕ: Отсутствуют")
    
    return "\n".join(analysis)

if __name__ == "__main__":
    print("=== ТЕСТИРОВАНИЕ TRAVELGATE API ===")
    
    # Выполняем запрос
    response = make_graphql_request()
    
    # Анализируем результат
    analysis = analyze_response(response)
    print("\n" + analysis)
    
    # Сохраняем результат в файл
    with open("/home/ubuntu/travelgate_api_response.json", "w", encoding="utf-8") as f:
        if response:
            json.dump(response, f, indent=2, ensure_ascii=False)
        else:
            json.dump({"error": "Не удалось получить ответ от API"}, f, indent=2, ensure_ascii=False)
    
    print(f"\nРезультат сохранен в файл: /home/ubuntu/travelgate_api_response.json")

