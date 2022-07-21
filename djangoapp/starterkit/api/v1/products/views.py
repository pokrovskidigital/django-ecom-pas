import re

from django.contrib.postgres.search import TrigramWordSimilarity, TrigramWordDistance
from django.shortcuts import render
from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework import mixins

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .models import Product, Category, Compilation, Brand
from .serializers import ProductsViewSerializer, CategoriesViewSerializer, ProductViewSerializer, \
    CompilationsViewSerializer, BrandSerializer, BrandListViewSerializer, BrandViewSerializer, CategorySearchSerializer
from rest_framework.permissions import AllowAny
import rest_framework.filters as f
from .services import ProductFilterSet, ProductSearchFilterSet

replaced_words = [' без ', ' в ', ' для ', ' за ', ' из ', ' к ', ' между ', ' на ', ' по ', ' при ', ' с ',
                  ' у ', ' под ', 'без ', 'в ', 'для ', 'за ', 'из ', 'к ', 'между ', 'на ', 'по ', 'при ',
                  'с ',
                  'у ', 'под ', ]


def get_options(products):
    cat_list = []
    options_dict = {'size': [], 'color': [],
                    'max_price': 0, 'min_price': 0, "brand": [], 'categories': []}
    for color in products.values_list('color__title', 'color__code_1c').distinct():
        if color not in options_dict['color'] and color[0] is not None:
            options_dict['color'].append(color)
    for size in products.values_list('leftovers__parent_size__title').distinct():
        if size not in options_dict['size']:
            options_dict['size'].append(size)
    for brand in products.values_list('brand__title', 'brand__slug').distinct():
        if brand not in options_dict['brand']:
            options_dict['brand'].append(brand)
    cats = products.values_list('category').distinct()
    print(cats)
    for cat in cats:
        cat_list.append(cat[0])
    categoties = Category.objects.filter(pk__in=cat_list)
    print(categoties)
    category_data = CategoriesViewSerializer(categoties, many=True).data
    options_dict['min_price'] = products.order_by('-price').first().price
    options_dict['max_price'] = products.order_by('price').first().price
    options_dict['categories'] = category_data
    return options_dict


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryListApiView(ListAPIView):
    pagination_class = None
    serializer_class = CategoriesViewSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.filter(sex__slug=self.kwargs['sex__slug']).distinct()


class ProductsListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend, f.SearchFilter)
    filterset_class = ProductFilterSet
    search_fields = ['@title', '@brand__title', '@color__title', '@description', ]

    def get_queryset(self):
        print(self.request.query_params)
        if "sort_by" in self.request.query_params.keys():
            return Product.objects.filter(sex__slug=self.kwargs['sex__slug'], leftovers__count__gt=0,
                                          leftovers__price__gt=0).order_by(
                self.request.query_params['sort_by']).distinct()
        return Product.objects.filter(sex__slug=self.kwargs['sex__slug'], leftovers__count__gt=0,
                                      leftovers__price__gt=0).distinct()


class ProductsSearchListApiView(mixins.ListModelMixin, GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)

    # def list_categories(self, request, *args, **kwargs):

    def list(self, request, *args, **kwargs):
        resp_data = {
            'categories': [],
            'products': []
        }
        queryset = self.filter_queryset(self.get_queryset())
        category_queryset = self.get_queryset_category()
        serializer = self.get_serializer(queryset, many=True)
        cat_serializer = CategorySearchSerializer(category_queryset, many=True)
        resp_data['products'] = serializer.data['results']
        resp_data['products'] = serializer.data
        # resp_data[]
        resp_data['categories'] = cat_serializer.data
        return Response(resp_data)

    def post(self, request, *args, **kwargs):
        return self.list(request)

    def get_queryset(self):
        if 'search' in self.request.data.keys():
            prods = Product.objects.all()
            k = 0.5
            query_string = self.request.data['search']
            for r in replaced_words:
                query_string = query_string.replace(r, ' ')
            query_string = list(filter(lambda x: x != "", query_string.split(' ')))
            for search_query_word in query_string:
                # print(search_query_word)
                prods = prods.filter(
                    leftovers__count__gt=0,
                    leftovers__price__gt=0, sex__slug=self.request.data['sex']).annotate(
                    similarity=TrigramWordSimilarity(search_query_word, 'search_string')).filter(
                    similarity__gt=k).order_by('-similarity').distinct()
                k -= 0.1
            return prods

        return Product.objects.filter(leftovers__count__gt=0, leftovers__price__gt=0).distinct()

    def get_queryset_category(self):
        if 'search' in self.request.data.keys():
            categories_query = Category.objects.all()
            k = 0.5
            query_string = self.request.data['search']
            for r in replaced_words:
                query_string = query_string.replace(r, ' ')
            query_string = list(filter(lambda x: x != "", query_string.split(' ')))
            for search_query_word in query_string:
                # print(search_query_word)
                categories_query = categories_query.filter(sex__slug=self.request.data['sex']).annotate(
                    similarity=TrigramWordSimilarity(search_query_word, 'title')).filter(
                    similarity__gt=k).order_by('-similarity').distinct()
                k -= 0.1
            return categories_query

        return Category.objects.all()


class ProductsBrandListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend, f.SearchFilter)
    filterset_class = ProductSearchFilterSet
    search_fields = ['@title', '@brand__title', '@color__title', '@description', '@sku']

    def get_queryset(self):
        return Product.objects.filter(brand__slug=self.kwargs['brand__slug'], sex__slug=self.kwargs['sex__slug'],
                                      leftovers__count__gt=0, leftovers__price__gt=0, image__isnull=False).distinct()


class ProductApiView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductViewSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OptionCategoryView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, sex__slug, category__id):
        options_dict = []
        try:
            category = Category.objects.get(pk=category__id)
            products = Product.objects.filter(sex__slug=sex__slug, leftovers__count__gt=0,
                                              category__id__in=category.get_descendants(include_self=True))
            options_dict = get_options(products)
        except:
            pass
        return Response(options_dict)


class OptionAllView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, sex__slug):
        options_dict = []

        try:
            products = Product.objects.filter(sex__slug=sex__slug, leftovers__count__gt=0)
            options_dict = get_options(products)
        except:
            pass
        return Response(options_dict)


class CompilationListApiView(ListAPIView):
    pagination_class = None
    serializer_class = CompilationsViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        return Compilation.objects.filter(sex__slug=self.kwargs['sex__slug']).distinct()


class CompilationApiView(GenericAPIView):
    queryset = Compilation.objects.all()
    serializer_class = CompilationsViewSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)
    lookup_field = 'slug'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductSearchFilterSet

    def get_object(self):
        queryset = self.get_queryset()

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def paginate_queryset(self, queryset):
        # print(queryset)
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        ser_prods = self.filter_queryset(instance.products.all())
        page = self.paginate_queryset(ser_prods)
        if page is not None:
            serializer = ProductViewSerializer(page, many=True)
            ser_prods = serializer.data

        serializer = self.get_serializer(instance)
        ser_data = serializer.data
        ser_data['products'] = ser_prods
        return Response(ser_data)


class BrandListView(ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = BrandListViewSerializer

    def get_queryset(self):
        return Brand.objects.filter(product__isnull=False).distinct()


class BrandView(GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandViewSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BrandCategoryListView(ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CategoriesViewSerializer

    def get_queryset(self):
        return Category.objects.filter(product__isnull=False,
                                       product__brand__slug=self.kwargs['brand__slug']).distinct()


class OptionBrandAllView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, sex__slug, brand__slug):
        options_dict = []

        try:
            products = Product.objects.filter(sex__slug=sex__slug, leftovers__count__gt=0, brand__slug=brand__slug)
            options_dict = get_options(products)
        except:
            pass
        return Response(options_dict)


class OptionCompilationAllView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, compilation__slug):
        options_dict = []

        # try:
        compilation = Compilation.objects.get(slug__icontains=compilation__slug)
        options_dict = get_options(compilation.products.all())
        # except:
        #     pass
        return Response(options_dict)


class ProductByIdView(mixins.ListModelMixin, GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.list(request)

    def get_queryset(self):
        return Product.objects.filter(leftovers__count__gt=0, leftovers__price__gt=0,
                                      pk__in=self.request.data['id_list']).distinct()
