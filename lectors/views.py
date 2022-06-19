import urllib.request
import json
from decouple import config
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from seminars.models import Seminar
from main.forms import LectorForm
from main.tasks import send_mail_task
from config.settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key, TO_EMAIL
from .models import LectorProfile

EMAIL_FROM = config('EMAIL_FROM')
EMAIL_TO = config('EMAIL_TO')


class LectorsListView(ListView):
    model = LectorProfile
    paginate_by = 10
    template_name = 'lectors/all_lectors.html'

    def get_queryset(self):
        return LectorProfile.objects.filter(is_published=True).select_related('lector') \
            .defer('photo_2', 'instagram', 'facebook', 'vk', 'lector__description', 'lector__photo')


class LectorDetailView(FormMixin, DetailView):
    model = LectorProfile
    form_class = LectorForm
    slug_field = 'url'
    slug_url_kwarg = 'url'
    template_name = 'lectors/lector_page.html'

    def get_queryset(self):
        return LectorProfile.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        upcoming_seminars = Seminar.objects.filter(is_finished=False, lector=self.object.lector).order_by('date')
        upcoming_seminars_count = upcoming_seminars.count()
        context['upcoming_seminars'] = upcoming_seminars
        context['upcoming_seminars_count'] = upcoming_seminars_count
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path_info

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['lector_name'].initial = self.object.lector.name
        form.fields['lector_name'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        lector_name = form.cleaned_data.get('lector_name')
        name = form.cleaned_data.get('name')
        phone_number = form.cleaned_data.get('phone_number')
        user_email = form.cleaned_data.get('email')

        send_mail_task.delay(
            'Заявка на семинар лектора',
            f'Лектор: {lector_name}\nИмя: {name}\nТелефон: {phone_number}\nEmail: {user_email}',
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
            messages.success(self.request, 'Заявка принята! Мы Вам сообщим, когда запланируем семинар с данным лектором.')
        else:
            messages.error(self.request, 'Подтвердите, что Вы не робот.')

        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return super().form_invalid(form)
