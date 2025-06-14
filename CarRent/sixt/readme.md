# Анализ API Sixt

## Обзор
Sixt Developer Portal предоставляет API для создания мобильных решений на основе глобальной сети мобильности Sixt.

## Основные продукты API

### 1. SHARE API
- **Назначение**: Полный контроль над флотом Sixt Share
- **Функциональность**: Создание полностью цифрового опыта каршеринга для клиентов
- **Описание**: "Our SHARE API allows you to take full control of our Sixt Share fleet and build a fully digital Car-Sharing experience for your customers."

### 2. RENT API  
- **Назначение**: Доступ к премиальному сервису аренды автомобилей
- **Функциональность**: Интеграция с глобальной сетью филиалов и подключенным автопарком
- **Описание**: "Our RENT API unlocks the full potential of our premium car rental service. Integrate our global branch network and tap into our connected car fleet offering your customers a unique and exclusive combination of premium location experience and fully digital processes."
- **Охват**: 105+ стран, 2000+ локаций

## Требования доступа
- Для доступа к документации и API требуется регистрация
- Процесс: заполнение формы запроса доступа с указанием:
  - Имя и фамилия
  - Email
  - Телефон (опционально)
  - Название компании (опционально)  
  - Причина запроса доступа

## URL портала
- Основной сайт: https://developers.sixt.com/
- Форма входа: https://developers.sixt.com/login/
- Форма регистрации: https://developers.sixt.com/register/



## Найденные API Endpoints (из GitHub hackatum2022)

### Базовый URL
`https://api.orange.sixt.com/v1/`

### 1. Поиск станций Sixt
**Endpoint**: `/locations`
**URL**: `https://api.orange.sixt.com/v1/locations?term=<SEARCH>&vehicleType=<TYPE>&type=station`

**Параметры**:
- `<SEARCH>` - свободный текстовый поиск, например "Garching"
- `<TYPE>` - тип транспорта: `car` или `truck`
- `type=station` - тип локации

### 2. Детали станции
**Endpoint**: `/locations/<STATION_ID>`
**URL**: `https://api.orange.sixt.com/v1/locations/<STATION_ID>`

**Параметры**:
- `<STATION_ID>` - ID станции, например `S_5252` (получается из поискового endpoint)

### 3. Предложения аренды
**Endpoint**: `/rentaloffers/offers`
**URL**: `https://api.orange.sixt.com/v1/rentaloffers/offers?pickupStation=<STATION_ID>&returnStation=<STATION_ID>&pickupDate=<DATE>&returnDate=<DATE>&vehicleType=car&currency=EUR&isoCountryCode=DE`

**Параметры**:
- `pickupStation` - ID станции получения
- `returnStation` - ID станции возврата
- `pickupDate` - дата получения в формате `2022-12-14T14:00:00`
- `returnDate` - дата возврата в формате `2022-12-16T14:00:00`
- `vehicleType` - тип транспорта: `car`
- `currency` - валюта: `EUR`
- `isoCountryCode` - код страны: `DE`

**Пример полного URL**:
`https://api.orange.sixt.com/v1/rentaloffers/offers?pickupStation=S_5252&returnStation=S_5252&pickupDate=2022-12-14T14:00:00&returnDate=2022-12-16T14:00:00&vehicleType=car&currency=EUR&isoCountryCode=DE`

### 4. Управление автомобилем (специальный endpoint для хакатона)
**Базовый URL**: `https://api.orange.sixt.com/v2/apps/hackatum2022/twingo/`

**Endpoints**:
- `/unlock` - разблокировать автомобиль
- `/lock` - заблокировать автомобиль  
- `/blink` - мигание фарами


## Результаты тестирования API

### Выполненные тесты

#### 1. ✅ Поиск станций Sixt - УСПЕШНО
**Endpoint**: `GET /v1/locations`
**URL**: `https://api.orange.sixt.com/v1/locations?term=Munich&vehicleType=car&type=station`

**Результат**:
- **Статус**: 200 OK
- **Найдено станций**: 23
- **Формат ответа**: JSON массив объектов

**Структура ответа**:
```json
{
  "id": "S_11",
  "title": "Munich Airport (DE)",
  "subtitle": "Terminalstr. Mitte/MWZ, 85356 München, Germany",
  "type": "station",
  "subtypes": ["car", "eCar", "airport", "pickup"]
}
```

**Примеры найденных станций**:
1. Munich Airport (DE) - ID: S_11
2. Munich Ostbahnhof (DE) - ID: S_46861  
3. Munich Pasing Station (DE) - ID: S_5

#### 2. ✅ Получение деталей станции - УСПЕШНО
**Endpoint**: `GET /v1/locations/{station_id}`
**URL**: `https://api.orange.sixt.com/v1/locations/S_5252`

**Результат**:
- **Статус**: 200 OK
- **Станция**: Munich Garching
- **Адрес**: Schleißheimer Straße 89, 85748 Garching b. München, Germany

**Структура ответа**:
```json
{
  "id": "S_5252",
  "title": "Munich Garching",
  "subtitle": "Schleißheimer Straße 89, 85748 Garching b. München, Germany",
  "coordinates": {
    "latitude": 48.24924087524414,
    "longitude": 11.626460075378418
  },
  "type": "station",
  "subtypes": ["car", "eCar", "downtown", "requiresAddressAndPayment", "delivery", "collection", "pickup"]
}
```

#### 3. ❌ Поиск предложений аренды - НЕУСПЕШНО
**Endpoint**: `GET /v1/rentaloffers/offers`
**URL**: `https://api.orange.sixt.com/v1/rentaloffers/offers?pickupStation=S_5252&returnStation=S_5252&pickupDate=2025-06-15T14:00:00&returnDate=2025-06-17T14:00:00&vehicleType=car&currency=EUR&isoCountryCode=DE`

**Результат**:
- **Статус**: 404 Not Found
- **Ошибка**: `{"error":"service does not exist"}`

**Возможные причины**:
- Endpoint может быть недоступен в публичной версии API
- Требуется авторизация или специальные права доступа
- Изменился URL или версия API

#### 4. ❌ Управление автомобилем - НЕУСПЕШНО
**Endpoint**: `POST /v2/apps/hackatum2022/twingo/blink`
**URL**: `https://api.orange.sixt.com/v2/apps/hackatum2022/twingo/blink`

**Результат**:
- **Статус**: 404 Not Found
- **Ошибка**: `{"errorCode":"not_found","message":"The resource /v2/apps/hackatum2022/twingo/blink could not be found","retriable":false}`

**Возможные причины**:
- Endpoint был создан специально для хакатона 2022 года и больше не доступен
- Требуется специальная авторизация для доступа к функциям управления автомобилем

### Анализ заголовков ответа

Успешные запросы содержат следующие важные заголовки:
- `Content-Type: application/json; charset=utf-8`
- `x-correlation-id: 3c07276b-b1ad-43b9-b3dc-009ed214615b` - ID для трассировки запроса
- `x-sx-session-key: 5fc59473-e722-4193-ad14-2353881dedaa` - ключ сессии
- `Server: cloudflare` - API использует Cloudflare для CDN/защиты

### Выводы

1. **Публично доступные endpoints**:
   - ✅ Поиск станций (`/v1/locations`) - работает без авторизации
   - ✅ Детали станции (`/v1/locations/{id}`) - работает без авторизации

2. **Ограниченные endpoints**:
   - ❌ Предложения аренды (`/v1/rentaloffers/offers`) - требует авторизации или недоступен
   - ❌ Управление автомобилем (`/v2/apps/hackatum2022/twingo/*`) - специальный endpoint, больше не доступен

3. **Качество API**:
   - Хорошо структурированные JSON ответы
   - Подробная информация о станциях включая координаты
   - Правильные HTTP статус коды
   - Система трассировки запросов

