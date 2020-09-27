from django.db import models

from helpers.transliterator import transliterate


class Report(models.Model):
    is_active = models.BooleanField(verbose_name='Статус', default=True)
    title = models.CharField(max_length=120, verbose_name='Заголовок', unique=True,
                             help_text='Название отображается на сайте и используется для формироватия url')
    slug = models.SlugField(max_length=120, unique=True)
    script = models.TextField(verbose_name='SQL скрипт', unique=True,
                              help_text='В скрипте нужно поставить {} вместо всех условий, на его место будет подставле'
                                        'нны условия полученные от пользователя<br>Пример:<br>SELECT * FROM event <span'
                                        ' style="color: red">WHERE id = 123 AND name LIKE (\'володя\')</span> ORDER BY '
                                        'id DESC<br>SELECT * FROM event {} ORDER BY id DESC')
    comment = models.TextField(verbose_name='Коментарии', default='',
                               help_text='Коментарий отображается при наведении на название отчета')

    def save(self, *args, **kwargs):
        self.slug = transliterate(self.title).replace(' ', '-')
        super(Report, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'


class ReportParam(models.Model):
    TEXT_TYPE = 'text'
    INT_TYPE = 'int'
    DATE_TYPE = 'date'
    DATETIME_TYPE = 'datetime'
    TYPE_CHOICES = (
        (TEXT_TYPE, 'Текст'),
        (INT_TYPE, 'Число(а)'),
        (DATE_TYPE, 'Дата'),
        (DATETIME_TYPE, 'Дата и время'),
    )
    is_mandatory = models.BooleanField(verbose_name='Обязательный?')
    title = models.CharField(max_length=120, verbose_name='Заголовок',
                             help_text='Заголовок отображается на сайте и используется для формироватия url')
    slug = models.SlugField(max_length=120)
    sql_condition = models.CharField(max_length=120, verbose_name='SQL параметр',
                                     help_text='Нужно написать ключ устовия, а значение заменить на {}<br>{} будет заме'
                                               'нен на значение полученное от пользователя<br>Из примера <br><span styl'
                                               'e="color: red">id = {}</span> и <span style="color: red">LIKE (\'{}\')<'
                                               '/span><br>WHERE и AND будут подставленны автоматически по мере необходи'
                                               'мости')
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    input_type = models.CharField(max_length=8, verbose_name='Тип', choices=TYPE_CHOICES,
                                  help_text='От типа будет зависить тип формы на сайте')

    def save(self, *args, **kwargs):
        self.slug = transliterate(self.title).replace(' ', '-').lower()
        super(ReportParam, self).save()

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'


class Organization(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организацию'
        verbose_name_plural = 'Организации'


class Agent(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название', unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Агента'
        verbose_name_plural = 'Агенты'


class Organizer(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название', unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организатора'
        verbose_name_plural = 'Организаторы'
