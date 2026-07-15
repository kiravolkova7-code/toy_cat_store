from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    publish_product,
    unpublish_product,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("product/add/", ProductCreateView.as_view(), name="product-add"),
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product-edit"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
    path("product/unpublish/<int:pk>/", unpublish_product, name="unpublish-product"),
    path("product/publish/<int:pk>/", publish_product, name="publish-product"),
]
