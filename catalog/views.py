from django.shortcuts import render
from catalog.models import Product
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


def home(request):
    return render(request, "home.html")


@csrf_protect
def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse( f'Спасибо, {name}. Сообщение получено.')
    else:
        return render(request, "contacts.html")


def home(request):
    latest_products = Product.objects.order_by('-id')[:5]

    for product in latest_products:
        print(f"ID: {product.id}, Название: {product.name}, Дата: {product.created_at}")

    context = {
        'latest_products': latest_products
    }
    return render(request, "home.html", context)
