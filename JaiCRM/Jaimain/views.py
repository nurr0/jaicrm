from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .models import *
from django.http import HttpResponse
from django.template import loader
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics
from Jaimain.serializers import *


class Partners(DataMixin, ListView):
    model = Partner
    template_name = 'Jaimain/partners.html'
    context_object_name = 'partners'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Партнеры')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = Partner.objects.all() if user.is_superuser else Partner.objects.filter(pk=user.partner.pk)
        return queryset


class ShowPartner(DataMixin, DetailView):
    model = Partner
    template_name = 'Jaimain/partner.html'
    pk_url_kwarg = 'partner_pk'
    context_object_name = 'partner'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Партнеры')
        c_def['shops_info'] = Shop.objects.all()
        c_def['product_cats_info'] = ProductCategory.objects.all()
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    # def get(self, request):
    #     partner_data = Partner.objects.all()
    #     shops_data = Shop.objects.all()
    #     return render(request, 'Jaimain/partner.html', {'partner_data': partner_data, 'shops_data': shops_data})


class AddPartner(DataMixin, CreateView):
    form_class = AddPartnerForm
    template_name = 'Jaimain/addpartner.html'
    success_url = reverse_lazy('partners')
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление партнера')
        return dict(list(context.items()) + list(c_def.items()))


class EditPartner(DataMixin, UpdateView):
    model = Partner
    fields = ['name', 'description', 'partner_tel', 'partner_email',
              'partner_person', 'time_start_working', 'time_expires', 'is_working', 'receipt_prefix']
    template_name = 'Jaimain/editpartner.html'
    success_url = '/partners/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение партнера')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def search_partners(request):
    if request.user.is_costumer:
        raise PermissionDenied
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
    model = JaiUser
    template_name = 'Jaimain/users.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пользователи')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return JaiUser.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = JaiUser.objects.all() if user.is_superuser else JaiUser.objects.filter(partner=user.partner)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ShowUser(DataMixin, DetailView):
    model = JaiUser
    template_name = 'Jaimain/show_user.html'
    pk_url_kwarg = 'jaiuser_pk'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Партнеры')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class EditUser(DataMixin, UpdateView):
    model = JaiUser
    fields = ['last_name', 'first_name', 'email', 'is_active']
    template_name = 'Jaimain/edituser.html'
    success_url = '/users/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение пользователя')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


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


def HomePage(request):
    return redirect('partners')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required()
def search_users(request):
    if request.user.is_costumer:
        raise PermissionDenied
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
    model = Shop
    template_name = 'Jaimain/shops.html'
    context_object_name = 'shops'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Торговые точки')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = Shop.objects.all() if user.is_superuser else Shop.objects.filter(partner=user.partner)
        return queryset


def add_shop(request):
    template = 'Jaimain/addshop.html'
    user_menu = menu.copy()
    form = AddShopForm()
    context = {'menu': user_menu, 'form': form}

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

    return render(request, template, context=context)


class ShowShop(DataMixin, DetailView):
    model = Shop
    template_name = 'Jaimain/show_shop.html'
    pk_url_kwarg = 'shop_pk'
    context_object_name = 'shop'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Торговая точка')
        c_def['products_in_shop'] = ProductInStock.objects.filter(shop=self.object)
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class EditShop(DataMixin, UpdateView):
    model = Shop
    fields = ['name', 'description', 'location']
    template_name = 'Jaimain/editshop.html'
    success_url = '/shops/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение торговой точки')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def add_product_category(request):
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
            return redirect('product_categories/')
        else:
            form = AddProductCategoryForm()
    categories = ProductCategory.objects.filter(partner=request.user.partner)
    form.fields['parent'].queryset = categories

    return render(request, template, context=context)


class ProductCategoriesList(DataMixin, ListView):
    model = Shop
    template_name = 'Jaimain/product_categories.html'
    context_object_name = 'product_cats'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Торговые точки')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = ProductCategory.objects.all() if user.is_superuser else ProductCategory.objects.filter(
            partner=user.partner)
        return queryset


# class EditProductCategory(DataMixin, UpdateView):
#     model = ProductCategory
#     fields = ['name', 'parent']
#     template_name = 'Jaimain/editproductcategory.html'
#     success_url = '/product_categories/'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Изменение товарной категории')
#         return dict(list(context.items()) + list(c_def.items()))
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_costumer:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)


def edit_product_category(request, pk):
    product_category = get_object_or_404(ProductCategory, pk=pk)
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
    model = ProductProperty
    template_name = 'Jaimain/product_properties.html'
    context_object_name = 'product_props'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Торговые точки')
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
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def add_sku(request):
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
                    if form.cleaned_data.get('DELETE'):
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
    return render(request, 'Jaimain/add_sku.html', {
        'sku_form': sku_form,
        'productpropertyrelation_formset': productpropertyrelation_formset, 'menu': user_menu
    })


def edit_sku(request, sku_pk):
    user_menu = menu.copy()
    sku = get_object_or_404(SKU, pk=sku_pk)

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
        'productpropertyrelation_formset': productpropertyrelation_formset, 'menu': user_menu
    })


class SKUList(DataMixin, ListView):
    model = SKU
    template_name = 'Jaimain/sku.html'
    context_object_name = 'sku_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
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
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def add_supply(request):
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
                    if form.cleaned_data.get('DELETE'):
                        continue
                    products_in_supply = form.save(commit=False)
                    products_in_supply.supply = supply
                    products_in_supply.save()
                    amount_added = products_in_supply.amount
                    product_added = products_in_supply.product
                    product_in_stock: object = ProductInStock.objects.filter(shop=shop_supply_to, product=product_added)
                    if len(product_in_stock) == 1:
                        product_in_stock.update(amount=F('amount') + amount_added)
                    elif len(product_in_stock) == 0:
                        save_product_to_warehouse = ProductInStock.objects.create(amount=amount_added,
                                                                                  product=product_added,
                                                                                  shop=shop_supply_to)
                        save_product_to_warehouse.save()
            except:
                supply.delete()
            return redirect('supplies')
        if not add_supply_form.is_valid():
            print(add_supply_form.errors)
    else:
        add_supply_form = AddSupplyForm()
        products_in_supply_formset = ProductsInSupplyFormSet()

    add_supply_form.fields['warehouse'].queryset = Shop.objects.filter(partner=request.user.partner)
    for form in products_in_supply_formset:
        form.fields['product'].queryset = SKU.objects.filter(partner=request.user.partner)

    return render(request, 'Jaimain/add_supply.html', {
        'add_supply_form': add_supply_form,
        'products_in_supply_formset': products_in_supply_formset, 'menu': user_menu
    })


class SupplyList(DataMixin, ListView):
    model = Supply
    template_name = 'Jaimain/supplies.html'
    context_object_name = 'supply_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Список поступлений товаров')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        queryset = Supply.objects.all() if user.is_superuser else Supply.objects.filter(
            partner=user.partner)
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
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


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
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def remove_products_from_shop(request, shop_pk):
    user_menu = menu.copy()
    template = 'Jaimain/product_remove.html'
    shop = Shop.objects.get(pk=shop_pk)
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


# def decrease_product_amount(request):
#     if request.method == 'POST':
#         form = DecreaseAmountForm(request.POST)
#         if form.is_valid():
#             product_id = form.cleaned_data['product_id']
#             decrease_amount = form.cleaned_data['decrease_amount']
#             product_in_stock = get_object_or_404(ProductInStock, product_id=product_id)
#             product_in_stock.amount -= decrease_amount
#             product_in_stock.save()
#             return render(request, 'decrease_success.html')
#     else:
#         form = DecreaseAmountForm()
#     return render(request, 'decrease_form.html', {'form': form})

class ProductInStockList(DataMixin, ListView):
    model = ProductInStock
    template_name = 'Jaimain/products_in_stock.html'
    context_object_name = 'products_in_stock'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Товары в продаже')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        partners_shops = Shop.objects.filter(partner=user.partner)
        queryset = ProductInStock.objects.all() if user.is_superuser else ProductInStock.objects.filter(
            shop__in=partners_shops)
        return queryset


def add_sell_price(request):
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
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def register_a_sale(request):
    user_menu = menu.copy()
    partner = request.user.partner
    receipt_number = SellReceipt.get_receipt_number_for_partner(partner)
    shops = Shop.objects.filter(partner=request.user.partner)
    if request.method == 'POST':
        receipt_form = SaleRegistrationForm(request.POST)
        products_in_receipt_formset = ProductsInReceiptFormSet(request.POST)
        if receipt_form.is_valid() and products_in_receipt_formset.is_valid():
            receipt = receipt_form.save(commit=False)
            receipt.partner = partner
            receipt.user_created = request.user
            receipt.number = receipt_number
            shop_sold_from = receipt.shop
            receipt.save()
            for form in products_in_receipt_formset:
                if form.is_valid:
                    if form.cleaned_data.get('DELETE'):
                        continue
                    products_in_receipt = form.save(commit=False)
                    products_in_receipt.receipt = receipt
                    products_in_receipt.save()
                    amount_sold = products_in_receipt.amount
                    product_sold = products_in_receipt.product
                    # sold_amount = form.cleaned_data['decrease_amount']
                    product_in_stock = form.cleaned_data['product']
                    if product_in_stock.amount >= amount_sold:
                        product_in_stock.amount -= amount_sold
                        product_in_stock.save()
                        form.save()

            return redirect('/')
        if not receipt_form.is_valid():
            print(receipt_form.errors)
    else:
        receipt_form = SaleRegistrationForm()
        products_in_receipt_formset = ProductsInReceiptFormSet()

    receipt_form.fields['receipt_number_display'].initial = f'{partner.receipt_prefix} {receipt_number}'
    receipt_form.fields['shop'].queryset = Shop.objects.filter(partner=request.user.partner)
    for form in products_in_receipt_formset:
        form.fields['product'].queryset = ProductInStock.objects.filter(shop__in=shops, amount__gt=0)

    return render(request, 'Jaimain/receipt_registration.html', {
        'receipt_form': receipt_form,
        'products_in_receipt_formset': products_in_receipt_formset, 'menu': user_menu, 'title': 'Регистрация продажи'
    })


class SellReceiptList(DataMixin, ListView):
    model = SellReceipt
    template_name = 'Jaimain/sell_receipt_list.html'
    context_object_name = 'sell_receipt_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Продажи')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        partner = self.request.user.partner
        queryset = SellReceipt.objects.all() if user.is_superuser else SellReceipt.objects.filter(
            partner=partner)
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
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_costumer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PropertyAPIView(generics.ListCreateAPIView):
    queryset = ProductProperty.objects.all()
    serializer_class = PropertySerializer


class PropertyAPIUpdate(generics.UpdateAPIView):
    queryset = ProductProperty.objects.all()
    serializer_class = PropertySerializer


class PartnerAPIView(generics.ListAPIView):
    queryset = Partner.objects.all()
