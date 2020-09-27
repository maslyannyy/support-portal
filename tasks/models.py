from django.db import models

from tasks.services.crons import write_task


class Task(models.Model):
    _TIME_CHOICES = [(i, i) for i in range(0, 60, 10)]
    is_active = models.BooleanField(default=True)
    script = models.CharField(max_length=120, verbose_name='Название')
    sleep = models.IntegerField(verbose_name='Отсрочка', choices=_TIME_CHOICES)
    param = models.CharField(max_length=120, verbose_name='Параметры запуска')

    def save(self, *args, **kwargs):
        write_task(**self.__dict__)
        super(Task, self).save()

    def __str__(self):
        return self.script

    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'


class Dictionary(models.Model):
    author = models.CharField(max_length=120, verbose_name='Автор', default='')
    message = models.TextField(verbose_name='Сообщение')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Цитату'
        verbose_name_plural = 'Цитаты'


class Feed(models.Model):
    is_active = models.BooleanField(verbose_name='Статус', default=True)
    url = models.TextField(verbose_name='URL', unique=True)
    is_multi = models.BooleanField(verbose_name='Проверять на всех доменах?', default=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Фид'
        verbose_name_plural = 'Фиды'


class Domain(models.Model):
    is_active = models.BooleanField(verbose_name='Статус', default=True)
    url = models.TextField(verbose_name='URL', unique=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'
