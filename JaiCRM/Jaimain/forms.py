import mptt.forms
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory
from mptt.forms import *
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
    CHOICES = (
        (True, 'Да'),
        (False, 'Нет'),
    )
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    partner = forms.ModelChoiceField(label='Партнер', queryset=Partner.objects.all())
    tel_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-input'}))
    is_costumer = forms.ChoiceField(label='Является покупателем', choices=CHOICES)

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


class AddProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        exclude = ('partner',)


class AddProductPropertyForm(forms.ModelForm):
    name = forms.CharField(label='Наименование свойства')

    class Meta:
        model = ProductProperty
        exclude = ('partner',)


class AddSKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        exclude = ('partner',)


class ProductPropertyRelationForm(forms.ModelForm):
    class Meta:
        model = ProductPropertyRelation
        fields = ['property', 'value']


ProductPropertyRelationFormSet = inlineformset_factory(SKU, ProductPropertyRelation,
                                                       fields=['property', 'value'],
                                                       extra=5,
                                                       can_delete=True,
                                                       can_delete_extra=True)


class EditSKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = ['name', 'description', 'identifier', 'producer', 'partner', 'category']


class EditProductPropertyRelationForm(forms.ModelForm):
    class Meta:
        model = ProductPropertyRelation
        fields = ['property', 'value']


class AddSupplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['warehouse'].queryset = Shop.objects.filter(partner=user.partner)

    class Meta:
        model = Supply
        exclude = ['partner']

        widgets = {
            'supplier': forms.TextInput(),
            'document': forms.TextInput(),
            'date': forms.SelectDateWidget(years=list(range(2020, 2030))),
        }


class ProductsInSupplyForm(forms.ModelForm):
    class Meta:
        model = ProductsInSupply
        fields = '__all__'

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Количество товара не может быть меньше или равно 0")
        return amount


ProductsInSupplyFormSet = inlineformset_factory(Supply, ProductsInSupply,
                                                form=ProductsInSupplyForm,
                                                fields='__all__',
                                                extra=10,
                                                can_delete=True,
                                                can_delete_extra=True)


class ProductsRemoveForm(forms.ModelForm):
    class Meta:
        model = ProductsRemove
        exclude = ['shop', 'date_created', 'user_created']

    def clean_decrease_amount(self):
        decrease_amount = self.cleaned_data['decrease_amount']
        if decrease_amount <= 0:
            raise forms.ValidationError("Количество товара не может быть меньше или равно 0")
        return decrease_amount


class AddSellPriceForm(forms.ModelForm):
    product_in_stock_display = forms.CharField(label='Товар', widget=forms.TextInput(attrs={'readonly': True}))
    product_latest_supply_price = forms.CharField(label='Последняя стоимость поставки',
                                                  widget=forms.TextInput(attrs={'readonly': True}))

    class Meta:
        model = SellPrice
        fields = ['product_in_stock_display', 'product_latest_supply_price', 'product_in_stock', 'price', ]
        widgets = {'product_in_stock': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_in_stock'].queryset = ProductInStock.objects.filter(sellprice__isnull=True)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Цена товара не может быть меньше или равна 0")
        return price

    def save(self, commit=True):
        product_in_stock = self.cleaned_data.pop('product_in_stock')
        instance = super().save(commit=False)
        instance.product_in_stock = product_in_stock
        if commit:
            instance.save()
        return instance


class SaleRegistrationForm(forms.ModelForm):
    receipt_number_display = forms.CharField(label='Документ продажи:', widget=forms.TextInput(attrs={'readonly': True}))

    class Meta:
        model = SellReceipt
        fields = ['receipt_number_display', 'shop']


class ProductsInReceiptForm(forms.ModelForm):
    class Meta:
        model = ProductInReceipt
        fields = '__all__'

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Количество товара не может быть меньше или равно 0")
        elif amount > self.cleaned_data['product'].amount:
            raise forms.ValidationError("Количество товара в чеке не может превышать количество товара на складе")
        return amount

    def clean_discount(self):
        discount = self.cleaned_data['discount']
        if discount and discount >= 100:
            raise forms.ValidationError("Скидка не может быть больше или равна 100%")
        return discount


ProductsInReceiptFormSet = inlineformset_factory(SellReceipt, ProductInReceipt,
                                                 form=ProductsInReceiptForm,
                                                 fields='__all__',
                                                 extra=2,
                                                 can_delete=True,
                                                 can_delete_extra=True)
