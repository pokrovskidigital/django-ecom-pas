from django.shortcuts import render
from rest_framework.generics import ListAPIView
# Create your views here.
from rest_framework.pagination import PageNumberPagination

from .models import Product, Category
from .serializers import ProductsViewSerializer,CategoriesViewSeriazlizer
from rest_framework.permissions import AllowAny


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    lookup_field = ('pk',)
    queryset = Category.objects.all()
    serializer_class = CategoriesViewSeriazlizer
    permission_classes = (AllowAny,)


class ProductListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(leftovers__count__gt=0)
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'sex__slug'
