from django.db import models


class BlogPost(models.Model):
    """Модель для хранения записей блога."""

    title = models.CharField(
        verbose_name="Заголовок",
        max_length=200,
        help_text="Введите название статьи"
    )

    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Основной текст статьи"
    )

    image = models.ImageField(
        verbose_name="Превью (изображение)",
        upload_to='blog_previews/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True
    )

    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=False,
        help_text="Отметьте, если статья должна быть видна на сайте"
    )

    view_count = models.PositiveIntegerField(
        verbose_name="Количество просмотров",
        default=0,
        editable=False,
        db_index=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"

    def __str__(self):
        return self.title

    def increment_view_count(self):
        """Метод для безопасного увеличения счетчика просмотров."""
        self.view_count += 1
        self.save(update_fields=['view_count'])

