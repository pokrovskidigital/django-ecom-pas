from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductsListApiView, CategoryListApiView, ProductApiView, OptionCategoryView, CompilationListApiView

urlpatterns = [
    path('<slug:sex__slug>/products/', ProductsListApiView.as_view()),
    path('<slug:sex__slug>/categories/', CategoryListApiView.as_view()),
    path('product/<int:pk>', ProductApiView.as_view()),
    path('<slug:sex__slug>/<int:category__id>/options', OptionCategoryView.as_view()),
    path('compilations/', CompilationListApiView.as_view())
]
