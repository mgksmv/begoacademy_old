from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
from decouple import config
import urllib.request
import json

from .models import Seminar, Category, NewOrganizer, OrganizerNumbers, OrganizerWhatsAppNumbers
from gallery.models import Gallery, PostImage
from main.forms import RegistrationForm
from config.settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key

EMAIL_FROM = config('EMAIL_FROM')
EMAIL_TO = config('EMAIL_TO')


def all_seminars(request, category_url=None):
    seminars = None
    categories = None
    active_category = None

    if category_url == None:
        seminars = Seminar.objects.filter(is_finished=False, is_published=True).order_by('date')
        seminar_count = seminars.count()
        active_category = 1
    else:
        categories = get_object_or_404(Category, url=category_url)
        seminars = Seminar.objects.filter(category=categories, is_finished=False, is_published=True).order_by('date')
        seminar_count = seminars.count()
        active_category = Category.objects.get(url=category_url)

    paginator = Paginator(seminars, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    context = {
        'seminars': page,
        'active_category': active_category,
        'seminar_count': seminar_count,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }

    return render(request, 'seminars/all_seminars.html', context)


def seminar_detail(request, seminar_url):
    seminar = get_object_or_404(Seminar, url=seminar_url)
    organizers = NewOrganizer.objects.all()
    organizer_numbers = OrganizerNumbers.objects.all()
    organizer_whatsapp_numbers = OrganizerWhatsAppNumbers.objects.all()
    
    gallery = Gallery.objects.filter(seminar=seminar)
    photo_list = PostImage.objects.filter(gallery__seminar=seminar)

    form = RegistrationForm()

    name = None
    invalid_captcha = False
    submitted = False
    
    today = datetime.today().date()
    seminar_date = seminar.date

    remaining = seminar_date - today

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form.fields['seminar_name'].initial = seminar.title

        seminar_name = request.POST['seminar_name']
        name = request.POST['name']
        phone_number = request.POST['phone_number']

        send_mail(
            'Запись на семинар',
            f'Семинар: {seminar_name}\nИмя: {name}\nТелефон: {phone_number}',
            EMAIL_FROM,
            [EMAIL_TO]
        )
            
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': secret_key,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
    
            if result['success']:
                form.save()
                return HttpResponseRedirect(f'{request.path_info}?submitted=True')
            else:
                messages.success(request, 'Подтвердите, что Вы не робот.')
                invalid_captcha = True

    else:
        form = RegistrationForm()
        form.fields['seminar_name'].initial = seminar.title
        form.fields['seminar_name'].widget.attrs['readonly'] = True
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'seminar': seminar,
        'organizers': organizers,
        'organizer_numbers': organizer_numbers,
        'organizer_whatsapp_numbers': organizer_whatsapp_numbers,
        'form': form,
        'message_name': name,
        'invalid_captcha': invalid_captcha,
        'submitted': submitted,
        'gallery': gallery,
        'photo_list': photo_list,
        'remaining': remaining,
    }

    return render(request, 'seminars/seminar_detail.html', context)


def past_seminars(request, category_url=None):
    seminars = None
    categories = None
    active_category = None

    if category_url == None:
        seminars = Seminar.objects.filter(is_finished=True, is_published=True)
        seminar_count = seminars.count()
        active_category = 1
    else:
        categories = get_object_or_404(Category, url=category_url)
        seminars = Seminar.objects.filter(category=categories, is_finished=True, is_published=True)
        seminar_count = seminars.count()
        active_category = Category.objects.get(url=category_url)

    paginator = Paginator(seminars, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    context = {
        'seminars': page,
        'active_category': active_category,
        'seminar_count': seminar_count,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }

    return render(request, 'seminars/past_seminars.html', context)
