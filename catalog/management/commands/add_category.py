from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category


class Command(BaseCommand):
    help = 'Очищает таблицу категорий и загружает данные из фикстуры'

    def handle(self, *args, **kwargs):
        self.stdout.write("Удаление существующих категорий...")
        Category.objects.all().delete()

        self.stdout.write("Загрузка данных из category_fixture.json...")
        try:
            call_command('loaddata', 'category_fixture.json')
            self.stdout.write(self.style.SUCCESS('Категории успешно загружены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке фикстуры: {e}'))