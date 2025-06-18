# Анализ API GetYourGuide

## Общая информация
- **URL документации**: https://code.getyourguide.com/partner-api-spec/
- **Базовый URL Production**: https://api.getyourguide.com
- **Базовый URL Test**: https://api.gygtest.net
- **Формат**: RESTful API с JSON
- **Аутентификация**: Требуется API ключ (видна кнопка Authorize)

## Основные разделы API

### 1. Configuration
- `GET /configuration/{version}` - Получить конфигурацию для версии API
- `GET /{version}/configuration/payment` - Получить конфигурацию платежей

### 2. Bookings (Бронирования)
- `POST /{version}/bookings` - Создать новое бронирование
- `GET /{version}/bookings` - Получить все бронирования
- `GET /{version}/bookings/{booking_hash}` - Получить информацию о бронировании
- `DELETE /{version}/bookings/{booking_hash}` - Удалить (отменить) бронирование

### 3. Carts (Корзины)
- `POST /{version}/carts` - Подтвердить корзину покупок
- `GET /{version}/carts/{shopping_cart_hash}` - Получить информацию о корзине

### 4. Categories (Категории)
- `GET /{version}/categories` - Список всех категорий
- `GET /{version}/categories/{category_id}` - Получить информацию о категории

### 5. Options (Опции)
- `GET /{version}/options/{option_id}` - Получить информацию об опции

### 6. Reviews (Отзывы)
- `GET /{version}/reviews/tour/{tour_id}` - Получить отзывы о туре

### 7. Suppliers (Поставщики)
- `GET /{version}/suppliers/{supplier_id}` - Получить информацию о поставщике

### 8. Tours (Туры)
- `GET /{version}/tours` - Поиск туров по различным параметрам
- `GET /{version}/tours/{tour_id}` - Поиск туров по ID
- `GET /{version}/tours/{tour_id}/availability` - Найти доступность тура

## Для тестирования
Самый простой эндпоинт для тестирования: `GET /{version}/categories` - не требует дополнительных параметров.


## Результаты тестирования API

### Тестовый запрос через Swagger UI

**Эндпоинт**: `GET /1/categories`
**Параметры**:
- version: 1
- cnt_language: en
- currency: USD
- limit: 10
- offset: 0

**Результат**: Ошибка 401 - Unauthorized

### Тестовый запрос через Python

**URL**: `https://api.getyourguide.com/1/categories?cnt_language=en&currency=USD&limit=10&offset=0`
**Статус код**: 401
**Ответ API**:
```json
{
  "descriptor": "GetYourGuide AG",
  "apiVersion": "1",
  "method": "/1/categories",
  "status": "ERROR",
  "query": "cnt_language=en&currency=USD&limit=10&offset=0",
  "errors": [
    {
      "errorCode": 0,
      "errorMessage": "The X-ACCESS-TOKEN header is missing."
    }
  ],
  "helpURL": "https://api.getyourguide.com/doc",
  "date": "2025-06-18T13:38:13.001610318Z"
}
```

## Анализ результатов

### Ключевые выводы

1. **Аутентификация обязательна**: API требует заголовок `X-ACCESS-TOKEN` для всех запросов
2. **Структурированные ошибки**: API возвращает детальную информацию об ошибках в JSON формате
3. **Версионирование**: API использует версионирование в URL (например, `/1/categories`)
4. **Стандартные HTTP коды**: Используются стандартные коды ответов (401 для неавторизованного доступа)

### Структура ответа API

API GetYourGuide использует консистентную структуру ответов:

```json
{
  "descriptor": "GetYourGuide AG",
  "apiVersion": "версия_api",
  "method": "вызванный_метод",
  "status": "статус_ответа",
  "query": "параметры_запроса",
  "errors": [массив_ошибок],
  "helpURL": "ссылка_на_документацию",
  "date": "временная_метка"
}
```

### Требования для работы с API

1. **API ключ**: Необходимо получить API ключ от GetYourGuide
2. **Заголовки**: Обязательный заголовок `X-ACCESS-TOKEN`
3. **Формат данных**: JSON для запросов и ответов
4. **HTTPS**: Все запросы должны использовать HTTPS

### Рекомендации по использованию

#### Обработка ошибок
```python
def handle_api_response(response):
    if response.status_code == 401:
        print("Ошибка аутентификации: проверьте API ключ")
    elif response.status_code == 400:
        print("Неверные параметры запроса")
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"Неожиданная ошибка: {response.status_code}")
```

#### Правильная настройка заголовков
```python
headers = {
    'X-ACCESS-TOKEN': 'ваш_api_ключ',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
```

#### Пагинация
API поддерживает пагинацию через параметры `limit` и `offset`:
- `limit`: количество записей на страницу (по умолчанию 10)
- `offset`: смещение от начала (по умолчанию 0)

#### Локализация
API поддерживает множественные языки и валюты:
- **Языки**: da, de, en, es, fr, it, ko, nl, no, pl, pt, fi, sv, ru, ja, ar
- **Валюты**: USD, EUR, GBP, и многие другие

## Практические примеры использования

### Получение категорий туров
```python
# С аутентификацией
client = GetYourGuideAPI("ваш_api_ключ")
categories = client.get_categories(
    language="ru",
    currency="EUR",
    limit=20
)
```

### Поиск туров
```python
# Поиск туров в определенном городе
tours = client.get_tours(
    language="en",
    currency="USD",
    q="Paris",  # поисковый запрос
    limit=10
)
```

### Получение информации о туре
```python
# Получение деталей конкретного тура
tour_details = client.get_tour_details(tour_id=12345)
```

## Заключение

API GetYourGuide представляет собой хорошо структурированный RESTful API с:
- Четкой документацией в формате OpenAPI/Swagger
- Консистентной структурой ответов
- Подробной информацией об ошибках
- Поддержкой множественных языков и валют
- Стандартными HTTP методами и кодами ответов

Для начала работы необходимо:
1. Получить API ключ от GetYourGuide
2. Настроить правильные заголовки аутентификации
3. Изучить доступные эндпоинты в документации
4. Реализовать обработку ошибок в своем приложении

API подходит для интеграции в туристические приложения, сайты бронирования и другие сервисы, связанные с туризмом и развлечениями.

