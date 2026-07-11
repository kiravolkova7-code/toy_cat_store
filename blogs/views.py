from itertools import product

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import BlogPost
from blogs.forms import BlogForm


class BlogListView(ListView):
    """Список опубликованных записей блога."""
    model = BlogPost
    template_name = 'blogpost-list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    """Детальный просмотр одной записи с подсчетом просмотров."""
    model = BlogPost
    template_name = 'blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_published:
            obj.increment_view_count()
        return obj


class BlogCreateView(CreateView):
    """Создание новой записи."""
    model = BlogPost
    form_class = BlogForm
    template_name = 'blogpost_form.html'
    success_url = reverse_lazy('blogs:blogpost-list')


class BlogUpdateView(UpdateView):
    """Редактирование существующей записи."""
    model = BlogPost
    form_class = BlogForm
    template_name = 'blogpost_form.html'
    def get_success_url(self):
        return reverse_lazy('blogs:blogpost-detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Мгновенное удаление записи без подтверждения."""
    model = BlogPost

    template_name = 'blogpost_confirm_delete.html'
    success_url = reverse_lazy('blogs:blogpost-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
