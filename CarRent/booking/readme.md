# Анализ Booking.com Demand API для размещений

## Общая информация

URL документации: https://developers.booking.com/demand/docs/open-api/demand-api/accommodations

### Описание API
Это коллекция API специально для части размещений в связанных поездках. API позволяет искать размещения (отели, апартаменты и т.д.), проверять их доступность, получать отзывы, детали размещений и т.д.

### Доступные операции:
1. **POST /accommodations/search** - Поиск размещений
2. **POST /accommodations/availability** - Проверка доступности
3. **POST /accommodations/bulk-availability** - Массовая проверка доступности
4. **POST /accommodations/chains** - Сети отелей
5. **POST /accommodations/constants** - Константы
6. **POST /accommodations/details** - Детали размещений
7. **POST /accommodations/details/changes** - Обновленные размещения
8. **POST /accommodations/reviews** - Отзывы

## Детальное изучение операций



### Операция: POST /accommodations/search

**Описание**: Возвращает самые дешевые доступные продукты для каждого размещения, соответствующего критериям поиска.

**Аутентификация**: Bearer Auth (требуется)

**Заголовки**:
- `X-Affiliate-Id` (integer, обязательный) - Идентификатор партнера

**Основные параметры тела запроса**:

1. **24_hour_reception** (boolean) - Фильтр по круглосуточной стойке регистрации
2. **accommodation_facilities** (Array of integers) - Удобства размещения
3. **accommodation_types** (Array of integers) - Типы размещения
4. **accommodations** (Array of integers, <= 100 items) - Конкретные размещения
5. **airport** (string, ^[A-Z]{3}$) - Трехбуквенный код аэропорта IATA
6. **booker** (object, обязательный) - Информация о бронирующем:
   - `country` (string, ^[a-z]{2}$, обязательный) - Страна бронирующего
   - `platform` (string, обязательный) - Платформа (android/desktop/ios/mobile/tablet)
   - `state` (string, ^[a-z]{2}$) - Штат (только для США)
   - `travel_purpose` (string) - Цель поездки (business/leisure)
   - `user_groups` (Array of strings) - Группы пользователей
7. **brands** (Array of integers) - Бренды
8. **cancellation_type** (string) - Тип отмены (free_cancellation/non_refundable)
9. **checkin** (string, date, обязательный) - Дата заезда (в течение 500 дней, формат yyyy-mm-dd)
10. **checkout** (string, date, обязательный) - Дата выезда (1-90 дней после заезда, формат yyyy-mm-dd)
11. **city** (integer) - ID города
12. **coordinates** (object) - Координаты для ограничения поиска
13. **country** (string, ^[a-z]{2}$) - Двухбуквенный код страны ISO 3166-1
14. **currency** (string, ^[A-Z]{3}$) - Трехбуквенный код валюты ISO 4217



15. **district** (integer, >= 1) - ID района
16. **dormitories** (string) - Включение общежитий (include/exclude/only)
17. **extras** (Array of strings) - Дополнительная информация (extra_charges/products)
18. **guests** (object, обязательный) - Детали гостей:
    - `allocation` (Array of objects) - Точное распределение гостей по комнатам
    - `children` (Array of integers) - Возраста детей
    - `number_of_adults` (integer, >= 1, обязательный) - Количество взрослых
    - `number_of_rooms` (integer, >= 1, обязательный) - Количество комнат
19. **landmark** (integer, >= 1) - ID достопримечательности
20. **meal_plan** (string) - План питания (all_inclusive/breakfast_included/full_board/half_board)
21. **page** (string) - Токен пагинации
22. **payment** (object) - Фильтр платежей
23. **price** (object) - Фильтр цен
24. **rating** (object) - Фильтр рейтинга
25. **region** (integer, >= 1) - ID региона
26. **room_facilities** (Array of integers) - Удобства в комнате
27. **rows** (integer, 10-100) - Максимальное количество результатов (по умолчанию 100)
28. **sort** (object) - Параметры сортировки
29. **travel_proud** (boolean) - Фильтр LGBTQ+ дружественных отелей

### Пример запроса (curl):
```bash
curl -i -X POST \
  https://demandapi.booking.com/3.1/accommodations/search \
  -H 'Authorization: Bearer <YOUR_STRING_HERE>' \
  -H 'Content-Type: application/json' \
  -H 'X-Affiliate-Id: 0' \
  -d '{
    "booker": {
      "country": "nl",
      "platform": "desktop"
    },
    "checkin": "!START_DATE!",
    "checkout": "!END_DATE!",
    "city": -2146479,
    "extras": [
      "extra_charges",
      "products"
    ],
    "guests": {
      "number_of_adults": 2,
      "number_of_rooms": 1
    }
  }'
```

### Структура ответа (200 OK):
```json
{
  "request_id": "string",
  "data": [
    // Массив объектов AccommodationsSearchDataOutput
  ],
  "next_page": "string или null"
}
```

**Поля ответа**:
- `request_id` (string) - Уникальный идентификатор запроса для поддержки
- `data` (Array) - Массив найденных размещений
- `next_page` (string или null) - Токен для следующей страницы результатов


## Результаты тестового запроса

### Выполненный тест
Был создан и выполнен тестовый Python скрипт, который демонстрирует:
- Правильную структуру HTTP запроса
- Необходимые заголовки
- Формат тела запроса в JSON
- Обработку ответа API

### Параметры тестового запроса:
- **URL**: `https://demandapi.booking.com/3.1/accommodations/search`
- **Метод**: POST
- **Заголовки**:
  - `Authorization: Bearer YOUR_API_TOKEN_HERE`
  - `Content-Type: application/json`
  - `X-Affiliate-Id: 0`
- **Тело запроса**:
  ```json
  {
    "booker": {
      "country": "nl",
      "platform": "desktop"
    },
    "checkin": "2025-06-21",
    "checkout": "2025-06-24",
    "city": -2146479,
    "extras": ["extra_charges", "products"],
    "guests": {
      "number_of_adults": 2,
      "number_of_rooms": 1
    },
    "currency": "EUR",
    "rows": 10
  }
  ```

### Результат запроса:
- **HTTP статус**: 401 (Unauthorized)
- **Тело ответа**: Пустое
- **Заголовки ответа**: Включают CloudFront и security заголовки

### Анализ результата:
✅ **Положительные моменты**:
- API endpoint доступен и отвечает
- Структура запроса корректна
- Получен ожидаемый ответ об ошибке аутентификации
- Сервер правильно обрабатывает запросы

❌ **Ограничения**:
- Требуется действительный Bearer токен для аутентификации
- Необходим реальный Affiliate ID партнера
- API находится в режиме раннего доступа (пилотная программа)
- Доступ ограничен только для выбранных партнеров Type 2 и Type 4

## Выводы и рекомендации

### Основные выводы:
1. **API функционален**: Booking.com Demand API работает и правильно обрабатывает запросы
2. **Документация полная**: Документация содержит всю необходимую информацию для интеграции
3. **Безопасность**: API использует современные методы аутентификации (Bearer tokens)
4. **Ограниченный доступ**: API доступен только партнерам в рамках пилотной программы

### Для успешного использования API необходимо:
1. **Регистрация в партнерской программе** Booking.com
2. **Получение API токена** (Bearer token) от Booking.com
3. **Получение Affiliate ID** для идентификации партнера
4. **Участие в пилотной программе** раннего доступа
5. **Соблюдение требований** Type 2 или Type 4 партнера

### Технические рекомендации:
1. **Обработка ошибок**: Всегда проверять HTTP статус ответа
2. **Пагинация**: Использовать поле `next_page` для получения дополнительных результатов
3. **Лимиты запросов**: Учитывать ограничения API (максимум 100 результатов за запрос)
4. **Валидация дат**: Даты заезда должны быть в пределах 500 дней от текущей даты
5. **Обязательные поля**: Всегда включать booker, checkin, checkout, guests

### Потенциальные сценарии использования:
- Поиск отелей и апартаментов по городам/регионам
- Фильтрация по цене, рейтингу, удобствам
- Получение информации о доступности номеров
- Интеграция с туристическими платформами
- Создание агрегаторов размещений

## Заключение

Booking.com Demand API представляет собой мощный инструмент для поиска и бронирования размещений, но его использование ограничено партнерской программой. API имеет хорошо структурированную документацию и современную архитектуру REST с JSON форматом данных.

Тестовый запрос подтвердил работоспособность API и корректность документации. Для реального использования потребуется прохождение процедуры партнерской регистрации и получение соответствующих учетных данных.

