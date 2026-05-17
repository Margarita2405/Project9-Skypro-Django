from django.core.cache import cache
from django.shortcuts import get_object_or_404

from catalog.models import Category


def get_products_by_category(category_id):
    """
    Возвращает список продуктов для категории с кешированием.
    Ключ: category_{id}
    TTL: 900 секунд (15 минут)
    """
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)

    if products is None:
        # Проверяем существование категории и получаем продукты
        category = get_object_or_404(Category, pk=category_id)
        products = category.products.all().order_by("-created_at")
        cache.set(cache_key, products, 60 * 15)

    return products
