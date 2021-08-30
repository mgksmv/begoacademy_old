from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode
from ckeditor.fields import RichTextField

from lectors.models import Lector


class Individual(models.Model):
    categories = (
        ('Для стоматологов', 'Для стоматологов'),
        ('Для техников', 'Для техников'),
        ('Для клиник', 'Для клиник'),
    )

    title = models.CharField(max_length=200, verbose_name='Тема')
    category = models.CharField(max_length=50, default="IndLesItem", choices=categories, verbose_name='Категория')
    doctor = models.ForeignKey(Lector, blank=True, null=True, verbose_name='Доктор', on_delete=models.CASCADE)
    content = RichTextField(verbose_name='Программа курса')
    photo = models.ImageField(upload_to="images/thumbnails", verbose_name='Фото')
    url = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    is_published = models.BooleanField(verbose_name='Опубликовать', default=True, help_text='Если снять галочку, то страница обучения станет черновиком и не будет отображаться на сайте.')

    class Meta:
        verbose_name = 'индивидуальное обучение'
        verbose_name_plural = 'Индивидуальное обучение'

    # def save(self, *args, **kwargs):
    #     self.url = slugify(unidecode(str(self.title)))
    #     return super(Individual, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
