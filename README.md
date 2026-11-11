## Модельдер

| Модель | Өрістер |
|---|---|
| Category | name, icon |
| Cuisine | name |
| Recipe | title, description, ingredients, instructions, cooking_time, servings, difficulty, category (FK), cuisine (FK), created_at |
| Review | recipe (FK), author_name, rating (1-5), comment, created_at |

```mermaid
erDiagram
    CATEGORY ||--o{ RECIPE : groups
    CUISINE ||--o{ RECIPE : "belongs to"
    RECIPE ||--o{ REVIEW : has

    CATEGORY {
        int id
        string name
        string icon
    }
    CUISINE {
        int id
        string name
    }
    RECIPE {
        int id
        string title
        text description
        text ingredients
        text instructions
        int cooking_time
        int servings
        string difficulty
        datetime created_at
    }
    REVIEW {
        int id
        string author_name
        int rating
        text comment
        datetime created_at
    }
```

## Іске қосу (деректермен)

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py loaddata sample_data
    python manage.py runserver

Сайт: http://127.0.0.1:8000/ , админ панель: http://127.0.0.1:8000/admin/