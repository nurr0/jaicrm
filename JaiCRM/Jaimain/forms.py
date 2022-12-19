from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from .models import *


class AddPartnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Partner
        fields = ['name', 'logo', 'description', 'iin', 'partner_person', 'partner_tel', 'partner_email', 'time_start_working',  'time_expires', 'is_working']
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



