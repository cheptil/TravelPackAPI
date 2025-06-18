# Примеры работы с Nominatim API

## Базовый класс для работы с API

```python
import requests
import time
import json
from typing import Dict, List, Optional

class NominatimClient:
    """Клиент для работы с Nominatim API"""
    
    def __init__(self, user_agent: str, base_url: str = "https://nominatim.openstreetmap.org"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': user_agent
        }
        self.last_request_time = 0
        self.min_request_interval = 1  # Минимальный интервал между запросами в секундах
    
    def _wait_if_needed(self):
        """Ожидание для соблюдения ограничений API"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def search(self, query: str = None, **params) -> List[Dict]:
        """
        Поиск места по запросу
        
        Args:
            query: Текст запроса для free-form поиска
            **params: Дополнительные параметры API
        
        Returns:
            Список найденных мест
        """
        self._wait_if_needed()
        
        url = f"{self.base_url}/search"
        
        # Параметры по умолчанию
        default_params = {
            'format': 'json',
            'addressdetails': 1,
            'limit': 10
        }
        
        # Объединяем параметры
        request_params = {**default_params, **params}
        
        if query:
            request_params['q'] = query
        
        try:
            response = requests.get(url, params=request_params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []
    
    def reverse(self, lat: float, lon: float, **params) -> Optional[Dict]:
        """
        Обратное геокодирование - поиск адреса по координатам
        
        Args:
            lat: Широта
            lon: Долгота
            **params: Дополнительные параметры API
        
        Returns:
            Информация о месте или None
        """
        self._wait_if_needed()
        
        url = f"{self.base_url}/reverse"
        
        request_params = {
            'format': 'json',
            'lat': lat,
            'lon': lon,
            'addressdetails': 1,
            **params
        }
        
        try:
            response = requests.get(url, params=request_params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка обратного геокодирования: {e}")
            return None
    
    def lookup(self, osm_ids: List[str], **params) -> List[Dict]:
        """
        Поиск деталей по OSM ID
        
        Args:
            osm_ids: Список OSM ID в формате [N|W|R]<id>
            **params: Дополнительные параметры API
        
        Returns:
            Список найденных объектов
        """
        self._wait_if_needed()
        
        url = f"{self.base_url}/lookup"
        
        request_params = {
            'format': 'json',
            'osm_ids': ','.join(osm_ids),
            'addressdetails': 1,
            **params
        }
        
        try:
            response = requests.get(url, params=request_params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка lookup: {e}")
            return []

# Примеры использования
if __name__ == "__main__":
    # Создаем клиент
    client = NominatimClient("MyApp/1.0 (contact@example.com)")
    
    # Пример 1: Простой поиск
    print("=== Простой поиск ===")
    results = client.search("Эйфелева башня, Париж")
    if results:
        place = results[0]
        print(f"Найдено: {place['display_name']}")
        print(f"Координаты: {place['lat']}, {place['lon']}")
    
    # Пример 2: Структурированный поиск
    print("\n=== Структурированный поиск ===")
    results = client.search(
        city="London",
        country="United Kingdom",
        limit=3
    )
    for result in results:
        print(f"- {result['display_name']}")
    
    # Пример 3: Обратное геокодирование
    print("\n=== Обратное геокодирование ===")
    place = client.reverse(55.7558, 37.6176)  # Координаты Красной площади
    if place:
        print(f"Адрес: {place['display_name']}")
    
    # Пример 4: Поиск с дополнительными параметрами
    print("\n=== Поиск с фильтрами ===")
    results = client.search(
        "restaurant",
        countrycodes="fr",
        bounded=1,
        viewbox="2.2,48.8,2.4,48.9",  # Ограничиваем поиск Парижем
        limit=5
    )
    print(f"Найдено ресторанов в Париже: {len(results)}")
```

## Полезные функции

```python
def extract_coordinates(result: Dict) -> tuple:
    """Извлекает координаты из результата"""
    return float(result['lat']), float(result['lon'])

def extract_address_components(result: Dict) -> Dict:
    """Извлекает компоненты адреса"""
    return result.get('address', {})

def get_country_code(result: Dict) -> str:
    """Получает код страны"""
    address = result.get('address', {})
    return address.get('country_code', '').upper()

def format_display_name(result: Dict, max_length: int = 100) -> str:
    """Форматирует отображаемое название с ограничением длины"""
    name = result.get('display_name', '')
    if len(name) <= max_length:
        return name
    return name[:max_length-3] + '...'

def filter_by_importance(results: List[Dict], min_importance: float = 0.3) -> List[Dict]:
    """Фильтрует результаты по важности"""
    return [r for r in results if r.get('importance', 0) >= min_importance]

def group_by_country(results: List[Dict]) -> Dict[str, List[Dict]]:
    """Группирует результаты по странам"""
    groups = {}
    for result in results:
        country = get_country_code(result)
        if country not in groups:
            groups[country] = []
        groups[country].append(result)
    return groups
```

## Обработка ошибок

```python
def safe_search(client: NominatimClient, query: str, retries: int = 3) -> List[Dict]:
    """Безопасный поиск с повторными попытками"""
    for attempt in range(retries):
        try:
            results = client.search(query)
            return results
        except Exception as e:
            print(f"Попытка {attempt + 1} неудачна: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Экспоненциальная задержка
    return []

def validate_coordinates(lat: float, lon: float) -> bool:
    """Проверяет корректность координат"""
    return -90 <= lat <= 90 and -180 <= lon <= 180
```

