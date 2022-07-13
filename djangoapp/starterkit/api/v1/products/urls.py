from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductsSearchListApiView, CategoryListApiView, ProductApiView, OptionCategoryView, \
    CompilationListApiView, \
    MainPageListApiView, ProductsListApiView, BrandListView, ProductsBrandListApiView, OptionAllView, \
    OptionBrandAllView, BrandView

urlpatterns = [
    path('search/products/', ProductsSearchListApiView.as_view()),
    path('brands/', BrandListView.as_view()),
    path('brands/options/<slug:sex__slug>/<slug:brand__slug>/', OptionBrandAllView.as_view()),
    path('brands/<slug:slug>/', BrandView.as_view()),
    path('products/<slug:sex__slug>/<slug:brand__slug>/', ProductsBrandListApiView.as_view()),
    path('<slug:sex__slug>/all/options', OptionAllView.as_view()),
    path('<slug:sex__slug>/products/', ProductsListApiView.as_view()),
    path('<slug:sex__slug>/categories/', CategoryListApiView.as_view()),
    path('product/<int:pk>', ProductApiView.as_view()),
    path('<slug:sex__slug>/<int:category__id>/options', OptionCategoryView.as_view()),
    path('<slug:sex__slug>/compilations/', CompilationListApiView.as_view()),
    path('<slug:sex__slug>/main_page/', MainPageListApiView.as_view()),
]
