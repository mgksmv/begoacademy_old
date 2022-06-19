import urllib.request
import json
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.http import Http404

from .models import Individual
from main.forms import IndividualForm
from main.tasks import send_mail_task
from config.settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key, TO_EMAIL


class ForDentistsListView(ListView):
    model = Individual
    context_object_name = 'dentist_individual'
    template_name = 'individual/for_dentists.html'

    def get_queryset(self):
        return Individual.objects.filter(category='Для стоматологов', is_published=True) \
            .select_related('doctor') \
            .defer('content', 'doctor__bio', 'doctor__description', 'doctor__description', 'doctor__photo')


class ForTechListView(ListView):
    model = Individual
    context_object_name = 'tech_individual'
    template_name = 'individual/for_tech.html'

    def get_queryset(self):
        return Individual.objects.filter(category='Для техников', is_published=True) \
            .select_related('doctor') \
            .defer('content', 'doctor__bio', 'doctor__description', 'doctor__description', 'doctor__photo')


class ForClinicsListView(ListView):
    model = Individual
    context_object_name = 'clinic_individual'
    template_name = 'individual/for_clinics.html'

    def get_queryset(self):
        return Individual.objects.filter(category='Для клиник', is_published=True) \
            .select_related('doctor') \
            .defer('content', 'doctor__bio', 'doctor__description', 'doctor__description', 'doctor__photo')


class IndividualDetailView(FormMixin, DetailView):
    model = Individual
    form_class = IndividualForm
    slug_field = 'url'
    slug_url_kwarg = 'url'
    template_name = 'individual/individual_page.html'

    def get_queryset(self):
        return Individual.objects.filter(is_published=True)

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
        form.fields['individual_name'].widget.attrs['readonly'] = True
        if self.object.doctor:
            form.fields['individual_name'].initial = f'{self.object.title} / {self.object.doctor}'
        else:
            form.fields['individual_name'].initial = self.object.title
        return form

    def form_valid(self, form):
        individual_name = form.cleaned_data.get('individual_name')
        name = form.cleaned_data.get('name')
        phone_number = form.cleaned_data.get('phone_number')

        send_mail_task.delay(
            'Индивидуальный курс',
            f'Курс: {individual_name}\nИмя: {name}\nТелефон: {phone_number}',
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
            messages.success(self.request, 'Ваша заявка принята! Мы Вам перезвоним для уточнения деталей.')
        else:
            messages.error(self.request, 'Подтвердите, что Вы не робот.')

        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return super().form_invalid(form)
