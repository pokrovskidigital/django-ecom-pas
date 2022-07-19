from django.contrib import admin
from django.urls import path

from .views import MenuListView, MainPageListApiView

urlpatterns = [
    path('<slug:sex__slug>/main_menu', MenuListView.as_view()),
    path('<slug:sex__slug>/main_page/', MainPageListApiView.as_view()),

]
