from django.db import models, IntegrityError
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode
from ckeditor.fields import RichTextField

from lectors.models import Lector


class NewOrganizer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    logo = models.ImageField(upload_to='images/organizer_logo', blank=True, verbose_name='Логотип организации')
    url = models.SlugField(max_length=50, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'организатор'
        verbose_name_plural = 'Список организаторов'

    def __str__(self):
        return self.name


class OrganizerNumbers(models.Model):
    post = models.ForeignKey(NewOrganizer, default=None, on_delete=models.CASCADE, verbose_name='Пост')
    number = models.CharField(max_length=200, verbose_name='Номер')

    class Meta:
        verbose_name = 'номер телефона'
        verbose_name_plural = '📞 Номера телефонов для звонков'

    def __str__(self):
        return self.number


class OrganizerWhatsAppNumbers(models.Model):
    post = models.ForeignKey(NewOrganizer, default=None, on_delete=models.CASCADE, verbose_name='Пост')
    number = models.CharField(max_length=200, verbose_name='Номер WhatsApp')

    class Meta:
        verbose_name = 'номер телефона WhatsApp'
        verbose_name_plural = '💬 Номера телефонов для WhatsApp'

    def __str__(self):
        return self.number


class Category(models.Model):
    category_name = models.CharField(max_length=200, verbose_name='Категория')
    icon = models.ImageField(upload_to='images/icons', blank=True, verbose_name='Иконка')
    url = models.SlugField(max_length=50, unique=True, verbose_name='URL')

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('seminar_by_category', args=[self.url])

    def get_past_url(self):
        return reverse('past_seminar_by_category', args=[self.url])

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Address(models.Model):
    address = models.CharField(max_length=250, verbose_name='Город и улица')
    embed_code = models.TextField(blank=True, verbose_name='Код', help_text='Код с Google Карты')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса'


class Seminar(models.Model):
    title = models.CharField(max_length=200, verbose_name='Тема')
    content = RichTextField(verbose_name='Программа курса')
    category = models.ManyToManyField(Category, blank=True, verbose_name='Категория')
    lector = models.ManyToManyField(Lector, verbose_name='Лектор')
    reserve_photo = models.ImageField(upload_to='images/seminar_reserve', verbose_name='Резервное фото', blank=True,
                                      help_text='Фото для отображения на странице семинаров. На случай, если лекторов несколько.')
    date = models.DateField(verbose_name='Дата проведения')
    date_info = models.CharField(max_length=200, blank=True, verbose_name='Дата для отображения',
                                 help_text='Именно это будет отображаться на сайте.')
    hours = models.CharField(max_length=200, blank=True, verbose_name='Время начала/конца')
    type = models.CharField(max_length=200, verbose_name='Тип курса')
    organizer = models.ForeignKey(NewOrganizer, verbose_name='Организатор', on_delete=models.CASCADE, blank=True,
                                  null=True)
    place = models.ForeignKey(Address, verbose_name='Место проведения', on_delete=models.CASCADE)
    price = models.CharField(max_length=200, blank=True, verbose_name='Цена')
    participants = models.CharField(max_length=200, blank=True, verbose_name='Количество участников')
    additional_info = models.CharField(max_length=200, blank=True, verbose_name='Дополнительная инфа')
    url = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    is_only_for_bego = models.BooleanField(verbose_name='Только для коллектива BEGO', help_text='Отметьте, если семинар проводится только для коллектива BEGO.')
    is_finished = models.BooleanField(verbose_name='Завершён', help_text='Отметьте, если семинар завершён.')
    is_published = models.BooleanField(verbose_name='Опубликовать', default=True, help_text='Если снять галочку, то страница семинара станет черновиком и не будет отображаться на сайте.')

    class Meta:
        verbose_name = 'семинар'
        verbose_name_plural = 'Семинары'
        ordering = ['-date']

    def get_url(self):
        return reverse('seminar_detail', args=[self.url])

    def __str__(self):
        lectors_list = []
        for lector in self.lector.all():
            lectors_list.append(lector.name)
        lectors = ', '.join(lectors_list)

        return f'{lectors} | {self.date}'


class Live(models.Model):
    video_youtube = models.CharField(max_length=200, blank=True, verbose_name='Видео с Ютуб канала (ссылка)')
    title = models.CharField(max_length=200, blank=True, verbose_name='Название')
    url = models.SlugField(max_length=50, verbose_name='URL')
    is_live = models.BooleanField(verbose_name='Сейчас в эфире')

    class Meta:
        verbose_name = 'прямой эфир'
        verbose_name_plural = 'Прямой эфир'

    def __str__(self):
        return 'Прямой эфир'
