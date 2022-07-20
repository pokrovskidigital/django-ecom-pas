from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Menu, MainPage
from .serializers import MenuViewSerializer, MainPageViewSerializer


class MenuListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MenuViewSerializer
    pagination_class = None

    def get_queryset(self):
        return Menu.objects.filter(sex__slug=self.kwargs['sex__slug'])


class MainPageListApiView(ListAPIView):
    pagination_class = None
    serializer_class = MainPageViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        return MainPage.objects.filter(sex__slug=self.kwargs['sex__slug']) \
            .prefetch_related('mobile_shopping_parts',
                              'product_blocks',
                              'compilations', 'product_blocks__products').select_related("sex", 'slider').distinct()
