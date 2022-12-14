from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from .models import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


class Partners(DataMixin, ListView):
    model = Partner
    template_name = 'Jaimain/partners.html'
    context_object_name = 'partners'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Партнеры')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Partner.objects.all()

class AddPartner(DataMixin, CreateView):
    form_class = AddPartnerForm
    template_name = 'Jaimain/addpartner.html'
    success_url = reverse_lazy('partners')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление партнера')
        return dict(list(context.items()) + list(c_def.items()))
