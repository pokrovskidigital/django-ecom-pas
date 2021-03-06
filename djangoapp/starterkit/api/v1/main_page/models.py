from django.db import models
from ..products.models import Category, Image, Sex, Brand, Compilation, Product
from mptt.models import TreeForeignKey


# Create your models here.
class Row(models.Model):
    heading = models.CharField(max_length=200, default='-')
    path = models.CharField(max_length=200, default='-')
    category = TreeForeignKey(Category, blank=True, on_delete=models.CASCADE, null=True, related_name='row')
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE, related_name='row')
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return self.heading


class Column(models.Model):
    heading = models.CharField(max_length=200, default='-')
    rows = models.ManyToManyField("Row", related_name='column')
    button_label = models.CharField(max_length=200, default='-')
    button_path = models.CharField(max_length=200, default='-')

    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['my_order']


class Menu(models.Model):
    label = models.CharField(max_length=200, default='-')
    path = models.CharField(max_length=200, default='-')
    is_category = models.BooleanField(default=True)
    columns = models.ManyToManyField('Column', blank=True, null=True, related_name='main_page')
    promo = models.ForeignKey("PromoBanner", on_delete=models.CASCADE, blank=True, null=True)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE, blank=True, null=True)
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['my_order']

    def sex_slug(self):
        return self.sex.slug


class PromoBanner(models.Model):
    image = models.FileField('media/img/', null=True, max_length=200)
    heading = models.CharField(max_length=200, default='-')
    caption = models.CharField(max_length=200, default='-')
    button_label = models.CharField(max_length=200, default='-')
    path = models.CharField(max_length=200, default='-')

    def __str__(self):
        return self.heading


class Slider(models.Model):
    heading = models.CharField(max_length=200, default='-')
    slides = models.ManyToManyField('Slide', blank=True)

    def __str__(self):
        return self.heading


class Slide(models.Model):
    heading = models.CharField(max_length=200, default='-')
    image = models.FileField(upload_to="media/main_page/img/", blank=True, null=True)
    mobile_image = models.FileField(upload_to="media/main_page/mobile_img/", blank=True, null=True)
    link = models.URLField(max_length=200, default='-')
    link_text = models.CharField(max_length=200, default='-')
    description = models.TextField(default='', max_length=1000)
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return self.heading


BLOCK_TYPE = (('G', 'Galery'), ('B', 'Block'))


class ProductBlock(models.Model):
    heading = models.CharField(max_length=200, default='-')
    image = models.FileField(upload_to="media/main_page/img/", blank=True, null=True)
    subheading = models.CharField(max_length=200, default='-')
    description = models.TextField(blank=True, null=True, max_length=1000)
    link = models.URLField(max_length=200, blank=True, null=True,)
    link_text = models.CharField(max_length=200, blank=True, null=True,)
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )
    block_type = models.CharField(choices=BLOCK_TYPE, max_length=200, default=BLOCK_TYPE[1])
    products = models.ManyToManyField(Product, blank=True)

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return self.heading


class MobileShopping(models.Model):
    heading = models.CharField(max_length=200, default='-')
    image = models.FileField(upload_to="media/main_page/img/", blank=True, null=True)
    link = models.URLField(max_length=200, default='-')
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return self.heading


class MainPage(models.Model):
    compilations = models.ManyToManyField(Compilation, related_name='MainMenu')
    sex = models.ForeignKey(Sex, on_delete=models.PROTECT, null=True, blank=True)
    slider = models.ForeignKey('Slider', on_delete=models.PROTECT, null=True, blank=True)
    product_blocks = models.ManyToManyField('ProductBlock', blank=True, related_name='MainMenu')
    mobile_shopping_parts = models.ManyToManyField('MobileShopping', blank=True, related_name='MainMenu')

    def __str__(self):
        return self.sex.title
