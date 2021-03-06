from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductsSearchListApiView, CategoryListApiView, ProductApiView, OptionCategoryView, \
    CompilationListApiView, ProductsListApiView, BrandListView, ProductsBrandListApiView, OptionAllView, \
    OptionBrandAllView, BrandView, CompilationApiView, ProductByIdView, OptionCompilationAllView

urlpatterns = [
    path('<slug:compilation__slug>/options', OptionCompilationAllView.as_view()),
    path('search/products/', ProductsSearchListApiView.as_view()),
    path('compilations/<slug:slug>', CompilationApiView.as_view()),
    path('brands/', BrandListView.as_view()),
    path('brands/options/<slug:sex__slug>/<slug:brand__slug>/', OptionBrandAllView.as_view()),
    path('brands/<slug:slug>/', BrandView.as_view()),
    path('products/get_by_id/', ProductByIdView.as_view()),
    path('products/<slug:sex__slug>/<slug:brand__slug>/', ProductsBrandListApiView.as_view()),
    path('<slug:sex__slug>/all/options', OptionAllView.as_view()),
    path('<slug:sex__slug>/products/', ProductsListApiView.as_view()),
    path('<slug:sex__slug>/categories/', CategoryListApiView.as_view()),
    path('product/<int:pk>', ProductApiView.as_view()),
    path('<slug:sex__slug>/<int:category__id>/options', OptionCategoryView.as_view()),
    path('<slug:sex__slug>/compilations/', CompilationListApiView.as_view()),
]
