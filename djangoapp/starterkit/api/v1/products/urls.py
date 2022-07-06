from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductListApiView, CategoryListApiView

urlpatterns = [
    path('products/all', ProductListApiView.as_view()),
    path('categories/all/<slug:sex__slug>', CategoryListApiView.as_view())
]
