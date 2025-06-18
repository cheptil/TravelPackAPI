#!/usr/bin/env python3
"""
Альтернативный тест TravelGate API - попытка найти публичные эндпоинты
"""

import requests
import json

def test_api_endpoints():
    """Тестирует различные эндпоинты TravelGate API"""
    
    endpoints = [
        "https://api.travelgate.com/graphql",
        "https://api.travelgate.com/",
        "https://docs.travelgate.com/api",
        "https://api.travelgate.com/health",
        "https://api.travelgate.com/status"
    ]
    
    results = []
    
    for endpoint in endpoints:
        try:
            print(f"Тестирую эндпоинт: {endpoint}")
            
            # Пробуем GET запрос
            response = requests.get(endpoint, timeout=10)
            result = {
                "endpoint": endpoint,
                "method": "GET",
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_type": response.headers.get("content-type", ""),
                "content_length": len(response.content),
                "response_preview": response.text[:500] if response.text else ""
            }
            results.append(result)
            print(f"  GET {response.status_code}: {response.headers.get('content-type', '')}")
            
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": "GET",
                "error": str(e)
            }
            results.append(result)
            print(f"  GET Error: {e}")
    
    return results

def test_graphql_introspection():
    """Пытается выполнить introspection запрос к GraphQL"""
    
    introspection_query = """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
      }
    }
    
    fragment FullType on __Type {
      kind
      name
      description
    }
    """
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": introspection_query
    }
    
    try:
        print("Пытаюсь выполнить GraphQL introspection...")
        response = requests.post(
            "https://api.travelgate.com/graphql",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        result = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "response": response.text
        }
        
        print(f"Introspection статус: {response.status_code}")
        return result
        
    except Exception as e:
        print(f"Ошибка introspection: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("=== РАСШИРЕННОЕ ТЕСТИРОВАНИЕ TRAVELGATE API ===")
    
    # Тестируем различные эндпоинты
    print("\n1. Тестирование эндпоинтов:")
    endpoint_results = test_api_endpoints()
    
    # Тестируем GraphQL introspection
    print("\n2. Тестирование GraphQL introspection:")
    introspection_result = test_graphql_introspection()
    
    # Сохраняем все результаты
    all_results = {
        "endpoint_tests": endpoint_results,
        "introspection_test": introspection_result,
        "summary": {
            "total_endpoints_tested": len(endpoint_results),
            "successful_responses": len([r for r in endpoint_results if "status_code" in r and r["status_code"] < 400]),
            "errors": len([r for r in endpoint_results if "error" in r])
        }
    }
    
    with open("/home/ubuntu/travelgate_extended_test.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nРезультаты сохранены в: /home/ubuntu/travelgate_extended_test.json")
    
    # Выводим краткую сводку
    print("\n=== КРАТКАЯ СВОДКА ===")
    for result in endpoint_results:
        if "status_code" in result:
            print(f"{result['endpoint']}: {result['status_code']} ({result['content_type']})")
        else:
            print(f"{result['endpoint']}: ERROR - {result.get('error', 'Unknown')}")

