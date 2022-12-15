from django.db.models import *
from django.core.cache import cache
from .models import *

menu = [
        # {'title': "Dashboard", 'url_name': 'dashboard'},
        {'title': "Партнеры", 'url_name': 'partners'},
        # {'title': "Торговые точки", 'url_name': 'shops'},
        # {'title': "Склад", 'url_name': 'warehouse'},
        # {'title': "CRM", 'url_name': 'crm'},
        {'title': 'Добавить партнера', 'url_name': 'addpartner'}
        ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        context['menu'] = user_menu
        return context
