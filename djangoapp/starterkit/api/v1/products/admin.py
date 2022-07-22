from django.contrib import admin
from .models import Product, Category, Tag, Size, Leftover, Sex, Season, Color, Brand, Image, Compilation, Baner

from mptt.admin import MPTTModelAdmin
from adminsortable2.admin import SortableAdminMixin


# Register your models here.
class CompilationsAdmin( admin.ModelAdmin, ):
    list_display = ['title', 'pk', 'sex']
    filter_horizontal = ("products", 'extra_images',)


admin.site.register(Compilation, CompilationsAdmin)


class BannerAdmin(SortableAdminMixin, admin.ModelAdmin, ):
    ordering = ['my_order']


admin.site.register(Baner, BannerAdmin)


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
    filter_horizontal = ("image", 'leftovers', 'similar_products', 'related_products', 'variants')
    search_fields = ['title', 'sku', 'slug']


admin.site.register(Product, ProductAdmin)


class LeftoverAdmin(admin.ModelAdmin):
    pass


admin.site.register(Leftover, LeftoverAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'id_1c']
    ordering = ['id_1c']
    search_fields = ['title', 'id_1c', 'slug']


admin.site.register(Brand, BrandAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)


class CategoryAdmin(SortableAdminMixin, MPTTModelAdmin):
    ordering = ['my_order']


admin.site.register(Category, CategoryAdmin)
