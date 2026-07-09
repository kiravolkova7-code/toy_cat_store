from django.shortcuts import render
from catalog.models import Product


def home(request):
    return render(request, "home.html")


def contacts(request):
    return render(request, "contacts.html")


def home(request):
    latest_products = Product.objects.order_by('-id')[:5]

    print("--- Последние 5 созданных продуктов ---")
    for product in latest_products:
        print(f"ID: {product.id}, Название: {product.name}, Дата: {product.created_at}")
    print("-------------------------------------")

    context = {
        'latest_products': latest_products
    }
    return render(request, "home.html", context)
