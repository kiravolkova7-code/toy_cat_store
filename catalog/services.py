from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Возвращает QuerySet опубликованных продуктов указанной категории,
    отсортированных по имени.
    Ключ кеша формируется динамически для каждой категории.
    """
    cache_key = f'products_in_category_{category_id}'

    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).order_by('name'))

        cache.set(cache_key, products, 300)

    return products
