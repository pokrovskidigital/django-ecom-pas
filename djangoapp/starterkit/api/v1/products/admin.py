from django.contrib import admin
from .models import Product, Category, Tag, Size, Leftover, Sex, Season, Color, Brand, Image, Compilation, MainMenu
from mptt.admin import MPTTModelAdmin


class MainMenuAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sex']
    ordering = ['pk']
    filter_horizontal = ("compilations",)


admin.site.register(MainMenu, MainMenuAdmin)


# Register your models here.
class CompilationsAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk', 'sex']
    ordering = ['pk']
    filter_horizontal = ("products", 'extra_images',)


admin.site.register(Compilation, CompilationsAdmin)


class SexAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk']
    ordering = ['pk']


admin.site.register(Sex, SexAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk']
    ordering = ['pk']


admin.site.register(Color, ColorAdmin)


class SeasonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Season, SeasonAdmin)


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)


class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ("image", 'leftovers', 'related_products', 'variants')
    list_display = ('pk', 'title')


admin.site.register(Product, ProductAdmin)


class LeftoverAdmin(admin.ModelAdmin):
    pass


admin.site.register(Leftover, LeftoverAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'id_1c']
    ordering = ['id_1c']


admin.site.register(Brand, BrandAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)


class CategoryAdmin(MPTTModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
