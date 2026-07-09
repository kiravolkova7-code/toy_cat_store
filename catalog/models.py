from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование", help_text="Введите наименование продукта")
    text = models.TextField(max_length=200, verbose_name="Описание", help_text="Введите описание продукта")
    image = models.ImageField(
        upload_to="products/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Укажите категорию продукта",
        blank=True,
        null=True,
    )
    price = models.FloatField(verbose_name="Цена", help_text="Укажите цену продукта")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ["name", "category", "price"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория", help_text="Введите наименование категории")
    text = models.TextField(
        max_length=300, blank=True, null=True, verbose_name="Описание", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
