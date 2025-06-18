#!/bin/bash

# Демонстрационные curl команды для API Musement
# Показывает, как бы выполнялись реальные запросы при наличии credentials

echo "=== ДЕМОНСТРАЦИЯ CURL КОМАНД ДЛЯ API MUSEMENT ==="
echo

# Переменные (в реальном использовании заменить на актуальные значения)
BASE_URL="https://sandbox-api.musement.com"
APPLICATION_VALUE="your-application-value"
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"

echo "ВАЖНО: Для реального использования необходимы credentials от Musement"
echo "Контакты для получения доступа:"
echo "- Strategic partnerships: business@musement.com"
echo "- API distribution: api-distribution@tui.com"
echo

echo "1. АУТЕНТИФИКАЦИЯ (получение access token)"
echo "================================================"
echo "curl -X POST '$BASE_URL/login' \\"
echo "  -H 'X-Musement-Application: $APPLICATION_VALUE' \\"
echo "  -H 'X-Musement-Version: 3.4.0' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  --data-raw '{"
echo "    \"client_id\": \"$CLIENT_ID\","
echo "    \"client_secret\": \"$CLIENT_SECRET\","
echo "    \"grant_type\": \"client_credentials\""
echo "  }'"
echo

echo "Ожидаемый ответ:"
echo "{"
echo "  \"access_token\": \"0GYzMGM5YjEyZjkzYzI0MGUON2Y4NDdmZm1MjVhYTkzNTY5NWhYTzmNGIzNzIxZTFhZjg3NzYyGYYQ\","
echo "  \"expires_in\": 3600,"
echo "  \"token_type\": \"bearer\","
echo "  \"scope\": null"
echo "}"
echo

echo "2. ПОИСК АКТИВНОСТЕЙ"
echo "================================================"
echo "# После получения access_token используем его в заголовке Authorization"
echo "ACCESS_TOKEN=\"полученный_access_token\""
echo
echo "curl -X GET '$BASE_URL/activities?city_in=1&limit=10' \\"
echo "  -H 'X-Musement-Application: $APPLICATION_VALUE' \\"
echo "  -H 'X-Musement-Version: 3.4.0' \\"
echo "  -H 'Authorization: Bearer \$ACCESS_TOKEN'"
echo

echo "3. ПОЛУЧЕНИЕ ИНФОРМАЦИИ ОБ АКТИВНОСТИ"
echo "================================================"
echo "ACTIVITY_UUID=\"uuid-активности-из-предыдущего-запроса\""
echo
echo "curl -X GET '$BASE_URL/activities/\$ACTIVITY_UUID' \\"
echo "  -H 'X-Musement-Application: $APPLICATION_VALUE' \\"
echo "  -H 'X-Musement-Version: 3.4.0' \\"
echo "  -H 'Authorization: Bearer \$ACCESS_TOKEN'"
echo

echo "4. ПОИСК С ДОПОЛНИТЕЛЬНЫМИ ПАРАМЕТРАМИ"
echo "================================================"
echo "curl -X GET '$BASE_URL/activities' \\"
echo "  -H 'X-Musement-Application: $APPLICATION_VALUE' \\"
echo "  -H 'X-Musement-Version: 3.4.0' \\"
echo "  -H 'Authorization: Bearer \$ACCESS_TOKEN' \\"
echo "  -G \\"
echo "  --data-urlencode 'city_in=1' \\"
echo "  --data-urlencode 'available_from=2025-07-01' \\"
echo "  --data-urlencode 'available_to=2025-07-31' \\"
echo "  --data-urlencode 'category_in=new-activities' \\"
echo "  --data-urlencode 'limit=20'"
echo

echo "5. ПОЛУЧЕНИЕ СТРАН"
echo "================================================"
echo "curl -X GET '$BASE_URL/countries' \\"
echo "  -H 'X-Musement-Application: $APPLICATION_VALUE' \\"
echo "  -H 'X-Musement-Version: 3.4.0' \\"
echo "  -H 'Authorization: Bearer \$ACCESS_TOKEN'"
echo

echo "6. ПОЛУЧЕНИЕ ГОРОДОВ"
echo "================================================"
echo "curl -X GET '$BASE_URL/cities' \\"
echo "  -H 'X-Musement-Application: $APPLICATION_VALUE' \\"
echo "  -H 'X-Musement-Version: 3.4.0' \\"
echo "  -H 'Authorization: Bearer \$ACCESS_TOKEN'"
echo

echo "=== ЗАКЛЮЧЕНИЕ ==="
echo "Эти команды показывают структуру запросов к API Musement."
echo "Для реального тестирования необходимо:"
echo "1. Получить sandbox credentials от Musement"
echo "2. Заменить placeholder значения на реальные"
echo "3. Выполнить команды в указанной последовательности"

