from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from decouple import config
import urllib.request
import json

from .models import LectorProfile
from seminars.models import Seminar
from main.forms import LectorForm
from config.settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key

EMAIL_FROM = config('EMAIL_FROM')
EMAIL_TO = config('EMAIL_TO')


def lectors(request):
    all_lectors = LectorProfile.objects.filter(is_published=True)

    paginator = Paginator(all_lectors, 10)
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
        'lectors': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }

    return render(request, 'lectors/all_lectors.html', context)


def lector_page(request, lector_url):
    try:
        lector = LectorProfile.objects.get(url=lector_url)

        upcoming_seminars = Seminar.objects.filter(is_finished=False).order_by('date')
        upcoming_seminars_count = Seminar.objects.filter(is_finished=False, lector=lector.lector).order_by('date').count()
        
    
        lector_seminar_count = upcoming_seminars.count()
    
        form = LectorForm()
        name = None
        invalid_captcha = False
        submitted = False
    
        if request.method == 'POST':
            form = LectorForm(request.POST)
            form.fields['lector_name'].initial = lector.lector.name
    
            lector_name = request.POST['lector_name']
            name = request.POST['name']
            phone_number = request.POST['phone_number']
            user_email = request.POST['email']
    
            send_mail(
                'Заявка на семинар лектора',
                f'Лектор: {lector_name}\nИмя: {name}\nТелефон: {phone_number}\nEmail: {user_email}',
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
            form = LectorForm()
            form.fields['lector_name'].initial = lector.lector.name
            form.fields['lector_name'].widget.attrs['readonly'] = True
            if 'submitted' in request.GET:
                submitted = True
    
        context = {
            'lector': lector,
            'upcoming_seminars': upcoming_seminars,
            'form': form,
            'invalid_captcha': invalid_captcha,
            'submitted': submitted,
            'lector_seminar_count': lector_seminar_count,
            'upcoming_seminars_count': upcoming_seminars_count,
        }
    except LectorProfile.DoesNotExist:
        raise Http404()

    return render(request, 'lectors/lector_page.html', context)
