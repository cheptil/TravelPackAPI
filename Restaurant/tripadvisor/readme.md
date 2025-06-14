# TripAdvisor Content API - Обзор

## Основная информация
- **URL документации**: https://tripadvisor-content-api.readme.io/reference/overview
- **Версия API**: v1.0
- **Тип**: Partner API для доступа к контенту TripAdvisor

## Возможности API
- Доступ к деталям локаций и до 5 отзывов и 5 фотографий на локацию
- До 50 вызовов в секунду
- Оплата только за использование
- Возможность установки дневного лимита для контроля бюджета
- Ежемесячная оплата, отмена в любое время

## Доступные эндпоинты

### 1. Location Details
Предоставляет доступ к полной информации о локации:
- Название, адрес, рейтинг
- URL для листинга на TripAdvisor

### 2. Location Photos  
Предоставляет доступ к высококачественным фотографиям локации

### 3. Location Reviews
Предоставляет самые свежие отзывы для конкретной локации

### 4. Location Search
Возвращает список локаций по поисковому запросу

### 5. Nearby Location Search
Возвращает список локаций рядом с заданными координатами (широта/долгота)

## Типы локаций
API поддерживает следующие типы локаций:
- Отели (hotels)
- Рестораны (restaurants) 
- Достопримечательности (attractions)

## Модель оплаты
- Pay monthly, cancel anytime (ежемесячная оплата, отмена в любое время)
- Оплата только за фактическое использование
- Возможность установки дневных лимитов для контроля расходов



## Аутентификация

### Процесс получения API ключа:
1. Перейти на www.tripadvisor.com/developers
2. Зарегистрироваться для получения аккаунта TripAdvisor
3. Нажать "Create API key"

### Использование API ключа:
- Content API использует API ключи для аутентификации запросов
- Все API запросы должны выполняться через HTTPS
- API ключ передается как параметр "key" в query string

### Безопасность API ключа:
⚠️ **Важно**: Необходимо защищать ваш ключ доступа
- Включать его в каждый запрос как значение параметра "key"
- При выполнении API вызовов из клиентского кода, учитывать что это может раскрыть ключ другим скриптам и расширениям браузера
- TripAdvisor оставляет за собой право отозвать ключ доступа в любое время и выдать новый, если ключ был скомпрометирован или используется неправильно

### Формат запроса:
```
https://api.content.tripadvisor.com/api/v1/location/{locationId}?key=YOUR_API_KEY
```


## Структура API запросов

### Location Details API
**Эндпоинт**: `GET https://api.content.tripadvisor.com/api/v1/location/{locationId}/details`

**Обязательные параметры**:
- `locationId` (int32) - Уникальный идентификатор локации в TripAdvisor
- `key` (string) - Partner API Key

**Опциональные параметры**:
- `language` (string) - Язык ответа (по умолчанию "en")
- `currency` (string) - Код валюты (по умолчанию "USD")

### Пример cURL запроса:
```bash
curl --request GET \
  --url 'https://api.content.tripadvisor.com/api/v1/location/{locationId}/details?key=YOUR_API_KEY' \
  --header 'accept: application/json'
```

### Пример ответа (200 OK):
```json
{
  "location_id": 0,
  "name": "string",
  "description": "string",
  "web_url": "string",
  "address_obj": {
    "street1": "string",
    "street2": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "postalcode": "string",
    "address_string": "string"
  },
  "ancestors": [
    {
      "abbrv": "string",
      "level": "string",
      "name": "string",
      "location_id": 0
    }
  ],
  "latitude": 0,
  "longitude": 0,
  "timezone": "string",
  "email": "string",
  "phone": "string",
  "website": "string",
  "write_review": "string",
  "ranking_data": {
    "geo_location_id": 0,
    "ranking_string": "string",
    "geo_location_name": "string",
    "ranking_out_of": 0,
    "ranking": 0
  }
}
```


## Результаты тестового запроса

### Выполненный тест
Был создан и выполнен тестовый Python скрипт для демонстрации работы с TripAdvisor Content API.

**Параметры тестового запроса**:
- URL: `https://api.content.tripadvisor.com/api/v1/location/60763/details`
- API ключ: `TEST_API_KEY_DEMO` (тестовый, нерабочий)
- Location ID: `60763` (тестовый идентификатор)
- Язык: `en`
- Валюта: `USD`

### Результат запроса
```json
{
  "status_code": 403,
  "headers": {
    "Date": "Sat, 14 Jun 2025 16:37:19 GMT",
    "Content-Type": "application/json",
    "Content-Length": "83",
    "Connection": "keep-alive",
    "x-amzn-RequestId": "fa22d141-4db4-4621-bbb2-512844a59007",
    "x-amzn-ErrorType": "AccessDeniedException",
    "x-amz-apigw-id": "MKbB-HYDIAMEq0w=",
    "X-Amzn-Trace-Id": "Root=1-684da53f-4a0f38c62c3e7345288b493b"
  },
  "data": {
    "Message": "User is not authorized to access this resource with an explicit deny"
  },
  "success": false
}
```

### Анализ результата
✅ **Положительные моменты**:
- API эндпоинт доступен и отвечает
- Сервер корректно обрабатывает запросы
- Возвращается структурированный JSON ответ
- Заголовки ответа содержат полезную информацию для отладки
- Ошибка 403 ожидаема при использовании недействительного API ключа

❌ **Ожидаемые ограничения**:
- Требуется валидный API ключ для доступа к данным
- Необходима регистрация в программе партнеров TripAdvisor

## Выводы и рекомендации

### Техническая реализация
1. **API работает корректно** - сервер отвечает и обрабатывает запросы
2. **Аутентификация обязательна** - все запросы требуют валидный API ключ
3. **Структура ответов стандартная** - используется JSON формат
4. **Обработка ошибок информативная** - сервер возвращает понятные коды ошибок

### Для получения доступа к API необходимо:
1. Перейти на https://www.tripadvisor.com/developers
2. Зарегистрироваться в программе партнеров
3. Создать API ключ через интерфейс разработчика
4. Ознакомиться с условиями использования и ограничениями

### Возможности API
- **Location Details**: Полная информация о локациях (отели, рестораны, достопримечательности)
- **Location Photos**: Высококачественные фотографии локаций
- **Location Reviews**: Свежие отзывы пользователей
- **Location Search**: Поиск локаций по запросу
- **Nearby Location Search**: Поиск локаций по координатам

### Ограничения
- До 50 запросов в секунду
- До 5 отзывов и 5 фотографий на локацию
- Платная модель использования
- Требования к отображению контента согласно политике TripAdvisor

### Практическое применение
API подходит для:
- Интеграции туристического контента в веб-сайты
- Создания мобильных приложений для путешественников
- Разработки систем бронирования
- Аналитических платформ в сфере туризма

