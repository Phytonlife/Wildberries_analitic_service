# products/parser.py
import requests
from bs4 import BeautifulSoup
import time
import random
import json
from urllib.parse import quote
from django.utils import timezone
from products.models import Product

class WildberriesParser:
    API_SEARCH_URL = "https://search.wb.ru/exactmatch/ru/common/v4/search"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.wildberries.ru/",
    }

    @classmethod
    def parse_search(cls, search_query, pages=1):
        """Парсим через официальное API Wildberries"""
        products = []
        
        for page in range(1, pages + 1):
            try:
                # Правильный формат параметров для API
                params = {
                    "query": search_query,
                    "resultset": "catalog",
                    "page": page,
                    "sort": "popular",
                    "dest": -1257786,  # id региона (Москва)
                    "regions": "80,64,83,4,38,33,70,69,86,30,40,48,1,66,31,22,114",  # основные регионы РФ
                    "curr": "rub",  # валюта
                    "lang": "ru",   # язык
                    "locale": "ru"   # локаль
                }
                
                # Добавляем случайные задержки между запросами
                time.sleep(random.uniform(0.5, 1.5))
                
                response = requests.get(
                    cls.API_SEARCH_URL,
                    headers=cls.HEADERS,
                    params=params,
                    timeout=15  # увеличенный таймаут
                )
                
                # Проверяем статус ответа
                if response.status_code != 200:
                    print(f"Ошибка HTTP {response.status_code} для страницы {page}")
                    continue
                    
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    print(f"Не удалось разобрать JSON для страницы {page}")
                    continue
                    
                # Проверяем структуру ответа
                if not isinstance(data, dict) or not data.get("data", {}).get("products"):
                    print(f"Неверный формат ответа для страницы {page}")
                    continue
                    
                # Парсим товары из ответа
                page_products = cls._parse_api_response(data)
                products.extend(page_products)
                
                print(f"Страница {page}: найдено {len(page_products)} товаров")
                
                # Если товаров меньше ожидаемого, прекращаем парсинг
                if len(page_products) < 100:  # обычно на странице 100 товаров
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Сетевая ошибка при запросе страницы {page}: {str(e)}")
                continue
            except Exception as e:
                print(f"Неожиданная ошибка на странице {page}: {str(e)}")
                continue
        
        print(f"Всего найдено товаров: {len(products)}")
        return products

    @classmethod
    def _parse_api_response(cls, data):
        """Парсим ответ API"""
        products = []
        
        if not data.get("data", {}).get("products"):
            return products
            
        for item in data["data"]["products"]:
            try:
                product = {
                    "name": item.get("name", ""),
                    "brand": item.get("brand", ""),
                    "product_id": item.get("id", ""),
                    "price": float(item.get("priceU", 0)) / 100,
                    "sale_price": float(item.get("salePriceU", 0)) / 100,
                    "rating": item.get("reviewRating", 0),
                    "reviews_count": item.get("feedbacks", 0),
                }
                products.append(product)
            except Exception as e:
                print(f"Ошибка парсинга товара: {str(e)}")
                continue
                
        return products

    @classmethod
    def save_to_db(cls, products_data):
        """Сохраняем товары в базу"""
        created_count = 0
        
        for product_data in products_data:
            if not product_data.get("product_id"):
                continue
                
            _, created = Product.objects.update_or_create(
                product_id=product_data["product_id"],
                defaults={
                    "name": product_data["name"],
                    "brand": product_data["brand"],
                    "price": product_data["price"],
                    "sale_price": product_data["sale_price"],
                    "rating": product_data["rating"],
                    "reviews_count": product_data["reviews_count"],
                    "query": product_data.get("query", ""),
                }
            )
            
            if created:
                created_count += 1
                
        return created_count