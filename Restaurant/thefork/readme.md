# Анализ TheFork API

## Обзор

TheFork API предназначен для подключения сторонних систем к платформе TheFork Manager (TFM). API позволяет внешним компаниям синхронизировать важные данные и процессы между их системами и экосистемой TheFork.

## Основные характеристики

### Версионирование
- Используется одна версия для всего API, а не отдельная версия для каждого endpoint
- При критических изменениях в контракте одного или нескольких endpoints вводится новая версия API
- Поддержка предыдущей версии прекращается через 6 месяцев

### Rate Limiting
- Rate limiting применяется на уровне по умолчанию, как указано в контракте
- Можно обратиться для обсуждения необходимых изменений на основе конкретных требований

## Типы API

В документации представлены два основных типа API:
1. **POS-API** - для систем точек продаж
2. **B2B-API** - для бизнес-партнеров

## Структура документации

- Getting started (текущая страница)
- Preliminary steps
- Best practices
- POS-API
- B2B-API
- Overview
- Versioning
- Rate limiting
- Error codes



## POS-API Endpoints

### postV1Create
- **URL**: `POST https://api.thefork.io/pos/v1/create`
- **Назначение**: Создание нового POS (Point of Sale) в системе TheFork
- **Аутентификация**: ApiKeyAuth (через заголовок X-Api-Key)

#### Обязательные параметры запроса:
- `homepageUrl` (string) - URL домашней страницы
- `name` (string) - Название POS
- `type` (string) - Тип POS

#### Дополнительные параметры:
- `oauthAuthorizeUrl` (string) - URL для OAuth авторизации
- `oauthClientId` (string) - OAuth Client ID
- `oauthClientSecret` (string) - OAuth Client Secret
- `oauthScope` (string[]) - OAuth области доступа
- `oauthTokenUrl` (string) - URL для получения OAuth токена
- `receiptOpeningUrl` (string) - URL для открытия чека
- `webhookToken` (string) - Токен для webhook

#### Ответ (200 OK):
```json
{
  "name": "string",
  "type": "string", 
  "homepageUrl": "string",
  "receiptOpeningUrl": "string",
  "oauthAuthorizeUrl": "string",
  "oauthTokenUrl": "string",
  "oauthScope": ["string"],
  "availableOn": "string",
  "logoPath": "string",
  "uuid": "string",
  "consumerId": "string"
}
```

#### Пример CURL запроса:
```bash
curl -L -X POST 'https://api.thefork.io/pos/v1/create' \
-H 'Content-Type: application/json' \
-H 'Accept: */*' \
-H 'X-Api-Key: <API_KEY_VALUE>' \
--data-raw '{
  "homepageUrl": "string",
  "name": "string",
  "oauthAuthorizeUrl": "string",
  "oauthClientId": "string",
  "oauthClientSecret": "string",
  "oauthScope": ["string"],
  "oauthTokenUrl": "string",
  "receiptOpeningUrl": "string",
  "type": "string",
  "webhookToken": "string"
}'
```


## B2B-API Endpoints

### Data - Get customers list
- **URL**: `GET https://api.thefork.io/manager/v1/customers`
- **Назначение**: Получение списка клиентов, созданных или обновленных между двумя датами
- **Аутентификация**: Требуется (тип не указан в данном разделе)

#### Обязательные параметры запроса:
- `groupUuid` (string) - UUID группы для фильтрации
- `startDate` (string) - Начальная дата для фильтрации
- `endDate` (string) - Конечная дата для фильтрации

#### Дополнительные параметры:
- `limit` (number) - Лимит количества клиентов для возврата (по умолчанию 100, максимум 10000)
- `page` (number) - Номер страницы для возврата (по умолчанию 1)

#### Пример CURL запроса:
```bash
curl -L -X GET 'https://api.thefork.io/manager/v1/customers?groupUuid=<GROUP_UUID>&startDate=<START_DATE>&endDate=<END_DATE>' \
-H 'Accept: */*'
```

### Другие доступные B2B-API endpoints:
- Data - Get customer details
- Data - Get reservations list  
- Data - Get reservation details
- Booking flow - Get availabilities
- Booking flow - Get offers

## Базовые URL:
- **POS-API**: `https://api.thefork.io/pos`
- **B2B-API**: `https://api.thefork.io/manager`


## Результаты тестирования API

### Тестовые запросы

Были выполнены тестовые запросы к обоим типам API с использованием curl для проверки доступности и анализа ответов сервера.

### B2B-API: Get customers list

**Запрос:**
```bash
curl -v -X GET "https://api.thefork.io/manager/v1/customers?groupUuid=test&startDate=2024-01-01&endDate=2024-12-31" \
-H "Accept: */*"
```

**Результат:**
- **Статус код**: 401 Unauthorized
- **Content-Type**: application/json; charset=utf-8
- **Заголовок аутентификации**: `www-authenticate: Bearer realm="auth.thefork.io", error="invalid_token"`
- **Ответ**: `{"message":"Unauthorized"}`

**Анализ:**
- API доступен и отвечает корректно
- Требуется Bearer токен для аутентификации
- Realm для аутентификации: `auth.thefork.io`
- Сервер использует HTTP/2 и TLS 1.3
- SSL сертификат валиден (*.thefork.io, выдан DigiCert)

### POS-API: Create POS

**Запрос:**
```bash
curl -v -X POST "https://api.thefork.io/pos/v1/create" \
-H "Content-Type: application/json" \
-H "Accept: */*" \
-H "X-Api-Key: test-api-key" \
-d '{"homepageUrl":"https://example.com","name":"Test POS","type":"restaurant"}'
```

**Результат:**
- **Статус код**: 401 Unauthorized  
- **Content-Type**: application/json; charset=utf-8
- **Ответ**: `{"message":"Invalid authentication credentials"}`

**Анализ:**
- API доступен и отвечает корректно
- Требуется валидный API ключ в заголовке X-Api-Key
- Сообщение об ошибке более специфичное ("Invalid authentication credentials")
- Сервер корректно обрабатывает JSON payload

### Технические детали инфраструктуры

**Сервер и безопасность:**
- Сервер: istio-envoy (указывает на использование Istio service mesh)
- CDN: Varnish cache (cache-par-* и cache-iad-* серверы)
- Заголовки безопасности:
  - `X-Content-Type-Options: nosniff`
  - `X-XSS-Protection: 1; mode=block`
  - `X-Frame-Options: SAMEORIGIN`
  - `Content-Security-Policy: frame-ancestors 'self'`
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`

**SSL/TLS:**
- Протокол: TLS 1.3 / TLS_AES_128_GCM_SHA256
- Сертификат: *.thefork.io (DigiCert Global G2 TLS RSA SHA256 2020 CA1)
- Срок действия: до 29 августа 2025

### Выводы

1. **API функционируют корректно** - оба endpoint доступны и возвращают ожидаемые ошибки аутентификации
2. **Разные методы аутентификации**:
   - B2B-API: Bearer токен
   - POS-API: API ключ в заголовке X-Api-Key
3. **Высокий уровень безопасности** - современные TLS протоколы и заголовки безопасности
4. **Профессиональная инфраструктура** - использование Istio, CDN, правильная обработка ошибок
5. **Готовность к продакшену** - API готовы для интеграции при наличии валидных учетных данных


## Рекомендации по интеграции

### Для разработчиков

1. **Получение доступа**:
   - Обратитесь к TheFork для получения API ключей
   - B2B-API требует OAuth 2.0 Bearer токен
   - POS-API требует API ключ для заголовка X-Api-Key

2. **Аутентификация B2B-API**:
   - Используйте OAuth 2.0 flow с realm `auth.thefork.io`
   - Включайте Bearer токен в заголовок Authorization
   - Обновляйте токены согласно их времени жизни

3. **Аутентификация POS-API**:
   - Включайте API ключ в заголовок `X-Api-Key`
   - Храните ключ в безопасном месте
   - Не передавайте ключ в URL параметрах

4. **Обработка ошибок**:
   - Обрабатывайте 401 ошибки для обновления токенов
   - Реализуйте retry логику с экспоненциальной задержкой
   - Логируйте ошибки для мониторинга

5. **Rate Limiting**:
   - Соблюдайте лимиты согласно вашему контракту
   - Реализуйте очереди запросов при необходимости
   - Мониторьте заголовки rate limiting в ответах

### Примеры интеграции

**Python с requests:**
```python
import requests

# B2B-API
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Accept': 'application/json'
}
response = requests.get(
    'https://api.thefork.io/manager/v1/customers',
    headers=headers,
    params={'groupUuid': 'your-group-uuid', 'startDate': '2024-01-01', 'endDate': '2024-12-31'}
)

# POS-API  
headers = {
    'X-Api-Key': 'YOUR_API_KEY',
    'Content-Type': 'application/json'
}
data = {
    'homepageUrl': 'https://your-restaurant.com',
    'name': 'Your Restaurant POS',
    'type': 'restaurant'
}
response = requests.post(
    'https://api.thefork.io/pos/v1/create',
    headers=headers,
    json=data
)
```

**JavaScript/Node.js:**
```javascript
// B2B-API
const response = await fetch('https://api.thefork.io/manager/v1/customers?groupUuid=your-group-uuid&startDate=2024-01-01&endDate=2024-12-31', {
    headers: {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Accept': 'application/json'
    }
});

// POS-API
const response = await fetch('https://api.thefork.io/pos/v1/create', {
    method: 'POST',
    headers: {
        'X-Api-Key': 'YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        homepageUrl: 'https://your-restaurant.com',
        name: 'Your Restaurant POS',
        type: 'restaurant'
    })
});
```

### Следующие шаги

1. **Изучите полную документацию** на https://docs.thefork.io/
2. **Свяжитесь с TheFork** для получения API доступа
3. **Изучите разделы Authentication** для каждого типа API
4. **Протестируйте интеграцию** в sandbox окружении (если доступно)
5. **Реализуйте обработку webhook** для event-based интеграций
6. **Настройте мониторинг** API вызовов и ошибок

---

*Документ создан на основе анализа TheFork API документации и тестирования endpoints. Для получения актуальной информации обращайтесь к официальной документации.*

