from django.contrib import admin
from .models import Menu, Column, PromoBanner, Row, Slider, Slide, MainPage, ProductBlock, MobileShopping
from easy_select2 import select2_modelform
from adminsortable2.admin import SortableAdminMixin

RowForm = select2_modelform(Row, attrs={'width': '250px'})


# Register your models here.
class MenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['label', 'sex_slug', 'sort_id']
    ordering = ['my_order']
    list_filter = ['sex']


admin.site.register(Menu, MenuAdmin)


class ColumnAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['heading', 'sort_id', 'pk']
    ordering = ['my_order']
    filter_horizontal = ("rows",)


admin.site.register(Column, ColumnAdmin)


class ProductBlockAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['my_order']
    filter_horizontal = ("products",)


admin.site.register(ProductBlock, ProductBlockAdmin)


class MobileShoppingAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['heading', 'sort_id', 'pk']
    ordering = ['my_order']


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


class SlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['pk']


admin.site.register(Slide, SlideAdmin)


class MainPageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sex']
    ordering = ['pk']
    filter_horizontal = ("compilations",)


admin.site.register(MainPage, MainPageAdmin)
