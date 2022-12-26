from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import views
from .models import *


class AddPartnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Partner
        fields = ['name', 'logo', 'description', 'iin', 'partner_person', 'partner_tel', 'partner_email',
                  'time_start_working', 'time_expires', 'is_working']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'time_start_working': forms.SelectDateWidget(years=list(range(1980, 2030))),
            'time_expires': forms.SelectDateWidget(years=list(range(1980, 2030))),

        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    partner = forms.ModelChoiceField(label='Партнер', queryset=Partner.objects.all())
    tel_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-input'}))
    is_costumer = forms.BooleanField(label='Является покупателем', widget=forms.CheckboxInput)

    class Meta:
        model = JaiUser
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'partner', 'tel_number',
                  'is_costumer')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        exclude = ('partner',)

