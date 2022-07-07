from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductListApiView, CategoryListApiView

urlpatterns = [
    path('<slug:sex__slug>/products/', ProductListApiView.as_view()),
    path('<slug:sex__slug>/categories/', CategoryListApiView.as_view())
]
