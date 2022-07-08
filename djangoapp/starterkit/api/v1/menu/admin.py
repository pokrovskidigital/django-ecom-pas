from django.contrib import admin
from .models import Menu, Column, PromoBanner


# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    list_display = ['label', 'sex_slug']
    ordering = ['pk']


admin.site.register(Menu, MenuAdmin)


class ColumnAdmin(admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['pk']
    filter_horizontal = ("categories",)


admin.site.register(Column, ColumnAdmin)


class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ['heading', 'pk']
    ordering = ['pk']


admin.site.register(PromoBanner, PromoBannerAdmin)
