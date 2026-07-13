from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from catalog.models import Product


class HomeView(ListView):
    """Список последних 5 товаров для главной страницы."""
    model = Product
    template_name = 'home.html'
    context_object_name = 'latest_products'
    def get_queryset(self):
        return Product.objects.order_by('-id')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(csrf_protect, name='dispatch')
class ContactsView(View):
    """
    Обработка формы контактов.
    """
    template_name = "contacts.html"
    success_url = reverse_lazy('catalog:home')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}. Сообщение получено.')


class ProductDetailView(DetailView):
    """Детальная страница товара."""
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'