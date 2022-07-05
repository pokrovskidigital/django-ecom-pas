from django.contrib import admin
from django.urls import path

from .models import Product
from .views import ProductListApiView

urlpatterns = [
    path('<slug:sex__slug>/products/all', ProductListApiView.as_view())
]
