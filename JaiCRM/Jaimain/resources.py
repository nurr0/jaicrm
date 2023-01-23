from django.contrib.auth.models import User
from import_export import resources
from import_export.fields import Field

from .models import SellReceipt, ProductInReceipt, JaiUser


class SalesResource(resources.ModelResource):
    datetime_created = Field(attribute='receipt__time_created', column_name='Дата создания')
    shop = Field(attribute='receipt__shop__name', column_name='Торговая точка')
    document = Field(attribute='receipt__partner__receipt_prefix', column_name='Наименование документа')
    doc_number = Field(attribute='receipt__number', column_name='№ документа')
    product = Field(attribute='product__product__name', column_name='Товар')
    product_idintifier = Field(attribute='product__product__identifier', column_name='Артикул')
    amount = Field(attribute='amount', column_name='Количество')
    price_in_stock = Field(attribute='price_in_stock', column_name='Установленная цена')
    discount = Field(attribute='discount', column_name='Скидка')
    price_with_discount = Field(attribute='price_with_discount', column_name='Цена со скидкой')
    is_returned = Field(attribute='receipt__is_returned', column_name='Возврат')
    total_price = Field(attribute='get_total_cost_with_discount', column_name='Общая стоимость')


    def __init__(self, *args, **kwargs):
        super(SalesResource, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(receipt__partner=self.user.partner)

    class Meta:
        model = ProductInReceipt
        exclude = ('id', 'receipt')
        widgets = {
                'receipt__time_created': {'format': '%d.%m.%Y'},
                }

