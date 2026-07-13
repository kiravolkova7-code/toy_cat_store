from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=100, verbose_name='username', )
    email = models.EmailField(unique=True, verbose_name='email', help_text='Введите адрес электронной почты' )

    avatar = models.ImageField(upload_to='users/avatar/', verbose_name = 'Аватар', blank=True, null=True, help_text='Загрузите фото')
    phone = models.CharField(max_length=20, verbose_name = 'Номер телефона', blank=True, null=True, help_text='Введите номер телефона')
    country = models.CharField(max_length=20,  verbose_name = 'Страна', blank=True, null=True, help_text='Укажите страну')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

