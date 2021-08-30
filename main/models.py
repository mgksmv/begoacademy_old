from django.db import models


class Registration(models.Model):
    seminar_name = models.CharField(max_length=200, verbose_name='Название семинара')
    name = models.CharField(max_length=200, verbose_name='ФИО')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'Регистрация на семинар'

    def __str__(self):
        return self.name


class Individual(models.Model):
    individual_name = models.CharField(max_length=200, verbose_name='Название')
    name = models.CharField(max_length=200, verbose_name='ФИО')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'Индивидуальное обучение'

    def __str__(self):
        return self.name


class Lector(models.Model):
    lector_name = models.CharField(max_length=200, verbose_name='Лектор')
    name = models.CharField(max_length=200, verbose_name='ФИО')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    email = models.EmailField(max_length=200, blank=True, verbose_name='Email (не обязательно)')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'Заявки на семинар'

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    name = models.CharField(max_length=200, verbose_name='ФИО')
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=500, verbose_name='Сообщение')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.name
