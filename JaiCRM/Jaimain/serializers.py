from rest_framework import serializers
from Jaimain.models import *


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductProperty
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name']


class ProductCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Shop
        fields = '__all__'


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExport
        fields = '__all__'


class ProductInStockSerializer(serializers.ModelSerializer):
    get_sell_price = serializers.DecimalField(decimal_places=2, max_digits=11)

    class Meta:
        model = ProductInStock
        fields = '__all__'


class PaymentFormSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PaymentForm
        fields = '__all__'


class SalesChannelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SalesChannel
        fields = '__all__'
