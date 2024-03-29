from datetime import date

from decouple import config
from celery import shared_task
from django.core.mail import send_mail
from django.apps import apps

EMAIL_HOST_USER = config('EMAIL_HOST_USER')


@shared_task
def send_mail_task(subject, message, to_email=None):
    if not to_email:
        to_email = EMAIL_HOST_USER
    return send_mail(subject, message, EMAIL_HOST_USER, [to_email], fail_silently=False)


@shared_task
def move_seminar_to_past_seminars():
    now = date.today()
    all_seminars = apps.get_model(app_label='seminars', model_name='Seminar')
    for seminar in all_seminars.objects.filter(is_finished=False):
        if now >= seminar.date and not seminar.is_finished:
            seminar.is_finished = True
            seminar.save()
