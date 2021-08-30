from django import forms
from .models import Registration, Individual, Lector, ContactUs


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваши фамилия, имя, отчество'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}),
        }
        fields = '__all__'


class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваши фамилия, имя, отчество'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}),
        }
        fields = '__all__'


class LectorForm(forms.ModelForm):
    class Meta:
        model = Lector
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваши фамилия, имя, отчество'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ваш Email'}),
        }
        fields = '__all__'


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваши фамилия, имя, отчество'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ваш Email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваше сообщение', 'rows': 5}),
        }
        fields = '__all__'
