"""JaiCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Jaimain.views import *
from JaiCRM import settings
from JaiCRM.views import   custom_handler404, custom_handler403, custom_handler500
handler404 = custom_handler404
handler500 = custom_handler500
handler403 = custom_handler403

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('Jaimain.urls')),
    path('api/v1/propertylist/', PropertyAPIView.as_view()),
    path('api/v1/propertylist/<int:pk>/', PropertyAPIUpdate.as_view()),
    path('api/v1/partnerlist/', PartnerAPIView.as_view()),
    path('api/v1/shoplist/', ShopApiView.as_view()),
    path('api/v1/product_cats/', ProductCategoryAPIView.as_view()),
    path('api/v1/sales_report_export/', sales_report_export_api),
    path('api/v1/reports/', ReportsAPIView.as_view()),
    path('api/v1/product_in_stock/<int:pk>/', ProductInStockAPIView.as_view()),
    path('api/v1/sales_channel/', SaleChannelAPIView.as_view()),
    path('api/v1/payment_form/', PaymentFormAPIView.as_view()),
    path('api/v1/customer/<int:pk>/', CustomerAPIView.as_view()),
    path('api/v1/product_in_stock/', ProductInStockListAPIView.as_view()),
    path('api/v1/customers/', CustomerListAPIView.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
