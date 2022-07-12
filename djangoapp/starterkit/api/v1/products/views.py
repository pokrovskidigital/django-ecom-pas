from django.shortcuts import render
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .models import Product, Category, Compilation, MainPage, Brand
from .serializers import ProductsViewSerializer, CategoriesViewSerializer, ProductViewSerializer, \
    CompilationsViewSerializer, MainPageViewSerializer, BrandSerializer, BrandViewSerializer
from rest_framework.permissions import AllowAny
import rest_framework.filters as f
from .services import ProductFilterSet, ProductSearchFilterSet


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
        return Product.objects.filter(sex__slug=self.kwargs['sex__slug'], leftovers__count__gt=0,
                                      leftovers__price__gt=0).distinct()


class ProductsSearchListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend, f.SearchFilter)
    filterset_class = ProductSearchFilterSet
    search_fields = ['@title', '@brand__title', '@color__title', '@description', '@sku']

    def get_queryset(self):
        return Product.objects.filter(leftovers__count__gt=0, leftovers__price__gt=0).distinct()


class ProductsBrandListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend, f.SearchFilter)
    filterset_class = ProductSearchFilterSet
    search_fields = ['@title', '@brand__title', '@color__title', '@description', '@sku']

    def get_queryset(self):
        return Product.objects.filter(brand__slug=self.kwargs['brand__slug'], sex__slug=self.kwargs['sex__slug'],
                                      leftovers__count__gt=0, leftovers__price__gt=0).distinct()


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
        options_dict = {'sizes': [], 'colors': [],
                        'max_price': 0, 'min_price': 0, "brands": []}

        try:
            category = Category.objects.get(pk=category__id)
            products = Product.objects.filter(sex__slug=sex__slug, leftovers__count__gt=0,
                                              category__id__in=category.get_descendants(include_self=True))
            for color in products.values_list('color__title', 'color__code_1c').distinct():
                if color not in options_dict['colors'] and color[0] is not None:
                    options_dict['colors'].append(color)
            for size in products.values_list('leftovers__parent_size__title').distinct():
                if size not in options_dict['sizes']:
                    options_dict['sizes'].append(size)
            for brand in products.values_list('brand__title', 'brand__slug').distinct():
                if brand not in options_dict['brands']:
                    options_dict['brands'].append(brand)
            options_dict['min_price'] = products.order_by('-price').first().price
            options_dict['max_price'] = products.order_by('price').first().price
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


class MainPageListApiView(ListAPIView):
    pagination_class = None
    serializer_class = MainPageViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        return MainPage.objects.filter(sex__slug=self.kwargs['sex__slug']).distinct()


class BrandListView(ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = BrandViewSerializer

    def get_queryset(self):
        return Brand.objects.filter(product__isnull=False).distinct()
