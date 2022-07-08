from ..products.serializers import CategoriesMenuSeriazlizer
from .models import Column, Menu, PromoBanner

from rest_framework import serializers


class ColumnSerializer(serializers.ModelSerializer):
    categories = CategoriesMenuSeriazlizer(many=True)

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
