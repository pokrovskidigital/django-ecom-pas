from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductsSearchListApiView, CategoryListApiView, ProductApiView, OptionCategoryView, \
    CompilationListApiView, \
    MainPageListApiView, ProductsListApiView

urlpatterns = [
    path('<slug:sex__slug>/products/', ProductsListApiView.as_view()),
    path('<slug:sex__slug>/categories/', CategoryListApiView.as_view()),
    path('product/<int:pk>', ProductApiView.as_view()),
    path('<slug:sex__slug>/<int:category__id>/options', OptionCategoryView.as_view()),
    path('<slug:sex__slug>/compilations/', CompilationListApiView.as_view()),
    path('<slug:sex__slug>/main_page/', MainPageListApiView.as_view()),
    path('search/products', ProductsListApiView.as_view()),
]
