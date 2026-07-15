from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" с нужными правами'

    def handle(self, *args, **options):
        can_unpublish = Permission.objects.get(codename='can_unpublish_product')
        delete_product = Permission.objects.get(codename='delete_product', content_type__app_label='catalog')

        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа создана'))

        group.permissions.set([can_unpublish, delete_product])
        group.save()

        self.stdout.write(
            self.style.SUCCESS(f'Группе назначены права: {group.permissions.values_list("name", flat=True)}'))
