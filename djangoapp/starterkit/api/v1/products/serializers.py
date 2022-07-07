from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer


class SexCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Sex
        fields = "__all__"

    def create(self, validated_data):
        category = Sex.objects.update_or_create(
            slug=validated_data.get('slug', None),
            defaults=validated_data)
        return category


class SexSeriazlizer(ModelSerializer):
    class Meta:
        model = Sex
        fields = "__all__"


class ParentCategorySerializer(ModelSerializer):
    parent = PrimaryKeyRelatedField(queryset=Category.objects.all())
    sex = SexSeriazlizer()

    class Meta:
        model = Category
        fields = ('title', 'slug', 'id', 'parent', 'sex',)


class CategorySeriazlizer(ModelSerializer):
    parent = ParentCategorySerializer()
    sex = SexSeriazlizer()

    class Meta:
        model = Category
        fields = ('title', 'slug', 'pk', 'parent', 'sex',)


class CategoryCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        category = Category.objects.update_or_create(slug=validated_data.get('slug', None),
                                                     sex=validated_data.get('sex', None),
                                                     defaults=validated_data)
        return category


class SizeCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"

    def create(self, validated_data):
        size = Size.objects.update_or_create(slug=validated_data.get('slug', None), defaults=validated_data)
        return size


class ColorCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"

    def create(self, validated_data):
        try:
            color = Color.objects.get(slug=validated_data.get('slug', None))
            if validated_data['code_1c'] not in color.synonyms:
                color.synonyms += f"{validated_data['code_1c']}, "
                color.save()
        except:
            color = Color.objects.create(title=validated_data['title'], code_1c=validated_data['code_1c'],
                                         slug=validated_data['slug'])
        return color


class TagCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, validated_data):
        tag = Tag.objects.update_or_create(slug=validated_data.get('slug', None), defaults=validated_data)
        return tag[0]


class SizeCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"

    def create(self, validated_data):
        size = Size.objects.update_or_create(title=validated_data.get('title', None), defaults=validated_data)
        return size[0]


class SizeTypeCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = SizeType
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        size_type = SizeType.objects.update_or_create(slug=validated_data.get('slug', None), defaults=validated_data)
        return size_type[0]


class LeftoverCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Leftover
        fields = "__all__"


class BrandCreateSeriazlizer(ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class SeasonSeriazlizer(ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


class ProductCreateSeriazlizer(WritableNestedModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BrandSeriazlizer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ("title",
                  )


class VariantsSerializer(ModelSerializer):
    category = CategorySeriazlizer()
    brand = BrandSeriazlizer()

    class Meta:
        model = Product
        exclude = ('variants',)


class ImageViewSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_l', 'image_s', 'image_m')


class ProductsViewSerializer(ModelSerializer):
    # category = CategorySeriazlizer()
    brand = BrandSeriazlizer()
    image = ImageViewSerializer(many=True)

    # variants = VariantsSerializer(many=True)
    # sex = SexSeriazlizer()

    class Meta:
        model = Product
        fields = ('id', 'slug', 'title', 'price', 'brand', 'image')


class CategoriesViewSeriazlizer(ModelSerializer):
    # parent = ParentCategorySerializer()

    sex_slug = serializers.SlugField(read_only=True, source="sex.slug")

    class Meta:
        model = Category
        fields = ('title', 'slug', 'pk', 'sex_slug')
