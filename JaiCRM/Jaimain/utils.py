from django.db.models import *
from django.core.cache import cache
from django.http import HttpResponseForbidden

from .models import *

menu = [
        # {'title': "Dashboard", 'url_name': 'dashboard'},
        {'title': "Партнеры", 'url_name': 'partners'},
        {'title': "Пользователи", 'url_name': 'users'},
        # {'title': "Склад", 'url_name': 'warehouse'},
        # {'title': "CRM", 'url_name': 'crm'},
        ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        context['menu'] = user_menu
        return context


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper
