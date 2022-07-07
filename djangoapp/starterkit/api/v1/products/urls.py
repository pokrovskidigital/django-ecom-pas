from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductsListApiView, CategoryListApiView, ProductApiView

urlpatterns = [
    path('<slug:sex__slug>/products/', ProductsListApiView.as_view()),
    path('<slug:sex__slug>/categories/', CategoryListApiView.as_view()),
    path('product/<int:pk>', ProductApiView.as_view())
]
