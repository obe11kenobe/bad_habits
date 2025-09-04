from calendar import mdays

from django.db import models
from django.conf import settings


class Habit(models.Model):
    # Тип цели: бинарная (да/нет) или числовая (например, 30 страниц)
    class GoalType(models.TextChoices):
        BINARY = 'binary', 'Выполнено / Не выполнено'
        NUMERIC = 'numeric', 'Количество (например, страниц)'

    # Частота: как часто нужно выполнять привычку

    class Frequency(models.TextChoices):
        DAILY = 'daily', 'Каждый день'
        WEEKLY = 'weekly', 'Каждую неделю'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,       # к какому пользователю привязана привычка
        on_delete=models.CASCADE,       # если удалить пользователя → удалятся его привычки
        related_name='habits'           # чтобы можно было писать user.habits.all()
    )

    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )

    description = models.TextField(
        blank=True,                     # можно оставить пустым
        verbose_name='Описание'
    )

    goal_type = models.CharField(
        max_length=10,
        verbose_name='Тип цели',
        choices=GoalType.choices,       # ограничиваем выбор: binary или numeric
        default=GoalType.BINARY         # по умолчанию "бинарная"
    )

    goal_value = models.PositiveSmallIntegerField(
        null=True,                      # в базе может быть пусто
        blank=True,                     # в форме можно оставить пустым
        verbose_name='Цель (число)'
    )

    frequency = models.CharField(
        max_length=10,
        choices=Frequency.choices,
        default=Frequency.DAILY,
        verbose_name='Частота'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,              # автоматически ставится дата создания
        verbose_name='Когда создана'
    )

    class Meta:
        ordering = ['title', '-created_at']  # сортировка по названию, потом по дате
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return self.title

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, # к какой привычке относится запись
                              on_delete=models.CASCADE,  # если удалить привычку → удаляются все её записи
                              related_name='logs') # доступно через habit.logs.all()
    completed_at = models.DateField(verbose_name='Дата выполнения')

    value = models.PositiveSmallIntegerField(
        null=True, # если бинарная привычка → можно оставить пустым
        blank=True,
        verbose_name='Значение'
    )

    class Meta:
        unique_together = ('habit', 'completed_at')  # нельзя 2 раза отметить один день
        ordering = ['-completed_at', ]
        verbose_name = 'Запись выполнения'
        verbose_name_plural = 'Записи выполнения'

    def __str__(self):
        return f'{self.habit.title} - {self.completed_at}'