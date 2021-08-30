from django.db import models
from ckeditor.fields import RichTextField


class Lector(models.Model):
    name = models.CharField(max_length=200, verbose_name="ФИО")
    bio = models.CharField(max_length=200, verbose_name='Краткое описание')
    description = RichTextField(verbose_name='Биография')
    photo = models.ImageField(upload_to='images/lector', verbose_name='Фото', help_text='Для страницы семинара')

    class Meta:
        verbose_name = 'лектор'
        verbose_name_plural = 'Список лекторов'
        ordering = ['name']

    def __str__(self):
        return self.name


class LectorProfile(models.Model):
    lector = models.ForeignKey(Lector, verbose_name='Лектор', on_delete=models.CASCADE)
    photo_1 = models.ImageField(upload_to="images/lector", verbose_name='Фото 1',
                                help_text='Для страницы лекторов, круглое')
    photo_2 = models.ImageField(upload_to="images/lector", verbose_name='Фото 2',
                                help_text='Для страницы лектора, прямоугольное')
    instagram = models.URLField(max_length=200, blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    vk = models.URLField(max_length=200, blank=True, verbose_name='ВКонтакте')
    url = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    is_published = models.BooleanField(verbose_name='Опубликовать', default=True, help_text='Если снять галочку, то страница лектора станет черновиком и не будет отображаться на сайте.')

    class Meta:
        verbose_name = 'профиль лектора'
        verbose_name_plural = 'Лекторы (профили)'

    def __str__(self):
        return f'{self.lector} (профиль)'
