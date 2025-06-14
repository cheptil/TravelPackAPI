import requests
import json
from datetime import datetime, timedelta

# Базовый URL для тестовой среды Amadeus
BASE_URL = "https://test.api.amadeus.com/v1"

def get_access_token(api_key, api_secret):
    """
    Получение access token через OAuth 2.0 Client Credentials Grant
    
    Args:
        api_key (str): API Key из панели управления Amadeus
        api_secret (str): API Secret из панели управления Amadeus
    
    Returns:
        str: Access token или None в случае ошибки
    """
    
    url = f"{BASE_URL}/security/oauth2/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    
    print("=== Запрос access token ===")
    print(f"URL: {url}")
    print(f"Данные: {data}")
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("Токен успешно получен:")
            print(json.dumps(token_data, indent=2))
            return token_data.get("access_token")
        else:
            print(f"Ошибка получения токена: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе токена: {e}")
        return None

def test_transfer_search_with_auth(api_key=None, api_secret=None):
    """
    Тестовый запрос к API Amadeus Transfer Search с авторизацией
    
    Args:
        api_key (str): API Key (если None, будет использован тестовый запрос без авторизации)
        api_secret (str): API Secret
    """
    
    # URL эндпоинта
    url = f"{BASE_URL}/shopping/transfer-offers"
    
    # Получаем access token, если предоставлены ключи
    access_token = None
    if api_key and api_secret:
        access_token = get_access_token(api_key, api_secret)
        if not access_token:
            print("Не удалось получить access token. Прерываем выполнение.")
            return
    
    # Заголовки запроса
    headers = {
        "Content-Type": "application/json"
    }
    
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    # Тестовые данные запроса
    # Трансфер из аэропорта CDG (Париж) до Эйфелевой башни
    request_data = {
        "startLocationCode": "CDG",  # Аэропорт Шарль де Голль
        "endAddressLine": "Avenue Anatole France, 5",
        "endCityName": "Paris",
        "endZipCode": "75007",
        "endCountryCode": "FR",
        "endName": "Eiffel Tower Area",
        "endGeoCode": "48.859466,2.2976965",
        "transferType": "PRIVATE",
        "startDateTime": "2024-12-15T14:30:00",  # Дата в будущем
        "passengers": 2
    }
    
    print("\n=== Тестовый запрос к Amadeus Transfer Search API ===")
    print(f"URL: {url}")
    print(f"Метод: POST")
    print(f"Заголовки: {json.dumps(headers, indent=2)}")
    print(f"Данные запроса:")
    print(json.dumps(request_data, indent=2))
    print("\n" + "="*50)
    
    try:
        # Выполняем запрос
        response = requests.post(url, headers=headers, json=request_data)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        # Пытаемся получить JSON ответ
        try:
            response_json = response.json()
            print(f"Ответ API:")
            print(json.dumps(response_json, indent=2))
            
            # Анализируем ответ
            if response.status_code == 200:
                analyze_transfer_response(response_json)
            
        except json.JSONDecodeError:
            print(f"Ответ (текст): {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

def analyze_transfer_response(response_data):
    """
    Анализ ответа API Transfer Search
    
    Args:
        response_data (dict): JSON ответ от API
    """
    print("\n=== АНАЛИЗ ОТВЕТА ===")
    
    if "data" in response_data:
        transfers = response_data["data"]
        print(f"Найдено предложений трансфера: {len(transfers)}")
        
        for i, transfer in enumerate(transfers, 1):
            print(f"\n--- Предложение {i} ---")
            print(f"ID: {transfer.get('id', 'N/A')}")
            print(f"Тип трансфера: {transfer.get('transferType', 'N/A')}")
            
            # Информация о начальной точке
            if "start" in transfer:
                start = transfer["start"]
                print(f"Начало: {start.get('locationCode', 'N/A')} в {start.get('dateTime', 'N/A')}")
            
            # Информация о конечной точке
            if "end" in transfer:
                end = transfer["end"]
                if "address" in end:
                    address = end["address"]
                    print(f"Назначение: {address.get('line', 'N/A')}, {address.get('cityName', 'N/A')}")
            
            # Информация о транспортном средстве
            if "vehicle" in transfer:
                vehicle = transfer["vehicle"]
                print(f"Транспорт: {vehicle.get('category', 'N/A')} - {vehicle.get('description', 'N/A')}")
            
            # Информация о цене
            if "quotation" in transfer:
                quotation = transfer["quotation"]
                if "monetaryAmount" in quotation:
                    amount = quotation["monetaryAmount"]
                    print(f"Цена: {amount.get('amount', 'N/A')} {amount.get('currencyCode', 'N/A')}")
    
    else:
        print("Данные о трансферах не найдены в ответе")

def demo_without_credentials():
    """
    Демонстрация работы без реальных учетных данных
    """
    print("=== ДЕМОНСТРАЦИЯ БЕЗ УЧЕТНЫХ ДАННЫХ ===")
    print("Для полного тестирования API необходимо:")
    print("1. Зарегистрироваться на https://developers.amadeus.com")
    print("2. Создать приложение в My Self-Service Workspace")
    print("3. Получить API Key и API Secret")
    print("4. Передать их в функцию test_transfer_search_with_auth()")
    print("\nВыполняем запрос без авторизации для демонстрации структуры ошибки:")
    
    test_transfer_search_with_auth()

if __name__ == "__main__":
    # Для тестирования с реальными ключами раскомментируйте и заполните:
    # API_KEY = "your_api_key_here"
    # API_SECRET = "your_api_secret_here"
    # test_transfer_search_with_auth(API_KEY, API_SECRET)
    
    # Демонстрация без ключей
    demo_without_credentials()

