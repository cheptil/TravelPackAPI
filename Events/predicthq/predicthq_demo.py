import requests
import json
from datetime import datetime, timedelta

# Демонстрационный скрипт для работы с PredictHQ Events API
# Показывает различные способы использования API

class PredictHQEventsAPI:
    def __init__(self, access_token=None):
        self.base_url = "https://api.predicthq.com/v1/events/"
        self.access_token = access_token
        self.headers = {
            "Accept": "application/json"
        }
        
        if access_token:
            self.headers["Authorization"] = f"Bearer {access_token}"
    
    def search_events(self, **params):
        """
        Поиск событий с заданными параметрами
        """
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_concerts_in_city(self, country="US", limit=10):
        """
        Получить концерты в указанной стране
        """
        params = {
            "category": "concerts",
            "country": country,
            "limit": limit,
            "sort": "rank"  # Сортировка по важности
        }
        return self.search_events(**params)
    
    def get_events_by_date_range(self, start_date, end_date, categories=None):
        """
        Получить события в указанном диапазоне дат
        """
        params = {
            "active.gte": start_date,
            "active.lte": end_date,
            "limit": 20
        }
        
        if categories:
            params["category"] = ",".join(categories)
            
        return self.search_events(**params)
    
    def search_by_keyword(self, keyword, limit=5):
        """
        Поиск событий по ключевому слову
        """
        params = {
            "q": keyword,
            "limit": limit
        }
        return self.search_events(**params)

def demonstrate_api_usage():
    """
    Демонстрация различных способов использования API
    """
    print("=== Демонстрация PredictHQ Events API ===\n")
    
    # Создаем экземпляр API без токена (для демонстрации)
    api = PredictHQEventsAPI()
    
    print("ВНИМАНИЕ: Для работы с API требуется валидный токен!")
    print("Получить токен можно на https://www.predicthq.com/\n")
    
    # Тест 1: Поиск концертов в США
    print("1. Поиск концертов в США:")
    print("   Параметры: category=concerts, country=US, limit=10")
    result1 = api.get_concerts_in_city("US", 10)
    print(f"   Статус: {result1.get('status_code', 'Ошибка')}")
    if result1.get('data'):
        print(f"   Ответ: {json.dumps(result1['data'], indent=4, ensure_ascii=False)}")
    print()
    
    # Тест 2: События в диапазоне дат
    print("2. События на следующие 30 дней:")
    today = datetime.now().strftime("%Y-%m-%d")
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    print(f"   Параметры: active.gte={today}, active.lte={future_date}")
    result2 = api.get_events_by_date_range(today, future_date, ["concerts", "festivals", "sports"])
    print(f"   Статус: {result2.get('status_code', 'Ошибка')}")
    if result2.get('data'):
        print(f"   Ответ: {json.dumps(result2['data'], indent=4, ensure_ascii=False)}")
    print()
    
    # Тест 3: Поиск по ключевому слову
    print("3. Поиск событий Taylor Swift:")
    print("   Параметры: q='taylor swift', limit=5")
    result3 = api.search_by_keyword("taylor swift", 5)
    print(f"   Статус: {result3.get('status_code', 'Ошибка')}")
    if result3.get('data'):
        print(f"   Ответ: {json.dumps(result3['data'], indent=4, ensure_ascii=False)}")
    print()
    
    # Анализ результатов
    print("=== Анализ результатов ===")
    all_results = [result1, result2, result3]
    
    for i, result in enumerate(all_results, 1):
        status = result.get('status_code')
        if status == 401:
            print(f"Тест {i}: ✓ API требует аутентификации (401)")
        elif status == 200:
            print(f"Тест {i}: ✓ Успешный запрос (200)")
            data = result.get('data', {})
            if isinstance(data, dict) and 'count' in data:
                print(f"         Найдено событий: {data['count']}")
        else:
            print(f"Тест {i}: ⚠ Статус {status}")
    
    print("\n=== Структура успешного ответа ===")
    print("""
При успешном запросе (статус 200) API возвращает JSON со следующей структурой:
{
  "count": 1,                    // Общее количество найденных событий
  "overflow": false,             // Превышен ли лимит результатов
  "previous": "...",             // URL предыдущей страницы
  "next": "...",                 // URL следующей страницы  
  "results": [                   // Массив событий
    {
      "id": "z13B3870YOgv",      // Уникальный ID события
      "title": "Katy Perry",     // Название события
      "category": "concerts",    // Категория события
      "start": "2025-06-17...",  // Время начала (UTC)
      "end": "2025-06-17...",    // Время окончания (UTC)
      "rank": 83,                // Ранг важности события
      "country": "US",           // Код страны
      "geo": {                   // Географические данные
        "geometry": {
          "type": "Point",
          "coordinates": [174.776792, -36.847319]
        },
        "address": {
          "formatted_address": "2350 Beach Blvd, Biloxi, MS 39531, USA",
          "locality": "Biloxi",
          "region": "Mississippi"
        }
      },
      "phq_attendance": 2511,    // Прогнозируемая посещаемость
      "predicted_event_spend": 11806680,  // Прогнозируемые расходы
      // ... другие поля
    }
  ]
}
    """)

if __name__ == "__main__":
    demonstrate_api_usage()

