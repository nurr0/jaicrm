import time

import jwt
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Jaimain.serializers import *
from .dashboard import METABASE_SECRET_KEY, METABASE_SITE_URL
from .forms import *
from .service import data_for_sales_by_cat_donought, data_for_sales_by_shop_graph, \
    data_for_sales_by_payment_form_donought, data_for_sales_by_sales_channel_donought
from .tasks import *
from .utils import *


def partner_time_expired(request):
    return render(request, 'Jaimain/partner_time_expired.html')


class Partners(DataMixin, ListView):
    model = Partner
    template_name = 'Jaimain/partners.html'
    context_object_name = 'partners'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Партнеры')
        return {**context, **c_def}

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Partner.objects.all()
        else:
            queryset = Partner.objects.filter(pk=user.partner.pk)
        return queryset


class ShowPartner(DataMixin, DetailView):
    model = Partner
    template_name = 'Jaimain/partner.html'
    pk_url_kwarg = 'partner_pk'
    context_object_name = 'partner'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Партнеры')
        c_def['shops_info'] = Shop.objects.filter(partner=self.object)
        c_def['sales_channel'] = SalesChannel.objects.filter(partner=self.object)
        c_def['payment_form'] = PaymentForm.objects.filter(partner=self.object)
        c_def['bsl'] = BaseLoyaltySystem.objects.filter(partner=self.object)
        c_def['user'] = self.request.user
        return {**context, **c_def}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object()
        if user.is_superuser or user.partner == partner:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class AddPartner(DataMixin, CreateView):
    form_class = AddPartnerForm
    template_name = 'Jaimain/addpartner.html'
    success_url = reverse_lazy('partners')
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление партнера')
        return {**context, **c_def}


class EditPartner(DataMixin, UpdateView):
    model = Partner
    fields = ['name', 'description', 'partner_tel', 'partner_email',
              'partner_person', 'time_start_working', 'time_expires', 'is_working', 'receipt_prefix']
    template_name = 'Jaimain/editpartner.html'
    success_url = '/partners/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение партнера')
        return {**context, **c_def}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object()
        if user.is_superuser or (user.partner == partner and user.is_partner_admin):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



@login_required
def search_partners(request):
    query = request.GET.get('q')
    results = []  # здесь будут храниться результаты поиска

    # выполняем поиск и заполняем список результатов
    if query:
        results = Partner.objects.filter(name__contains=query)

    # загружаем шаблон и передаем в него результаты поиска
    template = loader.get_template('Jaimain/search_results.html')
    context = {
        'results': results,
    }
    user_menu = menu.copy()
    context['menu'] = user_menu
    return HttpResponse(template.render(context, request))


class UsersList(DataMixin, ListView):
    paginate_by = 20
    model = JaiUser
    template_name = 'Jaimain/users.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пользователи')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = JaiUser.objects.all() if user.is_superuser else JaiUser.objects.filter(partner=user.partner)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)


class ShowUser(DataMixin, DetailView):
    model = JaiUser
    template_name = 'Jaimain/show_user.html'
    pk_url_kwarg = 'jaiuser_pk'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Просмотр пользователя')
        c_def['self_user'] = self.request.user
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object().partner
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif user.partner == partner and (user.is_partner_admin or user == self.get_object()):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class EditUser(DataMixin, UpdateView):
    model = JaiUser
    fields = ['last_name', 'first_name', 'email', 'shop_allowed', 'is_active', 'is_partner_admin']
    template_name = 'Jaimain/edituser.html'
    success_url = '/users/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение пользователя')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object().partner
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif user.partner == partner and user.is_partner_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'Jaimain/registeruser.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация пользователя')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'Jaimain/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('partners')

@login_required()
def home_page(request):
    request.session.set_expiry(3600)
    return redirect('dashboard')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required()
def search_users(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = JaiUser.objects.filter(username__contains=query)

    template = loader.get_template('Jaimain/user_search_results.html')
    context = {
        'results': results,
    }
    user_menu = menu.copy()
    context['menu'] = user_menu
    return HttpResponse(template.render(context, request))


class ShowShops(DataMixin, ListView):
    paginate_by = 10
    model = Shop
    template_name = 'Jaimain/shops.html'
    context_object_name = 'shops'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Торговые точки')
        c_def['user_partner'] = self.request.user.partner
        c_def['self_user'] = self.request.user
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = Shop.objects.all() if user.is_superuser else Shop.objects.filter(partner=user.partner)
        return queryset


@login_required
def add_shop(request):
    request.session.set_expiry(3600)
    template = 'Jaimain/addshop.html'
    user_menu = menu.copy()
    form = AddShopForm()
    context = {'menu': user_menu, 'form': form}
    if not request.user.is_partner_admin:
        raise PermissionDenied
    if request.method == 'POST':
        form = AddShopForm(request.POST)
        if form.is_valid():
            partner = request.user.partner
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']
            is_working = form.cleaned_data['is_working']
            queryset = Shop.objects.create(partner=partner, name=name, location=location,
                                           description=description, is_working=is_working)
            return redirect('shops')
        else:
            form = AddShopForm()

    return render(request, template, context=context, self_user=request.user)


class ShowShop(DataMixin, DetailView):
    model = Shop
    template_name = 'Jaimain/show_shop.html'
    pk_url_kwarg = 'shop_pk'
    context_object_name = 'shop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Торговая точка')
        c_def['products_in_shop'] = ProductInStock.objects.filter(shop=self.object)
        c_def['self_user'] = self.request.user
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object().partner
        if user.is_superuser or user.partner == partner:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class EditShop(DataMixin, UpdateView):
    model = Shop
    fields = ['name', 'description', 'location']
    template_name = 'Jaimain/editshop.html'
    success_url = '/shops/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение торговой точки')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object().partner
        if user.is_superuser or user.partner == partner:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


@login_required
def add_product_category(request):
    request.session.set_expiry(3600)
    template = 'Jaimain/addrootproductcategory.html'
    form = AddProductCategoryForm()
    partner = request.user.partner
    user_menu = menu.copy()
    context = {'partner': partner, 'form': form, 'menu': user_menu}

    if request.method == 'POST':
        form = AddProductCategoryForm(request.POST)
        if form.is_valid():
            partner = request.user.partner
            parent = form.cleaned_data['parent']
            name = form.cleaned_data['name']
            try:
                queryset = ProductCategory.objects.create(partner=partner, name=name, parent=parent)
            except:
                form = AddProductCategoryForm()


class ProductCategoriesList(DataMixin, ListView):
    model = Shop
    template_name = 'Jaimain/product_categories.html'
    context_object_name = 'product_cats'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категории товаров')
        c_def['user_partner'] = self.request.user.partner
        c_def['prod_cats'] = ProductCategory.objects.filter(partner=self.request.user.partner)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = ProductCategory.objects.all() if user.is_superuser else ProductCategory.objects.filter(
            partner=user.partner)
        return queryset


@login_required()
def edit_product_category(request, pk):
    request.session.set_expiry(3600)
    product_category = get_object_or_404(ProductCategory, pk=pk)
    if request.user.partner != product_category.partner:
        raise PermissionDenied
    user_menu = menu.copy()
    partner = request.user.partner
    context = {'partner': partner, 'menu': user_menu, }

    if request.method == 'POST':
        form = AddProductCategoryForm(request.POST, instance=product_category)
        form.fields['parent'].queryset = ProductCategory.objects.filter(partner=request.user.partner)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_categories'))
    else:
        form = AddProductCategoryForm(instance=product_category)

    categories = ProductCategory.objects.filter(partner=request.user.partner)
    form.fields['parent'].queryset = categories
    context['form'] = form
    return render(request, 'Jaimain/editproductcategory.html', context=context)


def add_product_property(request):
    template = 'Jaimain/addproductproperty.html'
    form = AddProductPropertyForm()
    partner = request.user.partner
    user_menu = menu.copy()
    context = {'partner': partner, 'form': form, 'menu': user_menu}

    if request.method == 'POST':
        form = AddProductPropertyForm(request.POST)
        if form.is_valid():
            partner = request.user.partner
            name = form.cleaned_data['name']
            try:
                queryset = ProductProperty.objects.create(partner=partner, name=name)
            except:
                form = AddProductPropertyForm()
            return redirect('product_properties')
        else:
            form = AddProductPropertyForm()

    return render(request, template, context=context)


class ProductPropertiesList(DataMixin, ListView):
    paginate_by = 20
    model = ProductProperty
    template_name = 'Jaimain/product_properties.html'
    context_object_name = 'product_props'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Торговые точки')
        c_def['user_partner'] = self.request.user.partner
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = ProductProperty.objects.all() if user.is_superuser else ProductProperty.objects.filter(
            partner=user.partner)
        return queryset


class EditProductProperty(DataMixin, UpdateView):
    model = ProductProperty
    fields = ['name']
    template_name = 'Jaimain/editproductproperty.html'
    success_url = '/product_properties/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение свойства товара')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object().partner
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif user.partner == partner:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

@login_required()
def add_sku(request):
    request.session.set_expiry(3600)
    user_menu = menu.copy()
    # context = {'partner': partner, 'form': form, 'menu': user_menu}
    if request.method == 'POST':
        sku_form = AddSKUForm(request.POST, request.FILES)
        productpropertyrelation_formset = ProductPropertyRelationFormSet(request.POST)

        if sku_form.is_valid() and productpropertyrelation_formset.is_valid():
            sku = sku_form.save(commit=False)
            sku.partner = request.user.partner
            sku.image = sku_form.cleaned_data['image']
            sku.save()

            try:
                for form in productpropertyrelation_formset:
                    if form.cleaned_data.get('DELETE') or not form.cleaned_data.get('property'):
                        continue
                    property_relation = form.save(commit=False)
                    property_relation.product = sku
                    property_relation.save()
            except:
                sku.delete()

            return redirect('sku')

        if not sku_form.is_valid():
            print(sku_form.errors)

    else:
        sku_form = AddSKUForm()
        productpropertyrelation_formset = ProductPropertyRelationFormSet()

    sku_form.fields['category'].queryset = ProductCategory.objects.filter(partner=request.user.partner)

    for form in productpropertyrelation_formset:
        form.fields['property'].queryset = ProductProperty.objects.filter(partner=request.user.partner)

    return render(request, 'Jaimain/add_sku.html', {
        'sku_form': sku_form,
        'productpropertyrelation_formset': productpropertyrelation_formset,
        'menu': user_menu,
    })


@login_required()
def edit_sku(request, sku_pk):
    request.session.set_expiry(3600)
    user_menu = menu.copy()
    sku = get_object_or_404(SKU, pk=sku_pk)
    if sku.partner != request.user.partner:
        raise PermissionDenied

    if request.method == 'POST':
        sku_form = AddSKUForm(request.POST, request.FILES, instance=sku)
        productpropertyrelation_formset = ProductPropertyRelationFormSet(request.POST, instance=sku)
        if sku_form.is_valid() and productpropertyrelation_formset.is_valid():
            sku = sku_form.save()
            for form in productpropertyrelation_formset:
                if form.cleaned_data.get('DELETE'):
                    if form.instance.pk:
                        form.instance.delete()
                else:
                    property_relation = form.save(commit=False)
                    property_relation.product = sku
                    property_relation.save()
            return redirect('sku')
    else:
        sku_form = AddSKUForm(instance=sku)
        productpropertyrelation_formset = ProductPropertyRelationFormSet(instance=sku)

    sku_form.fields['category'].queryset = ProductCategory.objects.filter(partner=request.user.partner)
    return render(request, 'Jaimain/edit_sku.html', {
        'sku_form': sku_form,
        'productpropertyrelation_formset': productpropertyrelation_formset,
        'menu': user_menu
    })


class SKUList(DataMixin, ListView):
    paginate_by = 20
    model = SKU
    template_name = 'Jaimain/sku.html'
    context_object_name = 'sku_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Список SKU Партнера')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = SKU.objects.all() if user.is_superuser else SKU.objects.filter(
            partner=user.partner)
        return queryset


class ShowSKU(DataMixin, DetailView):
    model = SKU
    template_name = 'Jaimain/show_sku.html'
    pk_url_kwarg = 'sku_pk'
    context_object_name = 'sku'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Просмотр SKU')
        c_def['properties_list'] = ProductPropertyRelation.objects.filter(product_id=self.object.pk)
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        partner = self.get_object().partner
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif user.partner == partner:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


@login_required()
def add_supply(request):
    request.session.set_expiry(3600)
    user_menu = menu.copy()

    if request.method == 'POST':
        add_supply_form = AddSupplyForm(request.POST)
        products_in_supply_formset = ProductsInSupplyFormSet(request.POST)

        if add_supply_form.is_valid() and products_in_supply_formset.is_valid():
            supply = add_supply_form.save(commit=False)
            supply.partner = request.user.partner
            supply.save()
            shop_supply_to = supply.warehouse

            try:
                for form in products_in_supply_formset:
                    if not form.cleaned_data.get('product'):
                        continue

                    if form.is_valid:
                        products_in_supply = form.save(commit=False)
                        products_in_supply.supply = supply
                        products_in_supply.save()
                        amount_added = products_in_supply.amount
                        product_added = products_in_supply.product
                        product_exists = ProductInStock.objects.filter(shop=shop_supply_to, product=product_added).exists()

                        if product_exists:
                            product = ProductInStock.objects.get(shop=shop_supply_to, product=product_added)
                            product.amount += amount_added
                            product.save()
                        else:
                            ProductInStock.objects.create(amount=amount_added, product=product_added, shop=shop_supply_to)

                if all([form.cleaned_data.get('product') is None for form in products_in_supply_formset]):
                    supply.delete()

            except:
                supply.delete()

            return redirect('supplies')

        if not add_supply_form.is_valid():
            print(add_supply_form.errors)

    else:
        add_supply_form = AddSupplyForm()
        products_in_supply_formset = ProductsInSupplyFormSet()

    if request.user.is_partner_admin or request.user.shop_allowed is None:
        add_supply_form.fields['warehouse'].queryset = Shop.objects.filter(partner=request.user.partner)
    else:
        add_supply_form.fields['warehouse'].queryset = Shop.objects.filter(pk=request.user.shop_allowed.pk)
        add_supply_form.fields['warehouse'].initial = request.user.shop_allowed.pk

    for form in products_in_supply_formset:
        form.fields['product'].queryset = SKU.objects.filter(partner=request.user.partner)

    return render(request, 'Jaimain/add_supply.html', {
        'add_supply_form': add_supply_form,
        'products_in_supply_formset': products_in_supply_formset,
        'menu': user_menu
    })


class SupplyList(DataMixin, ListView):
    paginate_by = 20
    model = Supply
    template_name = 'Jaimain/supplies.html'
    context_object_name = 'supply_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Список поступлений товаров')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Supply.objects.all()
        elif user.is_partner_admin or user.shop_allowed is None:
            queryset = Supply.objects.filter(partner=user.partner)
        else:
            queryset = Supply.objects.filter(warehouse=user.shop_allowed.pk)

        return queryset


class ShowSupply(DataMixin, DetailView):
    model = Supply
    template_name = 'Jaimain/show_supply.html'
    pk_url_kwarg = 'supply_pk'
    context_object_name = 'supply'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Просмотр Поступления товаров')
        c_def['product_in_supply_list'] = ProductsInSupply.objects.filter(supply=self.object)
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.is_partner_admin and user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class EditSupply(DataMixin, UpdateView):
    model = Supply
    fields = ['document', 'supplier', 'date']
    template_name = 'Jaimain/edit_supply.html'
    success_url = '/supplies/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение документа поступления товаров')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.is_partner_admin and user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

@login_required()
def remove_products_from_shop(request, shop_pk):
    request.session.set_expiry(3600)
    user_menu = menu.copy()
    template = 'Jaimain/product_remove.html'
    shop = Shop.objects.get(pk=shop_pk)

    if not request.user.is_partner_admin:
        raise PermissionDenied

    if request.user.partner != shop.partner:
        raise PermissionDenied

    if request.user.shop_allowed and request.user.shop_allowed != shop:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProductsRemoveForm(request.POST)
        if form.is_valid():
            remove = form.save(commit=False)
            remove.shop = shop
            remove.user_created = request.user
            decrease_amount = form.cleaned_data['decrease_amount']
            product_in_stock = form.cleaned_data['product']
            if product_in_stock.amount >= decrease_amount:
                product_in_stock.amount -= decrease_amount
                product_in_stock.save()
                remove.save()
                return redirect('showshop', shop_pk)
            else:
                raise forms.ValidationError('Количество списываемого товара не может быть больше имеющегося')
    else:
        form = ProductsRemoveForm()
    form.fields['product'].queryset = ProductInStock.objects.filter(shop_id=shop_pk)

    return render(request, template, {'form': form, 'menu': user_menu, 'title': 'Списание товаров со склада'})


class ProductInStockList(DataMixin, ListView):
    paginate_by = 20
    model = ProductInStock
    template_name = 'Jaimain/products_in_stock.html'
    context_object_name = 'products_in_stock'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Товары в продаже')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        partners_shops = Shop.objects.filter(partner=user.partner)
        if self.request.user.is_superuser:
            queryset = ProductInStock.objects.all()
        elif self.request.user.is_partner_admin or self.request.user.shop_allowed is None:
            queryset = ProductInStock.objects.filter(shop__in=partners_shops)
        else:
            queryset = ProductInStock.objects.filter(shop=self.request.user.shop_allowed)
        return queryset

@login_required()
def add_sell_price(request):
    request.session.set_expiry(3600)
    if not request.user.is_partner_admin and not request.user.is_superuser:
       raise PermissionDenied
    user_menu = menu.copy()
    shops = Shop.objects.filter(partner=request.user.partner)
    queryset = ProductInStock.objects.filter(sellprice__isnull=True, shop__in=shops)
    formset_class = formset_factory(AddSellPriceForm, extra=len(queryset), can_delete_extra=True, can_delete=True)

    if request.method == 'POST':
        formset = formset_class(request.POST)

        if formset.is_valid():
            for i, form in enumerate(formset):
                form.instance.partner = request.user.partner
                form.instance.product_in_stock = queryset[i]

                if form.cleaned_data.get('DELETE'):
                    continue
                try:
                    form.save()
                except IntegrityError:
                    messages.error(request, 'Цена для данного товара уже установлена')

            return redirect('products_in_stock')
    else:
        formset = formset_class()
        for i, form in enumerate(formset):
            form.fields['product_in_stock'].initial = queryset[i]
            form.fields['product_in_stock_display'].initial = str(queryset[i])
            form.fields['product_latest_supply_price'].initial = str(queryset[i].get_latest_supply_price())

    return render(request, 'Jaimain/add_price.html',
                  {'formset': formset, 'menu': user_menu, 'title': 'Добавление цены'})


class EditRetailPrice(DataMixin, UpdateView):
    model = SellPrice
    fields = ['price']
    template_name = 'Jaimain/edit_retail_price.html'
    success_url = '/products_in_stock/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение продажной цены',
                                      product=f'{self.object.product_in_stock}', )

        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.is_partner_admin and user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    """ДОДЕЛАТЬ НАЧИСЛЕНИЕ БОНУСОВ"""

@login_required()
def register_a_sale(request):
    request.session.set_expiry(3600)
    partner = request.user.partner
    receipt_number = SellReceipt.get_receipt_number_for_partner(partner)
    user_menu = menu.copy()
    bsl_queryset = BaseLoyaltySystem.objects.filter(partner=partner)

    if request.method == 'POST':
        receipt_form = SaleRegistrationForm(request.POST)
        products_in_receipt_formset = ProductsInReceiptFormSet(request.POST)
        if receipt_form.is_valid() and products_in_receipt_formset.is_valid():
            receipt = receipt_form.save(commit=False)
            receipt.partner = partner
            receipt.user_created = request.user
            receipt.number = receipt_number
            receipt.save()
            receipt_deleted = False
            for form in products_in_receipt_formset:
                if form.is_valid():
                    if not form.cleaned_data.get('product'):
                        continue
                    product_in_receipt = form.save(commit=False)
                    product_in_receipt.receipt = receipt
                    amount_sold = product_in_receipt.amount
                    product_in_stock = form.cleaned_data['product']
                    product_in_stock.amount -= amount_sold
                    product_in_stock.save()
                    product_in_receipt.save()

            if all([form.cleaned_data.get('product') is None for form in products_in_receipt_formset]):
                receipt.delete()
                receipt_deleted = True
                raise ValidationError('Нельзя создать чек без товаров')

            if not receipt_deleted:
                customer = receipt_form.cleaned_data['customer']
                if customer:
                    if bsl_queryset:
                        bsl = bsl_queryset[0]
                        if receipt_form.cleaned_data['points_achieve_or_spend'] == 'recieve':
                            points_achieve = int(int(receipt.get_total_price_with_discount()) * (bsl.points_achieve / 100))
                            points_queryset = Points.objects.create(customer=customer,
                                                                    partner=partner,
                                                                    points_amount=points_achieve,
                                                                    receipt=receipt,
                                                                    receive_or_spend='recieve')
                            points_queryset.save()
                        elif receipt_form.cleaned_data['points_achieve_or_spend'] == 'spend' and \
                                receipt_form.cleaned_data['points_used'] > 0:
                            points_queryset = Points.objects.create(customer=customer,
                                                                    partner=partner,
                                                                    points_amount=receipt_form.cleaned_data['points_used'],
                                                                    receipt=receipt,
                                                                    receive_or_spend='spend')
                            points_queryset.save()

            return redirect('sell_receipt_list')

        if not receipt_form.is_valid():
            print(receipt_form.errors)
    else:
        receipt_form = SaleRegistrationForm()
        products_in_receipt_formset = ProductsInReceiptFormSet()

    receipt_form.fields['receipt_number_display'].initial = f'{partner.receipt_prefix} {receipt_number}'
    receipt_form.fields['points_used'].initial = 0
    if request.user.is_partner_admin or request.user.shop_allowed is None:
        receipt_form.fields['shop'].queryset = Shop.objects.filter(partner=partner)
    else:
        receipt_form.fields['shop'].queryset = Shop.objects.filter(pk=request.user.shop_allowed.pk)
        receipt_form.fields['shop'].initial = request.user.shop_allowed
    receipt_form.fields['sales_channel'].queryset = SalesChannel.objects.filter(partner=partner)
    receipt_form.fields['payment_form'].queryset = PaymentForm.objects.filter(partner=partner)
    receipt_form.fields['customer'].queryset = Customer.objects.filter(partner=partner)

    for form in products_in_receipt_formset:
        if request.user.is_partner_admin or request.user.shop_allowed is None:
            form.fields['product'].queryset = ProductInStock.objects.filter(shop__partner=partner, amount__gt=0)
        else:
            form.fields['product'].queryset = ProductInStock.objects.filter(shop=request.user.shop_allowed, amount__gt=0)
        form.fields['DELETE'].initial = False

    return render(request, 'Jaimain/receipt_registration.html', {
        'receipt_form': receipt_form,
        'products_in_receipt_formset': products_in_receipt_formset,
        'menu': user_menu,
        'title': 'Регистрация продажи',
        'partner_bsl': bsl_queryset[0]
    })


class SellReceiptList(DataMixin, ListView):
    paginate_by = 20
    model = SellReceipt
    template_name = 'Jaimain/sell_receipt_list.html'
    context_object_name = 'sell_receipt_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Продажи')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        partner = self.request.user.partner
        if user.is_superuser:
            queryset = SellReceipt.objects.all().order_by(
            '-time_created')
        elif user.is_partner_admin:
            queryset = SellReceipt.objects.filter(partner=partner).order_by('-time_created')
        else:
            queryset = SellReceipt.objects.filter(shop=user.shop_allowed).order_by('-time_created')
        return queryset


class ShowSellReceipt(DataMixin, DetailView):
    model = SellReceipt
    template_name = 'Jaimain/show_receipt.html'
    pk_url_kwarg = 'receipt_pk'
    context_object_name = 'receipt'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Просмотр документа продажи')
        c_def['products_in_receipt'] = ProductInReceipt.objects.filter(receipt=self.object)
        c_def['points_achieved'] = Points.objects.filter(receipt=self.object)
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or \
                (user.is_partner_admin and user.partner == self.get_object().partner) or \
                (user.shop_allowed == self.get_object().shop):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class SellReceiptReturnView(DataMixin, UpdateView):
    model = SellReceipt
    fields = ('is_returned',)
    # pk_url_kwarg = 'receipt_pk'
    template_name = 'Jaimain/receipt_return.html'
    success_url = reverse_lazy('sell_receipt_list')

    def form_valid(self, form):
        receipt = form.save(commit=False)
        receipt.is_returned = True
        receipt.save()
        try:
            points_return = Points.objects.get(receipt=receipt)
            points_return.delete()
        except:
            pass

        products_in_receipt = ProductInReceipt.objects.filter(receipt=receipt)
        for products_item in products_in_receipt:
            product_in_stock = ProductInStock.objects.get(pk=products_item.product.pk)
            product_in_stock.amount += products_item.amount
            product_in_stock.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение свойства товара')
        c_def['receipt'] = SellReceipt.objects.get(pk=self.object.pk)
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or \
                (user.is_partner_admin and user.partner == self.get_object().partner) or \
                (user.shop_allowed == self.get_object().shop):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


@login_required()
def export_sales_data(request):
    request.session.set_expiry(3600)
    if request.method == 'POST':
        file_format = request.POST['file-format']
        export_sales_report.delay(user=request.user.pk, file_format=file_format)
        return redirect('sell_receipt_list')

    return render(request, 'Jaimain/export.html')


class ReportsList(DataMixin, ListView):
    paginate_by = 20
    model = ReportExport
    template_name = 'Jaimain/reports.html'
    context_object_name = 'reports'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Сформированные отчеты')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        partner = self.request.user.partner
        queryset = ReportExport.objects.all() if user.is_superuser else ReportExport.objects.filter(
            user__partner=partner)
        return queryset

@login_required()
def dashboard_old(request):
    user_menu = menu.copy()
    partner = request.user.partner

    data_sales_by_cat_pie = data_for_sales_by_cat_donought(
        partner)  # данные по продажам по категориям (функция в service)
    data_sales_by_shops_linear = data_for_sales_by_shop_graph(partner)  # линейный график продаж по магазинам
    data_sales_by_payment_forms_pie = data_for_sales_by_payment_form_donought(
        partner)  # круговая диаграмма по формам оплаты
    data_sales_by_sales_channel_pie = data_for_sales_by_sales_channel_donought(partner)

    return render(request, 'Jaimain/dashboard_old.html', {
        'menu': user_menu,
        'title': 'Dashboard',
        'data_sales_by_cat_pie': data_sales_by_cat_pie,
        'data_sales_by_shops_linear': data_sales_by_shops_linear,
        'data_sales_by_payment_forms_pie': data_sales_by_payment_forms_pie,
        'data_sales_by_sales_channel_pie': data_sales_by_sales_channel_pie

    })

@login_required()
def dashboard(request):
    request.session.set_expiry(3600)
    user_menu = menu.copy()
    partner = request.user.partner
    payload = {
        "resource": {"dashboard": 2},
        "params": {

        },
        "exp": round(time.time()) + (60 * 10)  # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#theme=transparent&bordered=false&titled=false"

    return render(request, 'Jaimain/dashboard.html', {
        'menu': user_menu,
        'title': 'Dashboard',
        'dashboard': iframeUrl

    })


class CustomersList(DataMixin, ListView):
    paginate_by = 20
    model = Customer
    template_name = 'Jaimain/customers.html'
    context_object_name = 'customers_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Клиенты')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        partner = self.request.user.partner
        queryset = Customer.objects.all() if user.is_superuser else Customer.objects.filter(
            partner=partner)
        return queryset


class CustomerCreation(DataMixin, CreateView):
    form_class = CustomerCreationForm
    template_name = 'Jaimain/customer_creation.html'
    success_url = reverse_lazy('customers')
    raise_exception = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление Клиента')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.partner = self.request.user.partner
        return super().form_valid(form)


class CustomerEdit(DataMixin, UpdateView):
    model = Customer
    fields = ['firstname', 'lastname', 'tel_number', 'gender', 'birthdate', 'city']
    template_name = 'Jaimain/customer_edit.html'
    success_url = reverse_lazy('customers')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение данных Клиента')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class CustomerShow(DataMixin, DetailView):
    model = Customer
    template_name = 'Jaimain/customer_show.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'customer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Информация о клиенте')
        c_def['points_amount'] = self.object.get_points_amount()
        c_def['points_history'] = Points.objects.filter(customer=self.object)
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class BaseLoyaltySystemCreation(DataMixin, CreateView):
    form_class = BaseLoyaltySystemForm
    template_name = 'Jaimain/bsl_create.html'
    success_url = reverse_lazy('partners')
    raise_exception = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        if request.user.is_superuser or request.user.is_partner_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление Базовой Системы Лояльности')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.partner = self.request.user.partner
        return super().form_valid(form)


class BaseLoyaltySystemEdit(DataMixin, UpdateView):
    model = BaseLoyaltySystem
    fields = ['points_achieve', 'points_spend']
    template_name = 'Jaimain/bsl_edit.html'
    success_url = reverse_lazy('partners')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение Базовой Системы Лояльности')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.is_partner_admin and user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PaymentFormEdit(DataMixin, UpdateView):
    model = PaymentForm
    fields = ['name']
    template_name = 'Jaimain/payment_form_edit.html'
    success_url = reverse_lazy('partners')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение Способа оплаты')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.is_partner_admin and user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class SalesChannelEdit(DataMixin, UpdateView):
    model = SalesChannel
    fields = ['name']
    template_name = 'Jaimain/sales_channel_edit.html'
    success_url = reverse_lazy('partners')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение Канала продаж')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session.set_expiry(3600)
        user = self.request.user
        if user.is_superuser or (user.is_partner_admin and user.partner == self.get_object().partner):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

@login_required()
def add_bug_report(request):
    request.session.set_expiry(3600)
    template = 'Jaimain/bugreport.html'
    form = BugReportForm()
    user_menu = menu.copy()
    context = {'form': form, 'menu': user_menu, 'title':'Форма обратной связи с разработчиком'}

    if request.method == 'POST':
        form = BugReportForm(request.POST, request.FILES)
        if form.is_valid():
            bug_report = form.save(commit=False)
            bug_report.user_created = request.user
            bug_report.save()
            return redirect('/')
    else:
        form = BugReportForm()
    return render(request, template, context=context)

"""API views \/"""


class PropertyAPIView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductProperty.objects.all()
        else:
            return ProductCategory.objects.filter(partner=self.request.user.partner)

class PropertyAPIUpdate(generics.UpdateAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductProperty.objects.all()
        else:
            return ProductCategory.objects.filter(partner=self.request.user.partner)

class PartnerAPIView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer



class ProductCategoryAPIView(generics.ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return ProductCategory.objects.filter(partner=self.request.user.partner)



class ShopApiView(generics.ListCreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Shop.objects.all()
        else:
            return Shop.objects.filter(partner=self.request.user.partner)

class SaleChannelAPIView(generics.ListCreateAPIView):
    serializer_class = SalesChannelSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SalesChannel.objects.all()
        else:
            return SalesChannel.objects.filter(partner=self.request.user.partner)


class PaymentFormAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentFormSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PaymentForm.objects.all()
        else:
            return PaymentForm.objects.filter(partner=self.request.user.partner)



class ReportsAPIView(generics.ListAPIView):
    serializer_class = ReportsSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        return ReportExport.objects.filter(user=self.request.user).order_by('-datetime')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sales_report_export_api(request):
    if request.method == 'POST':
        file_format = request.data['file-format']
        # user_pk = request.data['user']
        if file_format not in ('CSV', 'JSON', 'XLS (Excel)'):
            return Response({"error": "Укажите верный формат файла"})
        export_sales_report.delay(user=request.user.pk, file_format=file_format)
        # export_sales_report(user=request.user.pk, file_format=file_format)
        return Response({"message": "Запущена сборка отчета!"})
    return Response({"message": "Это апи для запуска сборки отчета, передайте в него file_format и user.id"})


class ProductInStockAPIView(generics.RetrieveAPIView):
    # queryset = ProductInStock.objects.all()
    serializer_class = ProductInStockSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductInStock.objects.all()
        else:
            return ProductInStock.objects.filter(shop__partner=self.request.user.partner)

class ProductInStockListAPIView(generics.ListAPIView):
    # queryset = ProductInStock.objects.all()
    serializer_class = ProductInStockSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductInStock.objects.all()
        else:
            return ProductInStock.objects.filter(shop__partner=self.request.user.partner)

class CustomerAPIView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()
        else:
            return Customer.objects.filter(partner=self.request.user.partner)

class CustomerListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()
        else:
            return Customer.objects.filter(partner=self.request.user.partner)


def temp_error404(request):
    template = 'core/error404.html'
    # user_menu = menu.copy()
    context = {'title': 'Страница не найдена'}
    return render(request, template, context=context)

def temp_error500(request):
    template = 'core/error500.html'
    # user_menu = menu.copy()
    context = {'title': 'ОШИБКА'}
    return render(request, template, context=context)

def temp_error403(request):
    template = 'core/error403.html'
    # user_menu = menu.copy()
    context = {'title': 'Доступ запрещен'}
    return render(request, template, context=context)
