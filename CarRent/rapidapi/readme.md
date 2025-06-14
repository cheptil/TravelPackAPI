# Анализ Trawex Car Rental API

## Обзор API

**URL:** https://rapidapi.com/nilesh160195/api/trawex-car-rental/playground/

**Базовый URL:** https://trawex-car-rental.p.rapidapi.com/

**Тип API:** REST API для аренды автомобилей

## Структура API

### Эндпоинт
- **Метод:** GET
- **Путь:** `/{CarRental}`
- **Полный URL:** `https://trawex-car-rental.p.rapidapi.com/{CarRental}`

### Параметры

#### Path Parameters
- **CarRental** (обязательный)
  - Тип: String
  - Описание: Параметр пути, определяющий конкретный ресурс или действие

### Заголовки

#### Обязательные заголовки
1. **X-RapidAPI-Host**
   - Значение: `trawex-car-rental.p.rapidapi.com`
   - Назначение: Идентификация хоста API в системе RapidAPI

2. **X-RapidAPI-Key**
   - Значение: Ваш личный API ключ от RapidAPI
   - Назначение: Авторизация и аутентификация запросов
   - Получение: https://docs.rapidapi.com/docs/keys

## Результаты тестирования

### Тест 1: Запрос без API ключа
```
URL: https://trawex-car-rental.p.rapidapi.com/test
Заголовки: X-RapidAPI-Host: trawex-car-rental.p.rapidapi.com
Результат: HTTP 401 - Invalid API key
```

**Ответ:**
```json
{
  "message": "Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info."
}
```

### Тест 2: Запрос с фиктивным API ключом
```
URL: https://trawex-car-rental.p.rapidapi.com/test
Заголовки: 
  - X-RapidAPI-Host: trawex-car-rental.p.rapidapi.com
  - X-RapidAPI-Key: fake-key-for-testing
Результат: HTTP 403 - Not subscribed
```

**Ответ:**
```json
{
  "message": "You are not subscribed to this API."
}
```

### Тест 3: Различные параметры пути
Протестированы параметры: `cars`, `rental`, `search`, `booking`, `vehicles`

**Результат:** HTTP 429 - Too many requests
```json
{
  "message": "Too many requests"
}
```

## Анализ результатов

### Система авторизации
1. **Двухуровневая авторизация:**
   - Первый уровень: Валидный API ключ (X-RapidAPI-Key)
   - Второй уровень: Подписка на API

2. **Процесс авторизации:**
   - Без ключа → 401 (Invalid API key)
   - С неверным ключом → 403 (Not subscribed)
   - С правильным ключом, но без подписки → 403 (Not subscribed)

### Ограничения по запросам
- API имеет ограничения на количество запросов (rate limiting)
- При превышении лимита возвращается HTTP 429

### Структура API
- API использует RESTful подход
- Параметр `{CarRental}` в пути определяет конкретный ресурс
- Возможные значения параметра могут включать: cars, rental, search, booking, vehicles

## Требования для использования

### Для разработчиков
1. **Регистрация на RapidAPI:**
   - Создать аккаунт на https://rapidapi.com/
   - Получить API ключ

2. **Подписка на API:**
   - Подписаться на Trawex Car Rental API
   - Выбрать подходящий тарифный план

3. **Настройка запросов:**
   ```python
   headers = {
       "X-RapidAPI-Host": "trawex-car-rental.p.rapidapi.com",
       "X-RapidAPI-Key": "ВАШ_API_КЛЮЧ"
   }
   ```

### Пример корректного запроса
```python
import requests

url = "https://trawex-car-rental.p.rapidapi.com/cars"
headers = {
    "X-RapidAPI-Host": "trawex-car-rental.p.rapidapi.com",
    "X-RapidAPI-Key": "ваш_реальный_api_ключ"
}

response = requests.get(url, headers=headers)
print(response.json())
```

## Заключение

Trawex Car Rental API представляет собой коммерческий API для работы с услугами аренды автомобилей, размещенный на платформе RapidAPI. API требует обязательной регистрации, получения API ключа и подписки на сервис. Без выполнения этих требований полноценное тестирование функциональности невозможно.

Структура API следует стандартам REST, использует JSON для обмена данными и имеет встроенные механизмы ограничения запросов для предотвращения злоупотреблений.

