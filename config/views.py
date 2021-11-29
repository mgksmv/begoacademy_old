from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
import urllib.request
import json

from seminars.models import Seminar
from main.forms import ContactUsForm
from .settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key

email = 'lonfyo@gmail.com'


class HomeListView(ListView):
    queryset = Seminar.objects.filter(is_finished=False, is_published=True).order_by('date')[:3]
    context_object_name = 'seminars'
    template_name = 'main/home.html'


def contacts(request):
    invalid_captcha = False
    submitted = False

    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        name = request.POST['name']
        user_email = request.POST['email']
        message = request.POST['message']

        send_mail(
            'Обратная связь',
            f'Имя: {name}\nEmail: {user_email}\nСообщение: {message}',
            email,
            ['begoacademy@gmail.com']
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
        form = ContactUsForm()
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form': form,
        'invalid_captcha': invalid_captcha,
        'submitted': submitted,
    }

    return render(request, 'main/contacts.html', context)
    

def error_404(request, exception):
    return render(request, 'main/not_found_page.html')
