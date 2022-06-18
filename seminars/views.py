import urllib.request
import json
from datetime import datetime
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.contrib import messages

from config.settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key, TO_EMAIL
from main.forms import RegistrationForm
from main.tasks import send_mail_task
from lectors.models import Lector
from gallery.models import Gallery, PostImage
from .models import Seminar, Category


class SeminarsListView(ListView):
    model = Seminar
    paginate_by = 10
    template_name = 'seminars/all_seminars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_path = self.request.path
        if current_path.split('/')[1] == 'past-seminars':
            is_finished = True
        else:
            is_finished = False

        category_url = self.kwargs.get('category_url')

        seminars = Seminar.objects.order_by('date') \
            .select_related('organizer', 'place') \
            .prefetch_related(
                Prefetch('category', queryset=Category.objects.all()),
                Prefetch('lector', queryset=Lector.objects.all().only('name', 'photo')),
            ) \
            .defer('content', 'place__embed_code')

        if not category_url:
            seminars = seminars.filter(is_finished=is_finished, is_published=True)
            active_category = 1
        else:
            categories = get_object_or_404(Category, url=category_url)
            seminars = seminars.filter(category=categories, is_finished=is_finished, is_published=True)
            active_category = Category.objects.get(url=category_url)

        seminar_count = seminars.count()

        context['object_list'] = seminars
        context['seminar_count'] = seminar_count
        context['active_category'] = active_category

        return context


class SeminarDetailView(FormMixin, DetailView):
    model = Seminar
    form_class = RegistrationForm
    slug_field = 'url'
    slug_url_kwarg = 'url'
    template_name = 'seminars/seminar_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gallery = Gallery.objects.filter(seminar=self.object)
        photo_list = PostImage.objects.filter(gallery__seminar=self.object)

        today = datetime.today().date()
        seminar_date = self.object.date
        remaining = seminar_date - today

        context['gallery'] = gallery
        context['photo_list'] = photo_list
        context['remaining'] = remaining

        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['seminar_name'].initial = self.object.title
        form.fields['seminar_name'].widget.attrs['readonly'] = True
        return form

    def get_success_url(self):
        return self.request.path_info

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        seminar_name = form.cleaned_data.get('seminar_name')
        name = form.cleaned_data.get('name')
        phone_number = form.cleaned_data.get('phone_number')

        send_mail_task.delay(
            'Запись на семинар',
            f'Семинар: {seminar_name}\nИмя: {name}\nТелефон: {phone_number}',
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
            messages.success(self.request, 'Ваша заявка принята! Мы вам перезвоним для уточнения деталей.')
        else:
            messages.error(self.request, 'Подтвердите, что Вы не робот.')

        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return super().form_invalid(form)
