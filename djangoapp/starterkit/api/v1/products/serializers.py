from django.db.models import Q
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer


class SexCreateSerializer(ModelSerializer):
    class Meta:
        model = Sex
        fields = "__all__"

    def create(self, validated_data):
        category = Sex.objects.update_or_create(
            slug=validated_data.get('slug', None),
            defaults=validated_data)
        return category


class SexSerializer(ModelSerializer):
    class Meta:
        model = Sex
        fields = "__all__"


class ParentCategorySerializer(ModelSerializer):
    parent = PrimaryKeyRelatedField(queryset=Category.objects.all())
    sex = SexSerializer()

    class Meta:
        model = Category
        fields = ('title', 'slug', 'id', 'parent', 'sex',)


class CategorySerializer(ModelSerializer):
    parent = ParentCategorySerializer()
    sex = SexSerializer()

    class Meta:
        model = Category
        fields = ('title', 'slug', 'pk', 'parent', 'sex',)


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        category = Category.objects.update_or_create(slug=validated_data.get('slug', None),
                                                     sex=validated_data.get('sex', None),
                                                     defaults=validated_data)
        return category


class CategorySearchSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug',)


class SizeCreateSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"

    def create(self, validated_data):
        size = Size.objects.update_or_create(title=validated_data.get('title', None), defaults=validated_data)
        return size


class ColorCreateSerializer(ModelSerializer):
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


class TagCreateSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, validated_data):
        tag = Tag.objects.update_or_create(slug=validated_data.get('slug', None), defaults=validated_data)
        return tag[0]


class SizeTypeCreateSerializer(ModelSerializer):
    class Meta:
        model = SizeType
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        size_type = SizeType.objects.update_or_create(slug=validated_data.get('slug', None), defaults=validated_data)
        return size_type[0]


class LeftoverCreateSerializer(ModelSerializer):
    class Meta:
        model = Leftover
        fields = "__all__"


class BrandCreateSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


class ProductCreateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ("title",
                  )


class BrandListViewSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ("title", 'slug', 'icon'
                  )


class BrandViewSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ImageViewSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_l', 'image_s', 'image_m')


class LeftoverViewSerializer(ModelSerializer):
    size_title = serializers.CharField(read_only=True, source='parent_size.title')

    class Meta:
        model = Leftover
        fields = ('size_title', 'count',)


class CategoriesViewSerializer(ModelSerializer):
    parent = SerializerMethodField()

    sex_slug = serializers.SlugField(read_only=True, source="sex.slug")

    class Meta:
        model = Category
        fields = ('title', 'slug', 'pk', 'sex_slug', 'parent')

    def get_parent(self, obj):
        if obj.parent is not None:
            print(obj.parent)
            return CategoriesViewSerializer(obj.parent).data
        else:
            print('none')

            return None


class CategoriesMenuSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug',)


class BrandMenuSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('title', 'slug',)


class BrandSearchSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('title', 'slug', 'icon')


class ColorViewSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ('title', 'code_1c')


class VariantsSerializer(ModelSerializer):
    color = ColorViewSerializer()
    image = ImageViewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('pk', "color", 'title', 'slug', 'image')


class ProductsViewSerializer(ModelSerializer):
    # category = CategorySeriazlizer()
    brand = BrandSerializer()
    image = ImageViewSerializer(many=True)
    # size_title = serializers.CharField(read_only=True, source='leftovers.parent_size.title')
    leftovers = LeftoverViewSerializer(many=True)
    sex = SexSerializer()

    class Meta:
        model = Product
        fields = ('id', 'slug', 'title', 'price', 'brand', 'image', 'leftovers', 'description', 'sex', 'search_string')


class ProductsSearchSerializer(ModelSerializer):
    brand = BrandSerializer()
    image = ImageViewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'slug', 'title', 'price', 'brand', 'image',)


class ProductBlockViewSerializer(ModelSerializer):
    brand = BrandSerializer()
    image = ImageViewSerializer(many=True)
    leftovers = LeftoverViewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'brand', 'image', 'leftovers', 'sku')


class ProductViewSerializer(ModelSerializer):
    category = CategoriesViewSerializer()
    brand = BrandListViewSerializer()
    image = ImageViewSerializer(many=True)
    leftovers = LeftoverViewSerializer(many=True)
    sex = SexSerializer()
    similar_products = ProductsViewSerializer(many=True)

    color = ColorViewSerializer()
    variants = VariantsSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'slug', 'title', 'price', 'brand',
            'image', 'leftovers', 'color', 'sex', 'category',
            'variants', 'sku', 'description', 'similar_products', 'detailed_description')


class CompilationsViewSerializer(ModelSerializer):
    title_image = ImageViewSerializer()
    extra_images = ImageViewSerializer(many=True)
    products = ProductViewSerializer(many=True)

    class Meta:
        model = Compilation
        fields = "__all__"


class CompilationsBlockViewSerializer(ModelSerializer):
    title_image = ImageViewSerializer()
    products = ProductBlockViewSerializer(many=True)

    class Meta:
        model = Compilation
        fields = "__all__"


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Baner
        fields = '__all__'
