from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Product


class HomeView(ListView):
    """Список последних 6 товаров для главной страницы."""
    model = Product
    template_name = 'home.html'
    context_object_name = 'latest_products'
    def get_queryset(self):
        return Product.objects.order_by('-id')[:6]

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


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Детальная страница товара."""
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Cтраница добавления товара."""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Cтраница редактирования товара."""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Cтраница удаления товара."""
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')