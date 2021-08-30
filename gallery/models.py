from django.db import models

from seminars.models import Seminar
from django.template.defaultfilters import slugify
from unidecode import unidecode


class Gallery(models.Model):
    seminar = models.ForeignKey(Seminar, verbose_name='Семинар', on_delete=models.CASCADE)
    preview_image = models.ImageField(upload_to='images/gallery_preview', verbose_name='Превью фото')
    video = models.FileField(upload_to='video/', blank=True, verbose_name='Видео')
    video_youtube = models.CharField(max_length=255, blank=True, verbose_name='Видео с Ютуб канала (ссылка)')
    url = models.SlugField(max_length=50, unique=True, verbose_name='URL')

    # number = [1]

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'Галерея'

    # def save(self, *args, **kwargs):
    #     lectors_list = []
    #     for lector in self.seminar.lector.all():
    #         lectors_list.append(lector.name)
    #     lectors = ' '.join(lectors_list)
    #
    #     auto_slug = slugify(unidecode(str(f'{self.seminar.title}-{lectors}-{self.seminar.date.year}')))
    #     self.url = auto_slug
    #     if Gallery.objects.filter(url=auto_slug):
    #         self.number.append(self.number[-1] + 1)
    #         new_auto_slug = slugify(
    #             unidecode(str(f'{self.seminar.title}-{lectors}-{self.seminar.date.year}-{self.number[-1]}'))
    #         )
    #         self.url = new_auto_slug
    #     return super(Gallery, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.seminar)


class PostImage(models.Model):
    gallery = models.ForeignKey(Gallery, default=None, on_delete=models.CASCADE, verbose_name='Пост')
    images = models.ImageField(upload_to=f'images/gallery/', verbose_name='Фото')

    def __str__(self):
        return f'{self.gallery.seminar.title}'

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'Фото'
