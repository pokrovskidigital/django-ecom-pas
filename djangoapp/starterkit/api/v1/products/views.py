from django.shortcuts import render
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .models import Product, Category
from .serializers import ProductsViewSerializer, CategoriesViewSeriazlizer, ProductViewSerializer
from rest_framework.permissions import AllowAny

from .services import ProductFilterset


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryListApiView(ListAPIView):
    pagination_class = None
    serializer_class = CategoriesViewSeriazlizer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.filter(sex__slug=self.kwargs['sex__slug'])


class ProductsListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(leftovers__count__gt=0)
    serializer_class = ProductsViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilterset

    def get_queryset(self):
        return Product.objects.filter(sex__slug=self.kwargs['sex__slug'], leftovers__count__gt=0)


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

    def get(self, request):
        return Response(request)
