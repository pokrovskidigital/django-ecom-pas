from django.db import models
from ..products.models import Category, Image, Sex


# Create your models here.


class Column(models.Model):
    heading = models.CharField(max_length=200, default='-')
    categories = models.ManyToManyField(Category, blank=True, null=True, related_name='column')
    button_label = models.CharField(max_length=200, default='-')


class Menu(models.Model):
    label = models.CharField(max_length=200, default='-')
    path = models.CharField(max_length=200, default='-')
    is_category_caetgory = models.BooleanField(default=True)
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
