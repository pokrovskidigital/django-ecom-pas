from ..products.serializers import CategoriesMenuSerializer, BrandMenuSerializer
from .models import Column, Menu, PromoBanner, Row

from rest_framework import serializers


class RowSerializer(serializers.ModelSerializer):
    category = CategoriesMenuSerializer()
    brand = BrandMenuSerializer()

    class Meta:
        model = Row
        fields = '__all__'


class ColumnSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True)

    class Meta:
        model = Column
        fields = '__all__'


class PromoBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoBanner
        fields = '__all__'


class MenuViewSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True)
    promo = PromoBannerSerializer()

    class Meta:
        model = Menu
        exlude = ('sex',)
