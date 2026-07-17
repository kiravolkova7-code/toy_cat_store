from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from django.views.decorators.cache import cache_page

from catalog.models import Product, Category
from .services import get_products_by_category


class HomeView(ListView):
    """Список последних 6 товаров для главной страницы."""

    model = Product
    template_name = "home.html"
    context_object_name = "latest_products"

    def get_queryset(self):
        qs = Product.objects.all()

        user = self.request.user

        if not user.is_authenticated:
            return qs.filter(is_published=True).order_by("-id")[:6]

        if user.has_perm("catalog.delete_product"):
            return qs.order_by("-id")[:6]

        filtered_qs = qs.filter(is_published=True) | qs.filter(owner=user)

        return filtered_qs.order_by("-id")[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(csrf_protect, name="dispatch")
class ContactsView(View):
    """
    Обработка формы контактов.
    """

    template_name = "contacts.html"
    success_url = reverse_lazy("catalog:home")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}. Сообщение получено.")


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Детальная страница товара."""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied
        self.object.is_published = False
        self.object.save()
        return super().get(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request_user"] = self.request.user
        return kwargs


class OwnerOrModeratorMixin(UserPassesTestMixin):
    """Миксин разрешает доступ владельцу объекта или пользователю с правом удаления."""

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm("catalog.delete_product")


class ProductUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request_user"] = self.request.user
        return kwargs


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    """Cтраница удаления товара."""

    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


@permission_required("catalog.can_unpublish_product", raise_exception=True)
def publish_product(request, pk):
    """
    Делает продукт видимым на сайте.
    Доступно пользователям с правом can_unpublish_product.
    """
    product = get_object_or_404(Product, pk=pk)

    if not product.is_published:
        product.is_published = True
        product.save()

    return redirect("catalog:product-detail", pk=pk)


@permission_required("catalog.can_unpublish_product", raise_exception=True)
def unpublish_product(request, pk):
    """
    Скрывает продукт с сайта.
    Доступно пользователям с правом can_unpublish_product.
    """
    product = get_object_or_404(Product, pk=pk)

    if product.is_published:
        product.is_published = False
        product.save()

    return redirect("catalog:product-detail", pk=pk)

@method_decorator(cache_page(300), name='dispatch')
class CategoryProductListView(ListView):
    """Список всех опубликованных продуктов в выбранной категории."""
    model = Product
    template_name = "product_list_by_category.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return get_products_by_category(self.category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        return context


class CategoryListView(ListView):
    """Страница со списком всех доступных категорий."""
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.all().order_by('name')
