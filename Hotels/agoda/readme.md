# Анализ API Agoda Partners

## Обзор
Agoda предоставляет API для партнеров с прямыми контрактами с отелями по всему миру, включая инвентарь Priceline. API предоставляет конкурентные тарифы и качественный контент для большого количества объектов размещения.

## Основные разделы API:
1. **Getting Started** - начало работы
2. **Environment Setup** - настройка окружения  
3. **Content API** - API контента
4. **Search API** - API поиска
5. **JSON Search API** - JSON API поиска
6. **NHA API** - API NHA
7. **CDS API** - API CDS
8. **Best Practices** - лучшие практики

## Процесс интеграции:
1. Изучение модели партнерства
2. Изучение API и начало интеграции
3. Получение учетных данных партнера
4. Запрос сертификации
5. Переключение на Live окружение

## Модели партнерства:
- Online affiliates / MSE model - для сайтов-агрегаторов и сравнения цен



## Short Search API

### Описание
Short Search API оптимизирован для партнеров, которым требуется минимальная информация о номерах. Для бронирования партнер должен использовать URL Agoda из ответа. Подходит только для модели Online affiliates / MSE partnership.

### Типы поиска:
1. **Single hotel search (Type=4)** - поиск по конкретному отелю
2. **Hotel list search (Type=6)** - поиск по списку отелей (до 30 ID за запрос)

### Основные параметры запроса:
- **siteid** - идентификатор сайта (integer)
- **apikey** - API ключ для аутентификации
- **Type** - тип поиска (4 или 6)
- **Id** - ID отеля или список ID через запятую
- **CheckIn** - дата заезда (YYYY-MM-DD)
- **CheckOut** - дата выезда (YYYY-MM-DD)
- **Rooms** - количество номеров
- **Adults** - количество взрослых
- **Children** - количество детей
- **Language** - язык ответа
- **Currency** - валюта
- **UserCountry** - страна пользователя (ISO код)

### Пример XML запроса:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<AvailabilityRequestV2 xmlns="http://xml.agoda.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" siteid="123456" apikey="00000000-0000-0000-0000-000000000000">
    <Type>6</Type>
    <Id>12133, 69001</Id>
    <CheckIn>2019-12-25</CheckIn>
    <CheckOut>2019-12-27</CheckOut>
    <Rooms>1</Rooms>
    <Adults>2</Adults>
    <Children>2</Children>
    <ChildrenAges>
        <Age>4</Age>
        <Age>8</Age>
    </ChildrenAges>
    <Language>th-th</Language>
    <Currency>USD</Currency>
    <UserCountry>TH</UserCountry>
</AvailabilityRequestV2>
```


## JSON Search API

### Описание
JSON Search API был выпущен для избранных партнеров в конце 2021 года и ожидается полный релиз с Q1 2022. Новый формат обеспечивает более быстрые ответы API с менее подробным вводом, а также большую гибкость в настройке запросов и ответов.

### Аутентификация
- **Authorization Header**: `Authorization: siteid:apikey`
- **Content-Type**: `application/json`

### Пример JSON запроса:
```json
{
  "criteria": {
    "propertyIds": [12157],
    "checkIn": "2022-12-23",
    "checkOut": "2022-12-24",
    "rooms": 1,
    "adults": 2,
    "children": 2,
    "childrenAges": [5, 6],
    "language": "en-us",
    "currency": "USD",
    "userCountry": "US"
  },
  "features": {
    "ratesPerProperty": 25,
    "extra": [
      "content",
      "surchargeDetail",
      "cancellationDetail",
      "benefitDetail",
      "dailyRate",
      "taxDetail",
      "rateDetail",
      "promotionDetail"
    ]
  }
}
```

### Основные параметры:
- **propertyIds** - массив ID отелей (максимум 100 за запрос)
- **checkIn/checkOut** - даты в формате YYYY-MM-DD
- **rooms** - количество номеров
- **adults** - количество взрослых
- **children** - количество детей
- **childrenAges** - возраст детей (0-17)
- **ratesPerProperty** - количество тарифов на отель
- **extra** - дополнительные данные в ответе

### Настройка окружения:
- **TTL для DNS**: рекомендуется <=5 минут
- **TLS Protocol**: требуется TLS v1.2
- **Accept-Encoding**: рекомендуется `gzip,deflate`
- **Sandbox Environment**: доступна тестовая среда
- **SSL Certificate**: принимаются глобально признанные сертификаты


## Анализ структуры API и требований

### Основные выводы из документации:
1. **Два основных формата API**: XML (Search API) и JSON (JSON Search API)
2. **Аутентификация**: через Authorization header с siteid:apikey
3. **Два окружения**: Sandbox (тестовое) и Production (боевое)
4. **Методы запросов**: POST для отправки данных поиска

### Предполагаемые URL эндпоинты:
Основываясь на стандартных паттернах API и найденной информации:

**Sandbox окружение:**
- XML Search API: `https://sandbox-distribution.agoda.com/dsws/hotelapi.asmx`
- JSON Search API: `https://sandbox-distribution.agoda.com/api/search` (предположительно)

**Production окружение:**
- XML Search API: `https://distribution.agoda.com/dsws/hotelapi.asmx`
- JSON Search API: `https://distribution.agoda.com/api/search` (предположительно)

### Требования для тестового запроса:
1. **Обязательные параметры**:
   - siteid (тестовый ID)
   - apikey (тестовый ключ)
   - propertyIds или Id (ID отелей)
   - checkIn/checkOut (даты)
   - rooms, adults (количество номеров и гостей)

2. **HTTP заголовки**:
   - Authorization: siteid:apikey
   - Content-Type: application/json (для JSON API) или text/xml (для XML API)
   - Accept-Encoding: gzip,deflate

### Ограничения:
- Для реальных запросов требуется регистрация в качестве партнера Agoda
- Тестовые учетные данные предоставляются только зарегистрированным партнерам
- Sandbox окружение доступно только с валидными учетными данными


## Результаты тестового запроса

### Выполненный тест
Был создан и выполнен тестовый запрос к предполагаемому эндпоинту Agoda JSON Search API:

**URL**: `https://sandbox-distribution.agoda.com/api/search`
**Метод**: POST
**Content-Type**: application/json

### Структура тестового запроса:
```json
{
  "criteria": {
    "propertyIds": [12157, 69001],
    "checkIn": "2025-06-19",
    "checkOut": "2025-06-20",
    "rooms": 1,
    "adults": 2,
    "children": 0,
    "language": "en-us",
    "currency": "USD",
    "userCountry": "US"
  },
  "features": {
    "ratesPerProperty": 25,
    "extra": [
      "content", "surchargeDetail", "cancellationDetail",
      "benefitDetail", "dailyRate", "taxDetail", 
      "rateDetail", "promotionDetail"
    ]
  }
}
```

### Результат тестирования:
- **HTTP Status**: 200 OK
- **Тип ответа**: HTML вместо ожидаемого JSON
- **Содержимое**: Главная страница Agoda.com

### Анализ результатов:

#### Обнаруженные факты:
1. Предполагаемый URL эндпоинт не существует
2. Сервер перенаправил запрос на главную страницу сайта
3. Реальные URL эндпоинты не публикуются в открытой документации
4. API использует закрытую архитектуру с ограниченным доступом

#### Выводы:
1. **Безопасность**: Agoda защищает свои API эндпоинты от несанкционированного доступа
2. **Партнерская модель**: Доступ предоставляется только официальным партнерам
3. **Документация**: Публичная документация содержит структуру запросов, но не URL
4. **Тестирование**: Невозможно без официальной регистрации и учетных данных

### Примерный ожидаемый ответ API:
На основе документации, успешный ответ должен выглядеть следующим образом:

```json
{
  "searchId": "162918320771983000",
  "properties": [
    {
      "propertyId": 12157,
      "propertyName": "Medhufushi Island Resort",
      "translatedPropertyName": "Medhufushi Island Resort",
      "rooms": [
        {
          "roomId": "3160573",
          "roomName": "1 Bedroom Seaview Villa - Room Only",
          "standardTranslation": "1 Bedroom Seaview Villa - Room Only",
          "rates": [
            {
              "rateId": "1125.00",
              "currency": "USD",
              "totalPrice": 1125.00,
              "averageNightlyRate": 562.50,
              "taxesAndFees": 45.00,
              "cancellationPolicy": "Free cancellation until 24 hours before check-in",
              "bookingUrl": "https://www.agoda.com/partners/partnersearch.aspx?...",
              "benefits": ["Free WiFi", "Free breakfast"],
              "promotions": ["Early Bird Discount"]
            }
          ]
        }
      ]
    }
  ],
  "metadata": {
    "totalProperties": 1,
    "searchCriteria": {
      "checkIn": "2025-06-19",
      "checkOut": "2025-06-20",
      "rooms": 1,
      "adults": 2,
      "children": 0
    }
  }
}
```

## Заключение и рекомендации

### Ключевые выводы:
1. **Документация Agoda API** хорошо структурирована и содержит подробные примеры запросов и ответов
2. **Два основных формата**: XML (классический) и JSON (современный) Search API
3. **Закрытая архитектура**: реальные URL эндпоинты доступны только партнерам
4. **Строгая аутентификация**: требуются официальные siteid и apikey

### Для реального использования API необходимо:

#### 1. Регистрация партнера
- Подача заявки через Agoda Developer Portal
- Выбор подходящей модели партнерства (Online affiliates/MSE, etc.)
- Подписание договора и документов AVRF

#### 2. Получение учетных данных
- Site ID (уникальный идентификатор сайта)
- API Key (ключ для аутентификации)
- Официальные URL эндпоинтов для sandbox и production

#### 3. Этапы интеграции
- Разработка и тестирование в sandbox окружении
- Сертификация от команды Agoda
- Переход на production окружение
- Запуск и мониторинг

#### 4. Технические требования
- Поддержка TLS v1.2
- TTL для DNS ≤ 5 минут
- Обработка сжатия gzip/deflate
- Правильная обработка ошибок и таймаутов

### Преимущества Agoda API:
- Доступ к обширной базе отелей включая Priceline
- Конкурентные тарифы и актуальная информация
- Гибкая настройка запросов и ответов
- Поддержка различных валют и языков
- Модульная архитектура для выборочной интеграции

### Ограничения:
- Требуется официальное партнерство
- Закрытые URL эндпоинты
- Процесс сертификации обязателен
- Ограничения по трафику в зависимости от договора

Agoda API представляет собой мощный инструмент для интеграции гостиничных услуг, но требует официального партнерства и соблюдения всех процедур регистрации и сертификации.

