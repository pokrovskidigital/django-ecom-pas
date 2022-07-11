from django.db import models
from ..products.models import Category, Image, Sex, Brand
from mptt.models import TreeForeignKey

# Create your models here.
class Row(models.Model):
    heading = models.CharField(max_length=200, default='-')
    path = models.CharField(max_length=200, default='-')
    category = TreeForeignKey(Category, blank=True, on_delete=models.CASCADE, null=True, related_name='row')
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE, related_name='row')
    sort_id = models.PositiveIntegerField(default=0)


class Column(models.Model):
    heading = models.CharField(max_length=200, default='-')
    rows = models.ManyToManyField("Row", related_name='column')
    button_label = models.CharField(max_length=200, default='-')
    sort_id = models.PositiveIntegerField(default=0)


class Menu(models.Model):
    label = models.CharField(max_length=200, default='-')
    path = models.CharField(max_length=200, default='-')
    is_category = models.BooleanField(default=True)
    columns = models.ManyToManyField('Column', blank=True, null=True, related_name='menu')
    promo = models.ForeignKey("PromoBanner", on_delete=models.CASCADE, blank=True, null=True)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE, blank=True, null=True)

    def sex_slug(self):
        return self.sex.slug


class PromoBanner(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    heading = models.CharField(max_length=200, default='-')
    caption = models.CharField(max_length=200, default='-')
    button_label = models.CharField(max_length=200, default='-')
    path = models.CharField(max_length=200, default='-')
