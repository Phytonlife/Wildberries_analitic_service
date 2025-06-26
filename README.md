
# Wildberries Product Analytics API

## Описание проекта

REST API для сбора, хранения и анализа данных о товарах с сайта Wildberries.

### Реализовано:

✅ Парсинг товаров по пользовательскому запросу (категория или поисковое слово)  
✅ Сохранение данных о товарах в базу данных  
✅ API-эндпоинты для получения списка товаров с фильтрацией и поиском  
✅ Дополнительные аналитические эндпоинты (гистограмма цен, рейтинг скидок, список брендов)

---

## Установка и запуск проекта

### 1. Клонирование репозитория:

```bash
git clone https://github.com/Phytonlife/Wildberries_analitic_service.git
cd wildberries_analytics
```

### 2. Создание и активация виртуального окружения:

**Linux / MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей:

```bash
pip install -r requirements.txt
```

### 4. Применение миграций:

```bash
python manage.py migrate
```

### 5. Запуск сервера разработки:

```bash
python manage.py runserver
```

---

## API эндпоинты

### 1. Список товаров с фильтрацией и поиском  
**URL:** `/api/products/`  
**Метод:** `GET`  

**Параметры фильтрации (Query Params):**
- `min_price` — минимальная цена
- `max_price` — максимальная цена
- `min_rating` — минимальный рейтинг
- `min_reviews` — минимальное количество отзывов
- `search` — поиск по названию товара

**Пример запроса:**
```
GET /api/products/?min_price=5000&min_rating=4
```

---

### 2. Гистограмма цен  
**URL:** `/api/products/histogram/`  
**Метод:** `GET`  
**Описание:** Возвращает распределение количества товаров по ценовым диапазонам.

---

### 3. Рейтинг скидок  
**URL:** `/api/products/discount-rating/`  
**Метод:** `GET`  
**Описание:** Возвращает список товаров, отсортированный по размеру скидки.

---

### 4. Список брендов  
**URL:** `/api/products/brands/`  
**Метод:** `GET`  
**Описание:** Список уникальных брендов среди товаров.

---

### 5. Парсинг товаров  
**URL:** `/api/products/parse/`  
**Метод:** `POST`  
**Описание:** Запуск парсинга товаров с Wildberries по запросу пользователя.

**Пример запроса:**

```json
POST /api/products/parse/
Body: {
  "query": "ноутбук"
}
```

---

## Технологии

- Python 3.10.0
- Django
- Django REST Framework
- SQLite (по умолчанию)

---


