from django.contrib import admin
from .models import Menu, Column, PromoBanner, Row, Slider, Slide, MainPage, ProductBlock, MobileShopping
from easy_select2 import select2_modelform

RowForm = select2_modelform(Row, attrs={'width': '250px'})


# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    list_display = ['label', 'sex_slug', 'sort_id']
    list_editable = ['sort_id']
    ordering = ['pk']
    list_filter = ['sex_slug']


admin.site.register(Menu, MenuAdmin)


class ColumnAdmin(admin.ModelAdmin):
    list_display = ['heading', 'sort_id', 'pk']
    list_editable = ['sort_id']
    ordering = ['pk']
    filter_horizontal = ("rows",)


admin.site.register(Column, ColumnAdmin)


class ProductBlockAdmin(admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['pk']
    filter_horizontal = ("products",)


admin.site.register(ProductBlock, ProductBlockAdmin)


class MobileShoppingAdmin(admin.ModelAdmin):
    list_display = ['heading', 'sort_id', 'pk']
    list_editable = ['sort_id']
    ordering = ['pk']


admin.site.register(MobileShopping, MobileShoppingAdmin)


class RowAdmin(admin.ModelAdmin):
    # list_display = ['heading', 'pk']
    # ordering = ['pk']
    form = RowForm


admin.site.register(Row, RowAdmin)


class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['pk']


admin.site.register(PromoBanner, PromoBannerAdmin)


class SliderAdmin(admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['pk']


admin.site.register(Slider, SliderAdmin)


class SlideAdmin(admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['pk']


admin.site.register(Slide, SlideAdmin)


class MainPageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sex']
    ordering = ['pk']
    filter_horizontal = ("compilations",)


admin.site.register(MainPage, MainPageAdmin)
