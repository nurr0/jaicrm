from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from .forms import *
from .models import *
from django.http import HttpResponse
from django.template import loader
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


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
              'partner_person', 'time_start_working', 'time_expires', 'is_working']
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
