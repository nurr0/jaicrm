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


class Partners(ListView):
    model = Partner
    template_name = 'Jaimain/partners.html'
    context_object_name = 'partners'
    menu = [{'title': "Партнеры", 'url_name': 'partners'},
            ]

    def get_queryset(self):
        return Partner.objects.all()
