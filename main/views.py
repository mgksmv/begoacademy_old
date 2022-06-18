import urllib.request
import json
from django.views.generic import ListView, FormView
from django.shortcuts import render
from django.db.models import Prefetch
from django.contrib import messages

from config.settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key, TO_EMAIL
from seminars.models import Seminar, Category
from lectors.models import Lector
from .forms import ContactUsForm
from .tasks import send_mail_task


class HomeListView(ListView):
    model = Seminar
    context_object_name = 'seminars'
    template_name = 'main/home.html'

    def get_queryset(self):
        return Seminar.objects.filter(is_finished=False, is_published=True) \
                   .select_related('organizer', 'place') \
                   .prefetch_related(
            Prefetch('category', queryset=Category.objects.all()),
            Prefetch('lector', queryset=Lector.objects.all().only('name', 'photo')),
        ) \
                   .defer(
            'content', 'hours', 'price', 'additional_info', 'place__embed_code', 'lector__bio',
            'lector__description', 'lector__photo',
        ) \
                   .order_by('date')[:3]


class ContactsFormView(FormView):
    form_class = ContactUsForm
    template_name = 'main/contacts.html'

    def get_success_url(self):
        return self.request.path_info

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        user_email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        send_mail_task.delay(
            'Обратная связь',
            f'Имя: {name}\nEmail: {user_email}\nСообщение: {message}',
            TO_EMAIL
        )

        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        if result['success']:
            form.save()
            messages.success(self.request, 'Мы получили ваше сообщение. Постараемся ответить Вам как можно скорее!')
        else:
            messages.error(self.request, 'Подтвердите, что Вы не робот.')

        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


def error_404(request, exception):
    return render(request, 'main/not_found_page.html')
