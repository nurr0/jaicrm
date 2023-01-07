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
    path('users/search/', search_users, name='search_users'),
    path('shops/', ShowShops.as_view(), name='shops'),
    path('addshop/', add_shop, name='addshop'),
    path('shops/<int:shop_pk>', ShowShop.as_view(), name='showshop'),
    path('shops/<int:pk>/edit/', EditShop.as_view(), name='editshop'),
    path('add_prod_cat', add_product_category, name='addproductcategory'),
    path('product_categories/', ProductCategoriesList.as_view(), name='product_categories'),
    path('product_categories/<int:pk>/', edit_product_category, name='editproductcategory'),
    path('addproductproperty/', add_product_property, name='addproductproperty'),
    path('product_properties/', ProductPropertiesList.as_view(), name='product_properties'),
    path('product_properties/<int:pk>/', EditProductProperty.as_view(), name='editproductproperty'),
    path('add_sku/', add_sku, name='add_sku'),
    path('sku/', SKUList.as_view(), name='sku'),
    path('sku/<int:sku_pk>/', ShowSKU.as_view(), name='show_sku'),
    path('sku/<int:sku_pk>/edit/', edit_sku, name='edit_sku')
]
