# Анализ API GeoDB Cities

## Общая информация
- **URL**: https://rapidapi.com/wirefreethought/api/geodb-cities
- **Описание**: API для получения данных о городах, регионах, странах и островах по всему миру
- **Источники данных**: GeoNames и WikiData
- **Лицензия**: Creative Commons (http://creativecommons.org/licenses/by/3.0)

## Основные возможности
- Фильтрация мест по префиксу названия, стране, местоположению, часовому поясу и минимальному населению
- Поиск мест рядом с городом или координатами
- Отображение результатов на нескольких языках (английский, французский, немецкий, итальянский, португальский, русский, испанский)
- Сортировка по названию, коду страны, высоте и населению
- Получение детальной информации о местах (GPS координаты, часовой пояс, население, высота над уровнем моря, текущее время)
- Интеграция с WikiData

## Тарифные планы
- **BASIC**: $0.00/месяц
- **PRO**: $10.00/месяц  
- **ULTRA**: $25.00/месяц

## Основные эндпоинты

### GET Cities
**URL**: `https://wft-geo-db.p.rapidapi.com/v1/geo/cities`

**Параметры запроса**:
- `types` (optional) - Типы городов (CITY | ADM2)
- `location` (optional) - Координаты в формате ISO-6709: ±DD.DDDD±DDD.DDDD
- `radius` (optional) - Радиус поиска от указанного местоположения (по умолчанию: 0)
- `distanceUnit` (optional) - Единица измерения расстояния: MI | KM
- `countryIds` (optional) - Коды стран (через запятую)
- `excludedCountryIds` (optional) - Исключаемые коды стран
- `timeZoneIds` (optional) - Идентификаторы часовых поясов

### Другие эндпоинты
- Admin Divisions - административные подразделения
- Countries - страны
- Country Details - детали стран
- Country Places - места в стране
- Country Regions - регионы стран
- City Details - детали городов
- Cities Near City - города рядом с городом
- Cities Near Location - города рядом с координатами

## Заголовки для запросов
- `X-RapidAPI-Host`: wft-geo-db.p.rapidapi.com
- `X-RapidAPI-Key`: [API ключ]

## Пример curl запроса
```bash
curl --request GET \
  --url 'https://wft-geo-db.p.rapidapi.com/v1/geo/cities?countryIds=RU' \
  --header 'x-rapidapi-host: wft-geo-db.p.rapidapi.com' \
  --header 'x-rapidapi-key: [API_KEY]'
```



## Результаты тестирования API

### Тестовый запрос без API ключа
Выполнен запрос к эндпоинту:
```
GET https://wft-geo-db.p.rapidapi.com/v1/geo/cities?countryIds=RU&limit=5
```

**Результат**: 
- Статус ответа: 401 (Unauthorized)
- Сообщение об ошибке: `{"message":"Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info."}`

Это подтверждает, что API требует авторизацию через RapidAPI с действительным API ключом.

### Структура ответа API (на основе демо)
Из демо-интерфейса видно, что API возвращает данные в следующем формате:

**Пример ответа для эндпоинта `/v1/geo/places`:**
```json
{
  "data": [
    {
      "name": "Abu Dhabi",
      "population": 1483000,
      "location": "24.451111111+54.396944444",
      "country": "United Arab Emirates"
    },
    {
      "name": "Ajman", 
      "population": 490035,
      "location": "25.399444444+55.479722222",
      "country": "United Arab Emirates"
    }
  ],
  "metadata": {
    "currentOffset": 0,
    "totalCount": 5496
  }
}
```

### Основные поля в ответе:
- **name** - название города/места
- **population** - население
- **location** - координаты в формате "широта+долгота"
- **country** - название страны

### Параметры запроса:
- **namePrefix** - префикс названия места
- **types** - типы мест (CITY, ADM2)
- **minPopulation** - минимальное население
- **location** - координаты для поиска рядом
- **radius** - радиус поиска
- **countryIds** - коды стран
- **excludedCountryIds** - исключаемые коды стран
- **sort** - сортировка результатов
- **language** - язык ответа

### Выводы:
1. API требует регистрацию на RapidAPI и получение API ключа
2. Базовый план (BASIC) бесплатный - $0.00/месяц
3. API предоставляет богатую функциональность для работы с географическими данными
4. Поддерживает множественные языки включая русский
5. Данные обновляются периодически из GeoNames и WikiData
6. API следует стандартам REST и включает HATEOAS-ссылки для пагинации

