from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from decouple import config
import urllib.request
import json

from .models import Individual
from main.forms import IndividualForm
from config.settings import GOOGLE_RECAPTCHA_SECRET_KEY as secret_key

EMAIL_FROM = config('EMAIL_FROM')
EMAIL_TO = config('EMAIL_TO')


class ForDentistsListView(ListView):
    queryset = Individual.objects.filter(category='Для стоматологов', is_published=True)
    context_object_name = 'dentist_individual'
    template_name = 'individual/for_dentists.html'
    
   
class ForTechListView(ListView):
    queryset = Individual.objects.filter(category='Для техников', is_published=True)
    context_object_name = 'tech_individual'
    template_name = 'individual/for_tech.html'
    

class ForClinicsListView(ListView):
    queryset = Individual.objects.filter(category='Для клиник', is_published=True)
    context_object_name = 'clinic_individual'
    template_name = 'individual/for_clinics.html'


def individual_page(request, individual_url):
    individual = get_object_or_404(Individual, url=individual_url)

    form = IndividualForm()

    name = None
    invalid_captcha = False
    submitted = False

    if request.method == 'POST':
        form = IndividualForm(request.POST)
        if individual.doctor:
            form.fields['individual_name'].initial = f'{individual.title} / {individual.doctor}'
        else:
            form.fields['individual_name'].initial = individual.title

        individual_name = request.POST['individual_name']
        name = request.POST['name']
        phone_number = request.POST['phone_number']

        send_mail(
            'Индивидуальный курс',
            f'Курс: {individual_name}\nИмя: {name}\nТелефон: {phone_number}',
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
        form = IndividualForm()
        if individual.doctor:
            form.fields['individual_name'].initial = f'{individual.title} / {individual.doctor}'
        else:
            form.fields['individual_name'].initial = individual.title
        form.fields['individual_name'].widget.attrs['readonly'] = True
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'individual': individual,
        'form': form,
        'message_name': name,
        'invalid_captcha': invalid_captcha,
        'submitted': submitted,
    }

    return render(request, 'individual/individual_page.html', context)
