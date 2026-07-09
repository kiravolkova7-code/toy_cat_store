from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product


class Command(BaseCommand):
    help = 'Очищает таблицу продуктов и загружает данные из фикстуры'

    def handle(self, *args, **kwargs):
        self.stdout.write("Удаление существующих продуктов...")
        Product.objects.all().delete()

        self.stdout.write("Загрузка данных из products_fixture.json...")
        try:
            call_command('loaddata', 'products_fixture.json')
            self.stdout.write(self.style.SUCCESS('Продукты успешно загружены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке фикстуры: {e}'))