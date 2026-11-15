"""9-апта: беттерге бөлу (пагинация) – бір бетте 5 жазба."""
from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    page_size = 5
    # ?page=2  – екінші бет. Жоқ бет сұралса (мысалы ?page=999) – 404 {"detail": "Invalid page."}
