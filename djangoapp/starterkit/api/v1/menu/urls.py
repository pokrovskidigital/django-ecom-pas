from django.contrib import admin
from django.urls import path

from .views import MenuListView

urlpatterns = [
    path('<slug:sex__slug>/menu', MenuListView.as_view())
]
