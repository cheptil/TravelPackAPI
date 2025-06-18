#!/usr/bin/env python3
"""
Тестовый скрипт для исследования AXS API endpoints
"""

import requests
import json
from urllib.parse import urljoin

class AXSAPITester:
    def __init__(self):
        self.base_urls = [
            "https://api.axs.com/",
            "https://www.axs.com/api/",
            "https://solutions.axs.com/api/",
            "https://developers.axs.com/api/"
        ]
        self.common_endpoints = [
            "v1/",
            "v2/",
            "events",
            "venues",
            "tickets",
            "health",
            "status",
            "info",
            "docs",
            "swagger",
            "openapi.json"
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }

    def test_endpoint(self, url):
        """Тестирует один endpoint"""
        try:
            print(f"Тестирую: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_type': response.headers.get('content-type', ''),
                'content_length': len(response.content),
                'response_preview': ''
            }
            
            # Попробуем получить превью ответа
            if response.status_code == 200:
                try:
                    if 'application/json' in result['content_type']:
                        json_data = response.json()
                        result['response_preview'] = json.dumps(json_data, indent=2)[:500]
                    else:
                        result['response_preview'] = response.text[:500]
                except:
                    result['response_preview'] = "Не удалось декодировать ответ"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'error': str(e),
                'status_code': None
            }

    def run_tests(self):
        """Запускает тесты для всех комбинаций URL и endpoints"""
        results = []
        
        print("Начинаю тестирование AXS API endpoints...")
        print("=" * 60)
        
        for base_url in self.base_urls:
            print(f"\nТестирую базовый URL: {base_url}")
            
            # Тестируем базовый URL
            result = self.test_endpoint(base_url)
            results.append(result)
            
            # Тестируем endpoints
            for endpoint in self.common_endpoints:
                full_url = urljoin(base_url, endpoint)
                result = self.test_endpoint(full_url)
                results.append(result)
        
        return results

    def analyze_results(self, results):
        """Анализирует результаты тестирования"""
        print("\n" + "=" * 60)
        print("АНАЛИЗ РЕЗУЛЬТАТОВ")
        print("=" * 60)
        
        successful_requests = [r for r in results if r.get('status_code') == 200]
        interesting_responses = [r for r in results if r.get('status_code') in [200, 401, 403, 404]]
        
        print(f"Всего запросов: {len(results)}")
        print(f"Успешных ответов (200): {len(successful_requests)}")
        print(f"Интересных ответов: {len(interesting_responses)}")
        
        if successful_requests:
            print("\nУСПЕШНЫЕ ЗАПРОСЫ:")
            for result in successful_requests:
                print(f"✓ {result['url']} - {result['content_type']}")
                if result['response_preview']:
                    print(f"  Превью: {result['response_preview'][:100]}...")
        
        print("\nВСЕ ИНТЕРЕСНЫЕ ОТВЕТЫ:")
        for result in interesting_responses:
            status = result.get('status_code', 'ERROR')
            print(f"{status}: {result['url']}")
            if result.get('error'):
                print(f"  Ошибка: {result['error']}")
        
        return results

if __name__ == "__main__":
    tester = AXSAPITester()
    results = tester.run_tests()
    tester.analyze_results(results)
    
    # Сохраняем результаты в файл
    with open('/home/ubuntu/axs_api_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nРезультаты сохранены в: /home/ubuntu/axs_api_test_results.json")

