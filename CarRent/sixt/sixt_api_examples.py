# Примеры использования API Sixt

## Базовая настройка

```python
import requests
import json

# Базовый URL API
BASE_URL = "https://api.orange.sixt.com/v1"

# Настройка сессии для повторного использования соединений
session = requests.Session()
session.headers.update({
    'User-Agent': 'SixtAPIClient/1.0',
    'Accept': 'application/json'
})
```

## 1. Поиск станций

```python
def search_stations(term, vehicle_type='car', location_type='station'):
    """
    Поиск станций Sixt по названию города или адресу
    
    Args:
        term (str): Поисковый запрос (город, адрес)
        vehicle_type (str): Тип транспорта ('car' или 'truck')
        location_type (str): Тип локации ('station')
    
    Returns:
        list: Список найденных станций
    """
    url = f"{BASE_URL}/locations"
    params = {
        'term': term,
        'vehicleType': vehicle_type,
        'type': location_type
    }
    
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при поиске станций: {e}")
        return []

# Пример использования
stations = search_stations("Munich")
for station in stations[:5]:
    print(f"ID: {station['id']}, Название: {station['title']}")
```

## 2. Получение деталей станции

```python
def get_station_details(station_id):
    """
    Получение подробной информации о станции
    
    Args:
        station_id (str): ID станции (например, 'S_5252')
    
    Returns:
        dict: Детальная информация о станции
    """
    url = f"{BASE_URL}/locations/{station_id}"
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении деталей станции: {e}")
        return None

# Пример использования
station_details = get_station_details("S_5252")
if station_details:
    print(f"Станция: {station_details['title']}")
    print(f"Адрес: {station_details['subtitle']}")
    print(f"Координаты: {station_details['coordinates']}")
    print(f"Типы услуг: {station_details['subtypes']}")
```

## 3. Поиск ближайших станций

```python
def find_nearest_stations(city, max_results=10):
    """
    Поиск ближайших станций в указанном городе
    
    Args:
        city (str): Название города
        max_results (int): Максимальное количество результатов
    
    Returns:
        list: Список ближайших станций с деталями
    """
    stations = search_stations(city)
    nearest_stations = []
    
    for station in stations[:max_results]:
        details = get_station_details(station['id'])
        if details:
            nearest_stations.append({
                'id': station['id'],
                'title': station['title'],
                'address': station['subtitle'],
                'coordinates': details.get('coordinates', {}),
                'services': details.get('subtypes', [])
            })
    
    return nearest_stations

# Пример использования
munich_stations = find_nearest_stations("Munich", 5)
for i, station in enumerate(munich_stations, 1):
    print(f"{i}. {station['title']}")
    print(f"   Адрес: {station['address']}")
    print(f"   Услуги: {', '.join(station['services'])}")
    print()
```

## 4. Фильтрация станций по типу услуг

```python
def filter_stations_by_service(city, required_service):
    """
    Поиск станций с определенным типом услуг
    
    Args:
        city (str): Название города
        required_service (str): Требуемая услуга (например, 'eCar', 'airport', 'delivery')
    
    Returns:
        list: Станции с требуемой услугой
    """
    stations = search_stations(city)
    filtered_stations = []
    
    for station in stations:
        if required_service in station.get('subtypes', []):
            details = get_station_details(station['id'])
            if details:
                filtered_stations.append(details)
    
    return filtered_stations

# Пример использования - поиск станций с электромобилями
ecar_stations = filter_stations_by_service("Munich", "eCar")
print(f"Найдено станций с электромобилями: {len(ecar_stations)}")
for station in ecar_stations[:3]:
    print(f"- {station['title']}: {station['subtitle']}")
```

## 5. Обработка ошибок и повторные попытки

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """Декоратор для повторных попыток при ошибках"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Попытка {attempt + 1} неудачна: {e}")
                    time.sleep(delay * (2 ** attempt))  # Экспоненциальная задержка
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=1)
def robust_search_stations(term):
    """Надежный поиск станций с повторными попытками"""
    return search_stations(term)
```

## 6. Полный пример приложения

```python
def main():
    """Основная функция демонстрации API"""
    print("=== Демонстрация API Sixt ===\n")
    
    # 1. Поиск станций в Мюнхене
    print("1. Поиск станций в Мюнхене:")
    munich_stations = search_stations("Munich")
    print(f"Найдено станций: {len(munich_stations)}\n")
    
    # 2. Показать первые 3 станции с деталями
    print("2. Топ-3 станции с подробностями:")
    for i, station in enumerate(munich_stations[:3], 1):
        details = get_station_details(station['id'])
        if details:
            print(f"{i}. {details['title']}")
            print(f"   ID: {details['id']}")
            print(f"   Адрес: {details['subtitle']}")
            coords = details.get('coordinates', {})
            if coords:
                print(f"   Координаты: {coords['latitude']}, {coords['longitude']}")
            print(f"   Услуги: {', '.join(details.get('subtypes', []))}")
            print()
    
    # 3. Поиск станций с электромобилями
    print("3. Станции с электромобилями:")
    ecar_stations = filter_stations_by_service("Munich", "eCar")
    for station in ecar_stations[:3]:
        print(f"- {station['title']}")
    
    print("\n=== Демонстрация завершена ===")

if __name__ == "__main__":
    main()
```

## Заметки по использованию

1. **Лимиты запросов**: API может иметь ограничения на количество запросов в минуту
2. **Кэширование**: Рекомендуется кэшировать результаты поиска станций
3. **Обработка ошибок**: Всегда проверяйте статус ответа и обрабатывайте исключения
4. **Таймауты**: Устанавливайте разумные таймауты для запросов (10-30 секунд)
5. **User-Agent**: Используйте осмысленный User-Agent для идентификации вашего приложения

