# Анализ API Ticketmaster Discovery v2.0

## Обзор API

Ticketmaster Discovery API позволяет искать события, артистов и площадки.

### Основные характеристики:
- **Root URL**: `https://app.ticketmaster.com/discovery/v2/`
- **Аутентификация**: API ключ через параметр `apikey`
- **Лимиты**: 5000 запросов в день, 5 запросов в секунду
- **Глубокая пагинация**: до 1000 элементов (size * page < 1000)
- **Покрытие**: 230K+ событий в США, Канаде, Мексике, Австралии, Новой Зеландии, Великобритании, Ирландии и других европейских странах

### Источники данных:
- Ticketmaster
- Universe
- FrontGate Tickets
- Ticketmaster Resale (TMR)

### Примеры запросов:
1. **Все события в США**: `https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey={apikey}`
2. **Поиск по ключевому слову**: `https://app.ticketmaster.com/discovery/v2/events.json?keyword=devjam&source=universe&countryCode=US&apikey={apikey}`
3. **Музыкальные события в Лос-Анджелесе**: `https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&dmaId=324&apikey={apikey}`
4. **События конкретного артиста**: `https://app.ticketmaster.com/discovery/v2/events.json?attractionId=K8vZ917Gku7&countryCode=CA&apikey={apikey}`

## Доступные эндпоинты:



### Event Search эндпоинт

**URL**: `/discovery/v2/events`
**Метод**: GET
**Описание**: Поиск событий с фильтрацией по местоположению, дате, доступности и другим параметрам.

#### Основные параметры запроса:

| Параметр | Описание |
|----------|----------|
| `id` | Фильтр по ID события |
| `keyword` | Ключевое слово для поиска |
| `attractionId` | Фильтр по ID артиста/исполнителя |
| `venueId` | Фильтр по ID площадки |
| `postalCode` | Фильтр по почтовому индексу |
| `latlong` | Фильтр по широте и долготе (устарел) |
| `radius` | Радиус области поиска |
| `unit` | Единица измерения радиуса |
| `source` | Фильтр по источнику (Ticketmaster, Universe, FrontGate, TMR) |
| `locale` | Локаль в формате ISO (например, en-us) |
| `marketId` | Фильтр по ID рынка |
| `startDateTime` | Фильтр событий после указанной даты |
| `endDateTime` | Фильтр событий до указанной даты |
| `includeTBA` | Включить события "To Be Announced" |
| `includeTBD` | Включить события "To Be Defined" |
| `includeTest` | Включить тестовые события |
| `size` | Размер страницы ответа |
| `page` | Номер страницы |
| `sort` | Сортировка результатов |
| `onsaleStartDateTime` | Фильтр по дате начала продаж |
| `onsaleEndDateTime` | Фильтр по дате окончания продаж |
| `city` | Фильтр по городу |
| `countryCode` | Фильтр по коду страны |
| `stateCode` | Фильтр по коду штата |
| `classificationName` | Фильтр по категории (музыка, спорт и т.д.) |

#### Опции сортировки:
- `name,asc` / `name,desc` - по названию
- `date,asc` / `date,desc` - по дате
- `relevance,asc` / `relevance,desc` - по релевантности
- `distance,asc` / `distance,desc` - по расстоянию
- `name,date,asc` / `name,date,desc` - по названию и дате
- `date,name,asc` / `date,name,desc` - по дате и названию
- `distance,date,asc` - по расстоянию и дате
- `onSaleStartDate,asc` / `onSaleStartDate,desc` - по дате начала продаж
- `id,asc` - по ID
- `venueName,asc` / `venueName,desc` - по названию площадки
- `random` - случайная сортировка



#### Дополнительные параметры:
| Параметр | Описание |
|----------|----------|
| `classificationId` | Фильтр по ID классификации |
| `dmaId` | Фильтр по DMA ID |
| `localStartDateTime` | Фильтр по локальному времени начала |
| `localStartEndDateTime` | Фильтр по диапазону локального времени |
| `startEndDateTime` | Фильтр по диапазону времени начала и окончания |
| `publicVisibilityStartDateTime` | Фильтр по времени публичной видимости |
| `preSaleDateTime` | Фильтр по времени предпродажи |
| `onsaleOnStartDate` | Фильтр по дате начала продаж |
| `onsaleOnAfterStartDate` | Фильтр по дате после начала продаж |
| `collectionId` | Фильтр по ID коллекции |
| `segmentId` | Фильтр по ID сегмента |
| `segmentName` | Фильтр по названию сегмента |
| `includeFamily` | Включить семейные события |
| `promoterId` | Фильтр по ID промоутера |
| `genreId` | Фильтр по ID жанра |
| `subGenreId` | Фильтр по ID поджанра |
| `typeId` | Фильтр по ID типа |
| `subTypeId` | Фильтр по ID подтипа |
| `geoPoint` | Фильтр по географической точке |
| `preferredCountry` | Предпочтительная страна для популярности |
| `includeSpellcheck` | Включить предложения проверки орфографии |
| `domain` | Фильтр по доменам |

### Структура ответа:

**HTTP Status**: 200 - успешная операция

**Основные элементы ответа**:
- `_links` (object) - ссылки на наборы данных
- `_embedded` (object) - контейнер с данными событий
- `page` (object) - информация о текущей странице в наборе данных

### Пример запроса:
```
GET /discovery/v2/events.json?apikey={apikey}&size=1 HTTP/1.1
Host: app.ticketmaster.com
X-Target-URI: https://app.ticketmaster.com
Connection: Keep-Alive
```

Для выполнения запросов необходим API ключ, который должен быть получен через регистрацию на портале разработчиков Ticketmaster.



## Результаты тестирования API

### Тестовые запросы

Были выполнены следующие тестовые запросы для изучения поведения API:

#### 1. Запрос без API ключа
```
GET https://app.ticketmaster.com/discovery/v2/events.json?size=1&countryCode=US
```

**Результат:**
- **HTTP статус**: 401 Unauthorized
- **Ответ**:
```json
{
  "fault": {
    "faultstring": "Failed to resolve API Key variable request.queryparam.apikey",
    "detail": {
      "errorcode": "steps.oauth.v2.FailedToResolveAPIKey"
    }
  }
}
```

#### 2. Запрос с неверным API ключом
```
GET https://app.ticketmaster.com/discovery/v2/events.json?apikey=invalid_key&size=1&countryCode=US
```

**Результат:**
- **HTTP статус**: 401 Unauthorized
- **Ответ**:
```json
{
  "fault": {
    "faultstring": "Invalid ApiKey",
    "detail": {
      "errorcode": "oauth.v2.InvalidApiKey"
    }
  }
}
```

### Анализ ошибок аутентификации

API Ticketmaster Discovery корректно обрабатывает ошибки аутентификации:

1. **Отсутствие API ключа** - возвращает ошибку `steps.oauth.v2.FailedToResolveAPIKey`
2. **Неверный API ключ** - возвращает ошибку `oauth.v2.InvalidApiKey`

Оба случая возвращают HTTP статус 401 и структурированный JSON с описанием ошибки.

## Структура успешного ответа

На основе документации API, успешный ответ имеет следующую структуру:

### Основные компоненты ответа

#### 1. Метаданные (`_links`)
Содержит ссылки для навигации по результатам:
- `self` - ссылка на текущий запрос
- `next` - ссылка на следующую страницу результатов
- `prev` - ссылка на предыдущую страницу (если применимо)

#### 2. Данные событий (`_embedded.events`)
Массив объектов событий, каждое из которых содержит:

**Основная информация:**
- `id` - уникальный идентификатор события
- `name` - название события
- `type` - тип объекта (всегда "event")
- `url` - ссылка на страницу события на Ticketmaster
- `locale` - локаль (например, "en-us")
- `test` - флаг тестового события

**Даты и время:**
- `dates.start.localDate` - локальная дата начала
- `dates.start.localTime` - локальное время начала
- `dates.start.dateTime` - дата и время в UTC
- `dates.timezone` - часовой пояс
- `dates.status.code` - статус события (например, "onsale")

**Продажи:**
- `sales.public.startDateTime` - начало публичных продаж
- `sales.public.endDateTime` - окончание публичных продаж

**Классификация:**
- `classifications[0].segment.name` - сегмент (например, "Music")
- `classifications[0].genre.name` - жанр (например, "Rock")
- `classifications[0].subGenre.name` - поджанр

**Изображения:**
- `images[]` - массив изображений с различными соотношениями сторон

#### 3. Вложенные данные (`_embedded`)
Каждое событие может содержать:

**Площадки (`venues`):**
- `name` - название площадки
- `city.name` - город
- `state.stateCode` - код штата
- `country.countryCode` - код страны
- `address.line1` - адрес
- `location.latitude/longitude` - координаты
- `postalCode` - почтовый индекс

**Исполнители (`attractions`):**
- `name` - название исполнителя/группы
- `id` - уникальный идентификатор
- `images[]` - изображения исполнителя
- `classifications[]` - классификация по жанрам

#### 4. Информация о пагинации (`page`)
- `size` - размер страницы
- `totalElements` - общее количество элементов
- `totalPages` - общее количество страниц
- `number` - номер текущей страницы (начиная с 0)

## Практические рекомендации

### Получение API ключа
Для работы с API необходимо:
1. Зарегистрироваться на https://developer.ticketmaster.com/
2. Создать приложение в личном кабинете
3. Получить API ключ для использования в запросах

### Лимиты использования
- **Дневной лимит**: 5000 запросов в день
- **Лимит скорости**: 5 запросов в секунду
- Возможно увеличение лимитов по запросу при соблюдении условий использования

### Рекомендуемые параметры для начала работы
```
GET /discovery/v2/events.json?apikey={your_key}&size=20&countryCode=US&sort=date,asc
```

### Обработка ошибок
Всегда проверяйте HTTP статус ответа:
- **200** - успешный запрос
- **401** - ошибка аутентификации
- **429** - превышение лимита запросов
- **500** - внутренняя ошибка сервера

## Заключение

API Ticketmaster Discovery представляет собой мощный инструмент для поиска событий с богатой функциональностью фильтрации и сортировки. API хорошо документирован, имеет понятную структуру ответов и корректно обрабатывает ошибки. 

Основные преимущества:
- Обширная база данных событий (230K+)
- Глобальное покрытие
- Детальная информация о событиях, площадках и исполнителях
- Гибкие возможности фильтрации
- Поддержка пагинации
- Высококачественные изображения

Для полноценного использования требуется регистрация и получение API ключа, что является стандартной практикой для коммерческих API.

