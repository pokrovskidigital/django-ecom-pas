from django.shortcuts import render
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Menu
from .serializers import MenuViewSerializer


class MenuListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MenuViewSerializer
    pagination_class = None

    def get_queryset(self):
        return Menu.objects.filter(sex__slug=self.kwargs['sex__slug'])
