# Recipebook — сайт рецептов (Django + Django REST Framework)

Веб-приложение «Recipebook» — каталог рецептов казахской и мировой кухни: ингредиенты и способ приготовления,
поиск по названию, фильтры по категории и кухне, отзывы с оценками, регистрация и вход.
Проект выполняется по неделям курса Backend; в репозитории накапливается весь пройденный материал.

## Возможности

- каталог рецептов с поиском, фильтром по категориям и национальным кухням, сортировкой;
- карточка рецепта: ингредиенты, шаги приготовления, время, порции, сложность;
- отзывы и оценки рецептов (1–5), средняя оценка;
- регистрация, вход и выход пользователей;
- админ-панель Django;
- REST API на Django REST Framework (сериализаторы, CRUD для рецептов, категорий, кухонь и отзывов,
  выборки по связанным сущностям, проверка данных и корректные коды ошибок).

## Технологии

Python 3.12, Django 5.x, Django REST Framework, SQLite, HTML/CSS/JS (шаблоны Django), Postman.

## Структура проекта

```
recipebook/
├── recipebook/            # настройки проекта (settings.py, urls.py, wsgi.py, asgi.py)
├── apps/
│   └── recipes/           # приложение (можно перенести в другой проект целиком)
│       ├── migrations/
│       ├── fixtures/      # тестовые данные
│       ├── templates/
│       ├── management/commands/seed_reviews.py
│       ├── admin.py  apps.py  forms.py  models.py  views.py  tests.py
│       ├── serializers.py     # сериализаторы DRF (недели 7–8)
│       ├── api_views.py       # представления DRF (недели 7–8)
│       └── api_urls.py        # маршруты API (недели 7–8)
├── docs/
│   ├── ER_diagram.md
│   └── Recipebook_API.postman_collection.json
├── manage.py
├── requirements.txt
└── README.md
```

## Запуск проекта

```bash
# 1. клонировать репозиторий и перейти в папку проекта
git clone <ССЫЛКА_НА_РЕПОЗИТОРИЙ>
cd recipebook

# 2. виртуальное окружение
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # macOS / Linux

# 3. зависимости
pip install -r requirements.txt

# 4. база данных
python manage.py migrate
python manage.py loaddata <[sample_data.json](apps/recipes/fixtures/sample_data.json)_apps/recipes/fixtures>   # тестовые данные
python manage.py createsuperuser                                  # для входа в /admin/

# 5. проверка и запуск
python manage.py check
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/ · Админка: http://127.0.0.1:8000/admin/ ·
API (Browsable API): http://127.0.0.1:8000/api/drf/recipes/

Необязательно: `python manage.py seed_reviews` добавляет демо-отзывы к имеющимся рецептам
(`python manage.py seed_reviews --clear` удаляет только их).

## Модели и связи

| Модель | Поля | Связи |
|---|---|---|
| `Category` | name, icon | 1 категория → много рецептов |
| `Cuisine` | name | 1 кухня → много рецептов |
| `Recipe` | title, description, ingredients, instructions, cooking_time, servings, difficulty, created_at | `category` → Category, `cuisine` → Cuisine, `author` → User (все `SET_NULL`) |
| `Review` | author_name, rating (1–5), comment, created_at | `recipe` → Recipe (`CASCADE`, `related_name="reviews"`) |

ER-диаграмма: [docs/ER_diagram.md](docs/ER_diagram.md)

```mermaid
erDiagram
    USER ||--o{ RECIPE : "author"
    CATEGORY ||--o{ RECIPE : "category"
    CUISINE ||--o{ RECIPE : "cuisine"
    RECIPE ||--o{ REVIEW : "reviews"
```

## REST API (префикс `/api/drf/`)

| Метод | URL | Назначение |
|---|---|---|
| GET, POST | `/api/drf/recipes/` | список рецептов / создание |
| GET, PUT, PATCH, DELETE | `/api/drf/recipes/<id>/` | один рецепт (GET — вместе с отзывами) |
| GET | `/api/drf/recipes/<id>/reviews/` | отзывы рецепта |
| GET, POST | `/api/drf/categories/` | список категорий / создание |
| GET, PUT, PATCH, DELETE | `/api/drf/categories/<id>/` | одна категория |
| GET | `/api/drf/categories/<id>/recipes/` | рецепты категории |
| GET, POST | `/api/drf/cuisines/` | список кухонь / создание |
| GET, PUT, PATCH, DELETE | `/api/drf/cuisines/<id>/` | одна кухня |
| GET | `/api/drf/cuisines/<id>/recipes/` | рецепты кухни |
| GET, POST | `/api/drf/reviews/` | отзывы / создание отзыва |
| GET, PUT, PATCH, DELETE | `/api/drf/reviews/<id>/` | один отзыв |

Ранее реализованные ручные JSON-маршруты (`/api/recipes/`, `/api/recipes/<id>/`) сохранены.

В ответе рецепта связанные данные выводятся рядом с идентификаторами: `category_detail`, `cuisine_detail`,
`category_name`, `cuisine_name`, `average_rating`, `reviews_count`. При записи передаются только id
(`"category": 2`, `"cuisine": 1`).

### Пример: создание рецепта

```http
POST /api/drf/recipes/
Content-Type: application/json

{
  "title": "Плов",
  "description": "Сытный рассыпчатый плов.",
  "ingredients": "1 кг риса\n1 кг моркови",
  "instructions": "Промыть рис.\nОбжарить мясо.",
  "cooking_time": 90,
  "servings": 6,
  "difficulty": "medium",
  "category": 2,
  "cuisine": 1
}
```
Ответ: `201 Created` и созданный рецепт.

### Ошибки

| Ситуация | Код | Ответ |
|---|---|---|
| рецепта / категории / кухни с таким id нет | 404 | `{"detail": "No Recipe matches the given query."}` |
| нет обязательного поля | 400 | `{"title": ["This field is required."], ...}` |
| название короче 2 символов | 400 | сообщение `validate_title` |
| несуществующий `category` / `cuisine` / `recipe` | 400 | `Invalid pk "99999" - object does not exist.` |
| оценка вне диапазона 1–5 | 400 | `Ensure this value is less than or equal to 5.` |

При удалении категории или кухни рецепты сохраняются (`SET_NULL`); при удалении рецепта удаляются его отзывы (`CASCADE`).

## Проверка работы

1. `python manage.py check` — без ошибок.
2. Postman: Import → `docs/Recipebook_API.postman_collection.json`, запустить папку «Сәтті», затем «Қателер».
   PUT и DELETE применяются только к рецепту, созданному самой коллекцией, поэтому реальные данные не затрагиваются.
3. Или открыть страницы API в браузере (DRF Browsable API) и проверить формы создания.

## Ход работы по неделям

| Неделя | Что сделано |
|---|---|
| 5 | Выбор темы, структура проекта, модели, каталог рецептов, шаблоны, авторизация |
| 6 | REST API и CRUD на обычных представлениях Django (JsonResponse) |
| 7 | Установка DRF, `ModelSerializer`, generic views, валидация, проверка в Browsable API и Postman |
| 8 | Связанные модели в API: сериализаторы Category, Cuisine, Review, CRUD, выборки по связанным сущностям, вложенный вывод, коллекция Postman, ER-диаграмма |

## Принятые решения и найденные ошибки

- **Приложение в папке `apps/`.** Приложение перенесено в `apps/recipes`, чтобы переносить его в другой проект целиком.
  В `apps.py` задано `name = "apps.recipes"` и `label = "recipes"`, чтобы не потерять миграции и данные.
  Типичная ошибка после переноса — `ModuleNotFoundError: No module named 'recipes'`: в `INSTALLED_APPS` и
  импортах нужно писать `apps.recipes`.
- **DRF под отдельным префиксом `/api/drf/`.** Так новые маршруты не конфликтуют со старыми JSON-маршрутами и не затрагивают дизайн сайта.
- **Запись — по id, чтение — вложенно.** Клиент передаёт `"category": 2`, а в ответе получает ещё и `category_detail`.
- **Предупреждение `urls.W005` (namespace не уникален).** Возникло из-за двойного `include` одного и того же `api_urls`; оставлено одно подключение.
- **`JSON parse error` в Postman.** Причиной была лишняя запятая и фигурная скобка после скопированного JSON; исправлено вручную.
