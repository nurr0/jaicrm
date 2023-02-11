from django.contrib import admin
from .models import *
from django_mptt_admin.admin import DjangoMpttAdmin
from import_export import resources


class ProductCategoryAdmin(DjangoMpttAdmin):
    pass



admin.site.register(Partner)
admin.site.register(JaiUser)
admin.site.register(Shop)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductProperty)
admin.site.register(ProductPropertyRelation)
admin.site.register(SKU)
admin.site.register(SellReceipt)
admin.site.register(BaseLoyaltySystem)
admin.site.register(Customer)
admin.site.register(PaymentForm)
admin.site.register(SalesChannel)
admin.site.register(Points)
admin.site.register(ProductsRemove)
admin.site.register(ProductInStock)
admin.site.register(ProductsInSupply)
admin.site.register(ProductInReceipt)
admin.site.register(SellPrice)
