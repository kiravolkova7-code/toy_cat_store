from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView
)

app_name = 'blogs'

urlpatterns = [
    path('', BlogListView.as_view(), name='blogpost-list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blogpost-detail'),
    path('create/', BlogCreateView.as_view(), name='blogpost-create'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blogpost-update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blogpost-delete'),
]
