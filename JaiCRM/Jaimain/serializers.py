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

