from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseNotFound, Http404
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
        login(self.request, user)
        return redirect('partners')  # не забыть исправить после реализации главной страницы

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
    results = []  # здесь будут храниться результаты поиска

    # выполняем поиск и заполняем список результатов
    if query:
        results = JaiUser.objects.filter(username__contains=query)

    # загружаем шаблон и передаем в него результаты поиска
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
