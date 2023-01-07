from django.contrib import admin
from .models import *
from django_mptt_admin.admin import DjangoMpttAdmin


class ProductCategoryAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Partner)
admin.site.register(JaiUser)
admin.site.register(Shop)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductProperty)
admin.site.register(ProductPropertyRelation)
admin.site.register(SKU)
