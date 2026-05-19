from django.db import models
from django.contrib.auth.models import User

# Модель профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=20)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.full_name


# Модель заявки на обучение
class Application(models.Model):
    class CourseType(models.TextChoices):
        QUALIFICATION = 'qualification', 'Повышение квалификации'
        RETRAINING = 'retraining', 'Переподготовка'
        OCCUPATIONAL_SAFETY = 'safety', 'Охрана труда'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличные'
        CARD = 'card', 'Банковская карта'

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'Идёт обучение'
        COMPLETED = 'completed', 'Обучение завершено'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    course_type = models.CharField('Тип курса', max_length=50, choices=CourseType.choices)
    start_date = models.DateField('Дата начала обучения')
    payment_method = models.CharField('Способ оплаты', max_length=50, choices=PaymentMethod.choices)
    status = models.CharField('Статус', max_length=50, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_course_type_display()} - {self.user.username}'
