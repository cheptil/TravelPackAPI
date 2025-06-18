# Amadeus City Search API - Анализ документации

## Основная информация

**URL API:** https://test.api.amadeus.com/v1
**Endpoint:** /reference-data/locations/cities
**Метод:** GET
**Версия:** 1.0

## Описание API

City Search API находит города, которые соответствуют определенному слову или строке букв. API предоставляет автодополнение для городов на основе того, что путешественник вводит в поле поиска. API возвращает список городов с названием, часовым поясом, координатами и, когда возможно, ближайшим аэропортом.

## Ключевые особенности

1. **Отличие от Airport & City Search API**: Этот API находит любой город, который соответствует поисковому ключевому слову, независимо от того, есть ли в нем аэропорт или нет.

2. **Опциональное включение аэропортов**: Можно дополнительно включить соответствующие аэропорты, добавив `include=AIRPORTS` к поисковому запросу.

3. **Пример использования**: "Какие названия городов начинаются с 'Dub'?"

## Требования для использования

- Необходимо получить API ключ через регистрацию
- Нужен access token для авторизации
- Доступна тестовая среда для разработки
- Бесплатное использование с ограничениями по квоте

## Серверы

- **Тестовый сервер**: https://test.api.amadeus.com/v1
- **Продакшн сервер**: https://api.amadeus.com/v1 (после перехода в продакшн)



## Параметры запроса

### Query Parameters

1. **countryCode** (string, optional)
   - Описание: ISO 3166 Alpha-2 код страны, например "US" для США
   - Пример: FR

2. **keyword** (string, required) ⭐
   - Описание: Ключевое слово, которое должно представлять начало слова в названии города
   - Пример: PARIS
   - Обязательный параметр

3. **max** (integer, optional)
   - Описание: Количество результатов, которые пользователь хочет видеть в ответе
   - Пример: 10
   - По умолчанию: не указано

4. **include** (array[string], optional)
   - Описание: Ресурсы для включения в ответ
   - Доступные значения: AIRPORTS
   - Пример: AIRPORTS

## Endpoint

**GET** `/reference-data/locations/cities`

Полный URL для тестовой среды:
`https://test.api.amadeus.com/v1/reference-data/locations/cities`


## Структура ответа

### Успешный ответ (200 OK)

Пример ответа в формате JSON:

```json
{
  "data": [
    {
      "type": "location",
      "subType": "city",
      "name": "PARIS",
      "iataCode": "PAR",
      "address": {
        "countryCode": "FR"
      },
      "geoCode": {
        "latitude": "49.01278",
        "longitude": "2.55"
      },
      "relationships": [
        {
          "id": "CDG",
          "type": "Airport",
          "href": "#/included/airports/CDG"
        },
        {
          "id": "ORY",
          "type": "Airport",
          "href": "#/included/airports/ORY"
        }
      ]
    }
  ]
}
```

### Коды ошибок

**400 Bad Request:**
- 32171: MANDATORY DATA MISSING
- 572: INVALID OPTION
- 2781: INVALID LENGTH
- 477: INVALID FORMAT
- 4926: INVALID DATA RECEIVED

**500 Internal Server Error:**
- 141: SYSTEM ERROR HAS OCCURRED

### Поля ответа

- **type**: Тип объекта (location)
- **subType**: Подтип (city)
- **name**: Название города
- **iataCode**: IATA код города (если доступен)
- **address.countryCode**: Код страны
- **geoCode.latitude**: Широта
- **geoCode.longitude**: Долгота
- **relationships**: Связанные аэропорты (если включены)


## Процесс авторизации

Amadeus API использует OAuth 2.0 с Client Credentials Grant для авторизации.

### Шаги для получения access token:

1. **Получение API ключей**: Необходимо зарегистрироваться и получить API Key и API Secret
2. **Запрос токена**: Отправить POST запрос на `https://test.api.amadeus.com/v1/security/oauth2/token`

### Параметры запроса токена:

- **URL**: `https://test.api.amadeus.com/v1/security/oauth2/token`
- **Метод**: POST
- **Content-Type**: `application/x-www-form-urlencoded`
- **Тело запроса**:
  - `grant_type=client_credentials`
  - `client_id={ваш_api_key}`
  - `client_secret={ваш_api_secret}`

### Пример cURL запроса:

```bash
curl "https://test.api.amadeus.com/v1/security/oauth2/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
```

### Ответ с токеном:

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

Добавить заголовок авторизации к каждому API запросу:
```
Authorization: Bearer {access_token}
```

### Примечания:

- Токен действителен 1799 секунд (около 30 минут)
- Необходимо обновлять токен при истечении срока действия
- API Key и API Secret должны храниться в безопасности

