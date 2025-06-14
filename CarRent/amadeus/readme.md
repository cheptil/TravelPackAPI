# Анализ API Amadeus Transfer Search

## Основная информация

**URL:** https://developers.amadeus.com/self-service/category/cars-and-transfers/api-doc/transfer-search
**Базовый URL:** test.api.amadeus.com/v1
**Эндпоинт:** POST /shopping/transfer-offers
**Описание:** API для поиска различных типов транспортных услуг

## Типы транспортных услуг

1. **Private Transfers** - Частные трансферы с водителем
2. **Hourly Services** - Почасовая аренда с водителем
3. **Taxis** - Предварительное бронирование такси
4. **Shared Transfers** - Общие трансферы с фиксированной ценой за пассажира
5. **Airport Express** - Экспресс-поезда между аэропортами и ж/д станциями
6. **Airport Buses** - Автобусы между аэропортами и автовокзалами

## Структура запроса

**Метод:** POST
**Content-Type:** application/vnd.amadeus+json или application/json

### Пример JSON запроса:
```json
{
  "startLocationCode": "CDG",
  "endAddressLine": "Avenue Anatole France, 5",
  "endCityName": "Paris",
  "endZipCode": "75007",
  "endCountryCode": "FR",
  "endName": "Souvenirs de la Tour",
  "endGeoCode": "48.859466,2.2976965",
  "transferType": "PRIVATE",
  "startDateTime": "2024-04-10T10:30:00",
  "passengers": 2,
  "stopOvers": [
    {
      "duration": "PT2H30M",
      "sequenceNumber": 1,
      "addressLine": "Avenue de la Bourdonnais, 19",
      "countryCode": "FR",
      "cityName": "Paris",
      "zipCode": "75007",
      "name": "De La Tours",
      "geoCode": "48.859477,2.2976965",
      "stateCode": "FR"
    }
  ]
}
```

## Основные параметры

- **startLocationCode** - Код начальной локации (например, CDG для аэропорта Шарль де Голль)
- **endAddressLine** - Адрес назначения
- **endCityName** - Город назначения
- **endZipCode** - Почтовый индекс
- **endCountryCode** - Код страны
- **transferType** - Тип трансфера (PRIVATE, SHARED, TAXI и др.)
- **startDateTime** - Дата и время начала в формате ISO 8601
- **passengers** - Количество пассажиров
- **stopOvers** - Промежуточные остановки (опционально)

## Авторизация

Требуется API ключ. Рекомендуется изучить Authorization Guide для получения access token.

## Тестовая среда

- Используется подмножество продакшн данных
- Рекомендуется тестировать с крупными городами как LON (Лондон) или NYC (Нью-Йорк)



## Процесс авторизации

Для получения access token необходимо:

1. **Зарегистрироваться** на https://developers.amadeus.com и создать приложение
2. **Получить API Key и API Secret** из панели управления
3. **Запросить access token** через OAuth 2.0 Client Credentials Grant

### Эндпоинт для получения токена:
```
POST https://test.api.amadeus.com/v1/security/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={API_KEY}&client_secret={API_SECRET}
```

### Пример ответа с токеном:
```json
{
    "type": "amadeusOAuth2Token",
    "username": "foo@bar.com",
    "application_name": "BetaTest_foobar",
    "client_id": "3sY9VNvXIjyJYd5mmOtOzJLuL1BzJBBp",
    "token_type": "Bearer",
    "access_token": "CpjU0sEenniHCgPDrndzOSWFk5mN",
    "expires_in": 1799,
    "state": "approved",
    "scope": ""
}
```

### Использование токена:
```
Authorization: Bearer {access_token}
```

Токен действителен в течение 1799 секунд (около 30 минут).



## Результаты тестирования

### Тестовый запрос без авторизации

**Статус:** 401 Unauthorized  
**Ошибка:** Missing or invalid format for mandatory Authorization header

```json
{
  "errors": [
    {
      "code": 38191,
      "title": "Invalid HTTP header",
      "detail": "Missing or invalid format for mandatory Authorization header",
      "status": 401
    }
  ]
}
```

### Анализ ответа

1. **Корректная обработка ошибок**: API возвращает структурированную ошибку в JSON формате
2. **Информативные сообщения**: Четко указано, что отсутствует заголовок Authorization
3. **Стандартные HTTP коды**: Используется стандартный код 401 для ошибок авторизации
4. **Дополнительная информация**: В заголовке WWW-Authenticate содержится детальная информация об ошибке

### Структура успешного ответа (из документации)

При успешном запросе API возвращает массив предложений трансфера:

```json
{
  "data": [
    {
      "type": "transfer-offer",
      "id": "4cb11574-4a02-11e8-842f-0ed5f89f718b",
      "transferType": "PRIVATE",
      "start": {
        "dateTime": "2021-11-10T10:30:00",
        "locationCode": "CDG"
      },
      "end": {
        "address": {
          "line": "Avenue Anatole France, 5",
          "zip": "75007",
          "countryCode": "FR",
          "cityName": "Paris",
          "latitude": 48.859466,
          "longitude": 2.2976965
        },
        "googlePlaceId": "ChIJL-DOWeBv5kcRfTbh97PimWc",
        "name": "Souvenirs De La Tour"
      }
    }
  ]
}
```

## Выводы и рекомендации

### Положительные аспекты API

1. **Хорошая документация**: Подробное описание параметров и примеры запросов
2. **Стандартизированный подход**: Использование OAuth 2.0 для авторизации
3. **Гибкость**: Поддержка различных типов трансферов
4. **Структурированные данные**: Четкая JSON схема для запросов и ответов

### Требования для использования

1. **Регистрация**: Необходимо создать аккаунт на developers.amadeus.com
2. **API ключи**: Получение API Key и API Secret через панель управления
3. **Авторизация**: Обязательное получение access token перед каждым запросом
4. **Ограничения**: Тестовая среда имеет ограниченный набор данных

### Рекомендации по интеграции

1. **Кэширование токенов**: Токены действительны 30 минут, следует кэшировать их
2. **Обработка ошибок**: Реализовать автоматическое обновление токена при истечении
3. **Валидация данных**: Проверять корректность координат и кодов локаций
4. **Тестирование**: Использовать крупные города (LON, NYC) для тестирования

### Пример интеграции

Создан полный Python скрипт `amadeus_transfer_api_complete.py`, который включает:

- Функцию получения access token
- Выполнение запроса к Transfer Search API
- Анализ и парсинг ответа
- Обработку ошибок

### Следующие шаги

1. Зарегистрироваться на платформе Amadeus for Developers
2. Создать тестовое приложение
3. Получить API ключи
4. Протестировать скрипт с реальными учетными данными
5. Интегрировать в основное приложение

## Заключение

API Amadeus Transfer Search представляет собой мощный инструмент для поиска транспортных услуг. Несмотря на необходимость регистрации и получения ключей, API предоставляет хорошо структурированный интерфейс с подробной документацией. Тестирование показало корректную обработку ошибок авторизации и соответствие заявленным спецификациям.

