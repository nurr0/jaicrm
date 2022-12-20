from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', HomePage, name='home'),
    path('partners/', Partners.as_view(), name='partners'),
    path('addpartner/', AddPartner.as_view(), name='addpartner'),
    path('partners/<int:partner_pk>/', ShowPartner.as_view(), name='partner'),
    path('partners/<int:pk>/edit/', EditPartner.as_view(), name='editpartner'),
    path('partners/search/', search_partners, name='search'),
    path('users/', UsersList.as_view(), name='users'),
    path('users/<int:jaiuser_pk>', ShowUser.as_view(), name='showuser'),
    path('users/<int:pk>/edit/', EditUser.as_view(), name='edituser'),
    path('registeruser/', RegisterUser.as_view(), name='registeruser'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
