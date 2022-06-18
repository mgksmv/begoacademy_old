from django.db import models

from seminars.models import Seminar


class Gallery(models.Model):
    seminar = models.ForeignKey(Seminar, verbose_name='Семинар', on_delete=models.CASCADE)
    preview_image = models.ImageField(upload_to='images/gallery_preview', verbose_name='Превью фото')
    video = models.FileField(upload_to='video/', blank=True, verbose_name='Видео')
    video_youtube = models.CharField(max_length=255, blank=True, verbose_name='Видео с Ютуб канала (ссылка)')
    url = models.SlugField(max_length=50, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return str(self.seminar)


class PostImage(models.Model):
    gallery = models.ForeignKey(Gallery, default=None, on_delete=models.CASCADE, verbose_name='Пост')
    images = models.ImageField(upload_to='images/gallery/', verbose_name='Фото')

    def __str__(self):
        return str(self.gallery.seminar.title)

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'Фото'
