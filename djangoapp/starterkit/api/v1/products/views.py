from django.shortcuts import render
from rest_framework.generics import ListAPIView
# Create your views here.
from rest_framework.pagination import PageNumberPagination

from .models import Product
from .serializers import ProductViewSerializer
from rest_framework.permissions import AllowAny


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductListApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(leftovers__count__gt=0)
    serializer_class = ProductViewSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'sex__slug'