# Анализ API 2GIS Places

## Обзор API
Places API выполняет поиск организаций, зданий и мест.

### Возможности поиска:
- По названию компании ("Moos Hair Dressing")
- По сфере деятельности ("restaurants" или "music instrument stores")
- С геотегами ("Al Mankhool flowers")
- По атрибутам товаров и услуг ("Italian cuisine café" или "Sauna with a pool")
- По номеру телефона или веб-сайту ("97143017777" или "www.marinaviewhotel.com")
- Без указания текстового запроса (в здании, в категории, в городе)
- По makani ("12991 75289")

## Формат запроса
Базовый URL: `https://catalog.api.2gis.com/3.0/items`

### Обязательные компоненты:
1. **Поисковый запрос** (что искать):
   - Текстовый запрос (`q` параметр)
   - Фильтр по атрибуту
   - ID объекта или категории
   - Известные атрибуты (телефон, сайт, налоговый номер)

2. **Географическое ограничение** (где искать):
   - В текстовом запросе (`q` параметр)
   - По ID города, здания, станции метро
   - По региону поиска (радиус, прямоугольная область, произвольная область)

3. **API ключ**

### Пример запроса:
```
https://catalog.api.2gis.com/3.0/items?q=cafe&location=37.630866,55.752256&key=YOUR_KEY
```

Параметры:
- `q=cafe` - поиск по запросу "cafe"
- `location=37.630866,55.752256` - географические координаты
- `key=YOUR_KEY` - API ключ

## Формат ответа
Ответ возвращается в формате JSON:

```json
{
    "meta": {
        "api_version": "3.0.448950",
        "code": 200,
        "issue_date": "20200626"
    },
    "result": {
        "items": [
            {
                "address_comment": "3, 5 floor",
                "address_name": "Nikolskaya, 25",
                "id": "70000001031668425",
                "name": "MCK, lounge bar chain",
                "type": "branch"
            }
        ],
        "total": 5926
    }
}
```

### Параметры по умолчанию:
- `id` - идентификатор объекта
- `name` - название объекта
- `type` - тип объекта
- `address_name` - адрес
- `address_comment` - комментарий к адресу




## Примеры запросов

### Ограничение результатов поиска
Для ограничения количества объектов в результатах поиска используются параметры:
- `page_size` - количество объектов на странице (максимум 10 для demo key)
- `page` - номер страницы (максимум 5 для demo key)

```
https://catalog.api.2gis.com/3.0/items?q=Moscow cafe&type=branch&page_size=10&page=1&key=YOUR_KEY
```

### Поиск по текстовому параметру
```
https://catalog.api.2gis.com/3.0/items?q=Moscow cafe&type=branch&key=YOUR_KEY
```

### Поиск в радиусе
```
https://catalog.api.2gis.com/3.0/items?q=cafe&type=branch&point=37.416469%2C55.619325&radius=1000&key=YOUR_KEY
```

### Поиск в радиусе с сортировкой по расстоянию
```
https://catalog.api.2gis.com/3.0/items?q=cafe&point=37.545423%2C55.740693&radius=1000&location=37.545423%2C55.740693&sort=distance&key=YOUR_KEY
```

### Поиск с указанием точки поиска
```
https://catalog.api.2gis.com/3.0/items?q=cafe&location=37.545423%2C55.740693&key=YOUR_KEY
```

### Поиск в прямоугольной области
```
https://catalog.api.2gis.com/3.0/items?q=cafe&fields=items.point&point1=37.602631%2C55.764592&point2=37.648702%2C55.743089&key=YOUR_KEY
```

### Поиск в произвольной области (полигон)
```
https://catalog.api.2gis.com/3.0/items?q=cafe&fields=items.point&polygon=POLYGON((37.5930 55.7667,37.6494 55.7667,37.6494 55.7405,37.5930 55.7405,37.5930 55.7667))&key=YOUR_KEY
```

### Поиск в конкретном городе
1. Найти city_id:
```
https://catalog.api.2gis.com/3.0/items?q=Moscow&key=YOUR_KEY
```

2. Использовать city_id в запросе:
```
https://catalog.api.2gis.com/3.0/items?q=cafe&fields=items.point&city_id=4504222397630173&key=YOUR_KEY
```

### Поиск с сортировкой по рейтингу
```
https://catalog.api.2gis.com/3.0/items?q=beauty&city_id=4504222397630173&sort=rating&key=YOUR_KEY
```

### Поиск рядом со станцией метро
```
https://catalog.api.2gis.com/3.0/items?q=metro kosino beauty&city_id=4504222397630173&key=YOUR_KEY
```

### Поиск с фильтрацией по времени работы и наличию сайта
```
https://catalog.api.2gis.com/3.0/items?q=beauty&city_id=4504222397630173&work_time=thu,09:00&has_site=true&key=YOUR_KEY
```

### Поиск по номеру телефона
```
https://catalog.api.2gis.com/3.0/items/byphone?phone=+74951234567&key=YOUR_KEY
```

### Поиск по веб-сайту
```
https://catalog.api.2gis.com/3.0/items/bysite?site=mcdonalds.ru&key=YOUR_KEY
```

## Ключевые параметры API:
- `q` - текстовый запрос
- `type` - тип объекта (branch, building, etc.)
- `point` - координаты точки (долгота,широта)
- `radius` - радиус поиска в метрах
- `location` - координаты для сортировки по расстоянию
- `city_id` - ID города
- `fields` - дополнительные поля в ответе
- `sort` - сортировка (distance, rating)
- `page_size` - размер страницы
- `page` - номер страницы
- `key` - API ключ


## Результаты тестирования API

### Тестовая среда
- **Дата тестирования**: 14 июня 2025
- **API версия**: 3.0.18881
- **Демо-ключ**: "demo" (работает для тестирования)
- **Базовый URL**: https://catalog.api.2gis.com/3.0/items

### Проведенные тесты

#### 1. Поиск кафе в Москве
**Параметры запроса:**
```
q=cafe
location=37.630866,55.752256
key=demo
page_size=5
```

**Результат:**
- ✅ Статус: 200 (успешно)
- 📊 Всего найдено: 168 объектов
- 📋 Возвращено: 5 объектов
- 🏢 Примеры найденных мест:
  - "Мясо&Рыба, ресторан" (Тверская street, 23/12)
  - "Дымзавод, лаундж-бар" (Болотная набережная, 3 ст4)
  - "Тануки, сеть японских ресторанов" (Пятницкая street, 53)

#### 2. Поиск ресторанов с дополнительными полями
**Параметры запроса:**
```
q=restaurant
location=37.630866,55.752256
key=demo
page_size=3
fields=items.point,items.contact_groups,items.schedule
```

**Результат:**
- ✅ Статус: 200 (успешно)
- 📊 Всего найдено: 120 объектов
- 📋 Возвращено: 3 объекта
- ℹ️ Дополнительные поля не были возвращены (возможно, требуется платный доступ)

#### 3. Поиск в радиусе с сортировкой по расстоянию
**Параметры запроса:**
```
q=pizza
point=37.630866,55.752256
radius=1000
location=37.630866,55.752256
sort=distance
key=demo
page_size=3
```

**Результат:**
- ✅ Статус: 200 (успешно)
- 📊 Всего найдено: 73 объекта
- 📋 Возвращено: 3 объекта
- 🍕 Найдены пиццерии в радиусе 1 км от центра Москвы

#### 4. Поиск по типу объекта (банки)
**Параметры запроса:**
```
q=bank
type=branch
location=37.630866,55.752256
key=demo
page_size=3
```

**Результат:**
- ✅ Статус: 200 (успешно)
- 📊 Всего найдено: 91 объект
- 📋 Возвращено: 3 объекта
- 🏦 Примеры найденных банков:
  - СберБанк (Лубянский проезд, 17)
  - Альфа-банк (улица Кузнецкий Мост, 9/10)
  - Банк ВТБ (Красная площадь, 3)

### Анализ структуры ответа API

#### Метаданные (meta)
```json
{
  "api_version": "3.0.18881",
  "code": 200,
  "issue_date": "20250614"
}
```

#### Результаты (result)
```json
{
  "items": [...],  // Массив найденных объектов
  "total": 168     // Общее количество найденных объектов
}
```

#### Структура объекта (item)
Каждый объект содержит следующие поля:

**Обязательные поля:**
- `id` - уникальный идентификатор объекта
- `name` - название организации/места
- `type` - тип объекта (обычно "branch")
- `address_name` - адрес
- `address_comment` - дополнительная информация об адресе (этаж, офис)

**Дополнительные поля:**
- `ads` - рекламная информация
  - `text` - рекламный текст
  - `link.text` - текст ссылки
  - `link.value` - URL ссылки
  - `text_warning` - предупреждающий текст (юридическая информация)

### Особенности работы с API

#### ✅ Что работает хорошо:
1. **Демо-ключ**: Ключ "demo" позволяет тестировать API без регистрации
2. **Быстрый ответ**: API отвечает быстро (< 1 сек)
3. **Качественные данные**: Возвращает актуальную информацию о местах
4. **Гибкий поиск**: Поддерживает различные типы поисковых запросов
5. **Географическая привязка**: Хорошо работает с координатами и радиусом поиска

#### ⚠️ Ограничения демо-ключа:
1. **Размер страницы**: Максимум 10 объектов на страницу
2. **Количество страниц**: Максимум 5 страниц
3. **Дополнительные поля**: Некоторые поля требуют платного доступа
4. **Специальные методы**: Поиск по телефону, сайту, налоговому номеру требует отдельного доступа

#### 🔧 Технические детали:
- **Кодировка**: UTF-8, поддержка кириллицы
- **Формат ответа**: JSON
- **HTTP методы**: GET
- **CORS**: Поддерживается
- **Кэширование**: Ответы не кэшируются (Cache-Control: no-store)

### Рекомендации по использованию

#### Для разработчиков:
1. **Начните с демо-ключа** для изучения API
2. **Используйте параметр location** для более точных результатов
3. **Комбинируйте текстовый поиск с географическими ограничениями**
4. **Обрабатывайте ошибки** - API возвращает детальную информацию об ошибках
5. **Учитывайте лимиты** демо-ключа при планировании приложения

#### Для бизнеса:
1. **Качественные данные**: API предоставляет актуальную информацию о местах
2. **Реклама**: В результатах присутствует рекламная информация
3. **Масштабируемость**: Для продакшена потребуется платный ключ
4. **Интеграция**: API легко интегрируется в веб и мобильные приложения

### Примеры использования

#### Простой поиск кафе:
```bash
curl "https://catalog.api.2gis.com/3.0/items?q=cafe&location=37.630866,55.752256&key=demo"
```

#### Поиск в радиусе с сортировкой:
```bash
curl "https://catalog.api.2gis.com/3.0/items?q=restaurant&point=37.630866,55.752256&radius=500&sort=distance&key=demo"
```

#### Поиск по типу объекта:
```bash
curl "https://catalog.api.2gis.com/3.0/items?q=bank&type=branch&location=37.630866,55.752256&key=demo"
```

### Заключение

API 2GIS Places показал отличные результаты в тестировании:
- ✅ Стабильная работа
- ✅ Качественные данные
- ✅ Гибкие возможности поиска
- ✅ Хорошая документация
- ✅ Возможность бесплатного тестирования

API подходит для создания приложений поиска мест, интеграции карт, геолокационных сервисов и других задач, связанных с поиском организаций и мест.

