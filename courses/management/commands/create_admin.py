from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Profile


class Command(BaseCommand):
    help = 'Создание администратора для портала'

    def handle(self, *args, **options):
        username = 'Admin26'
        password = 'Demo20'
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует'))
            return
        user = User.objects.create_superuser(
            username=username,
            password=password,
            email='admin@uchus.ru',
        )
        Profile.objects.create(
            user=user,
            full_name='Администратор Системы',
            phone='+7 (123) 000-00-00',
        )
        self.stdout.write(self.style.SUCCESS(f'Администратор {username} успешно создан'))
