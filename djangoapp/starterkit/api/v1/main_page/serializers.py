from ..products.serializers import CategoriesMenuSerializer, BrandMenuSerializer, SexSerializer, \
    CompilationsViewSerializer, ProductsViewSerializer, ProductBlockViewSerializer, CompilationsBlockViewSerializer
from .models import Column, Menu, PromoBanner, Row, MainPage, Slider, Slide, ProductBlock, MobileShopping

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


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'


class MobileShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileShopping
        fields = '__all__'


class SliderSerializer(serializers.ModelSerializer):
    slides = SlideSerializer(many=True)

    class Meta:
        model = Slider
        fields = '__all__'


class ProductBlockSerializer(serializers.ModelSerializer):
    products = ProductBlockViewSerializer(many=True)

    class Meta:
        model = ProductBlock
        fields = '__all__'


class MenuViewSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True)
    promo = PromoBannerSerializer()

    class Meta:
        model = Menu
        fields = '__all__'


class MainPageViewSerializer(serializers.ModelSerializer):
    sex = SexSerializer()
    compilations = CompilationsBlockViewSerializer(many=True)
    slider = SliderSerializer()
    product_blocks = ProductBlockSerializer(many=True)
    mobile_shopping_parts = MobileShoppingSerializer(many=True)

    class Meta:
        model = MainPage
        fields = "__all__"
