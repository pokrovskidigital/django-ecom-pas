from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from .utils import l_image_directory_path, m_image_directory_path, s_image_directory_path

IMAGE_TYPES = (
    ('P', 'Products'),
    ('C', 'Category'),
    ('B', 'Brands'),
    ('C', 'Compilation'),

)


# Create your models here.

class Image(models.Model):
    image_s = models.ImageField(
        upload_to='media/LARGE/', null=True, blank=True, max_length=1200)
    image_m = models.ImageField(
        upload_to='media/MEDIUM/', null=True, blank=True, max_length=1200)
    image_l = models.ImageField(
        upload_to='media/SMALL/', null=True, blank=True, max_length=1200)
    title = models.CharField(max_length=200, verbose_name="title")
    type = models.CharField(max_length=200, choices=IMAGE_TYPES, default=IMAGE_TYPES[0])

    def __str__(self):
        return self.title


class Category(MPTTModel):
    title = models.CharField(max_length=200, verbose_name="title")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    sort = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, unique=False, db_index=True, verbose_name="slug", default="-")
    id_1c = models.CharField(max_length=200, unique=False, null=True, blank=True)
    image = models.ForeignKey('Image', on_delete=models.PROTECT, null=True, blank=True, )
    sex = models.ForeignKey('Sex', on_delete=models.PROTECT, null=True, blank=True, related_name='sex')
    sort = models.IntegerField(default=0)
    description = models.TextField(default='', max_length=1000)

    class MPTTMeta:
        order_insertion_by = ['title']

    class META:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title + ' ' + self.sex.title


class Leftover(models.Model):
    parent_size = models.ForeignKey('Size', on_delete=models.PROTECT, null=True, blank=True, )
    count = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return str(self.count)


class Sex(models.Model):
    slug = models.SlugField(max_length=250, unique=False, db_index=True, verbose_name="slug", default="-")
    title = models.CharField(max_length=200, verbose_name="title")

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    slug = models.SlugField(max_length=250, unique=False, db_index=True, null=True, verbose_name="slug", default="-")

    def __str__(self):
        return self.title


class Color(models.Model):
    slug = models.SlugField(max_length=250, unique=False, db_index=True, verbose_name="slug", default="-")
    title = models.CharField(max_length=200, verbose_name="title")
    code_1c = models.CharField(max_length=200, verbose_name="code_1c")
    synonyms = models.CharField(max_length=900, verbose_name="synonyms", blank=True, null=True, default=' ')

    def __str__(self):
        return self.title


class Brand(models.Model):
    id_1c = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="slug", default="-")
    title = models.CharField(max_length=200, verbose_name="title", null=True, blank=True, )
    description = models.TextField(default='', max_length=1000, null=True, blank=True, )
    icon = models.ForeignKey('Image', on_delete=models.PROTECT, null=True, blank=True, related_name='brand_icon')
    image = models.ForeignKey('Image', on_delete=models.PROTECT, null=True, blank=True, related_name='brand_image')
    sex = models.ForeignKey('Sex', on_delete=models.PROTECT, default=31, blank=True)

    def __str__(self):
        return self.title + ' ' + self.id_1c


class Season(models.Model):
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="slug", default="-")
    title = models.CharField(max_length=200, verbose_name="title")
    id_1c = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    parent_category = TreeForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True, related_name="size")
    type = models.ForeignKey('SizeType', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="title"
    )
    sku = models.CharField(
        max_length=200,
        verbose_name="sku"
    )
    sex = models.ForeignKey(
        'Sex',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    category = TreeForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="product"
    )
    image = models.ManyToManyField(
        'Image',
        null=True,
        blank=True,
        related_name="product"
    )
    slug = models.SlugField(
        max_length=250,
        unique=False,
        db_index=True,
        verbose_name="slug",
        default="-"
    )
    description = models.TextField(default='', max_length=1000)
    tags = models.ManyToManyField('Tag', blank=True)
    leftovers = models.ManyToManyField('Leftover', blank=True, null=True,
                                       related_name="product")
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, null=True, blank=True, )
    collection = models.CharField(max_length=200, verbose_name="collection", blank=True, null=True)
    fashion_collection = models.CharField(max_length=200, verbose_name="fashion_collection", blank=True, null=True)
    season = models.ForeignKey('Season', on_delete=models.PROTECT, null=True, blank=True, related_name="product")
    color = models.ForeignKey('Color', on_delete=models.PROTECT, null=True, blank=True, related_name="product")
    price = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    related_products = models.ManyToManyField('self', null=True, blank=True)
    similar_products = models.ManyToManyField('self', null=True, blank=True)
    variants = models.ManyToManyField('self', null=True, blank=True)
    sort = models.IntegerField(default=0)
    id_1c = models.CharField(max_length=200, unique=False)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Create time ')
    update_by_1c_time = models.DateTimeField(auto_now=True, verbose_name='Update Time')
    detailed_description = models.TextField(default='', max_length=2000)
    weight = models.CharField(max_length=200, verbose_name="weight", null=True, blank=True)
    width = models.CharField(max_length=200, verbose_name="width", null=True, blank=True)
    height = models.CharField(max_length=200, verbose_name="height", null=True, blank=True)
    volume = models.CharField(max_length=200, verbose_name="volume", null=True, blank=True)
    popularity = models.IntegerField(default=0)
    labels = models.ManyToManyField('Labels', null=True, blank=True)
    options = models.ManyToManyField('Options', null=True, blank=True)

    @property
    def discount_price(self):
        return self.price - (self.price * 0.01 * self.discount)

    def __str__(self):
        if self.color is not None:
            return self.title + " " + self.brand.title + " " + self.sku + ' ' + self.color.title
        else:
            return self.title + " " + self.brand.title + " " + self.sku


class Labels(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="slug", default="-")
    color = models.ForeignKey('Color', on_delete=models.PROTECT, null=True, blank=True)
    sort = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class SizeType(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")

    def __str__(self):
        return self.title


class Options(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    parent_category = TreeForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True,
                                     related_name="options")
    value = models.CharField(max_length=200, verbose_name="Значение")


class Compilation(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    subtitle = models.CharField(max_length=200, verbose_name="subtitle")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="slug", default="-")
    sex = models.ForeignKey('Sex', on_delete=models.PROTECT, default=31, blank=True)
    text = models.TextField(max_length=1000, verbose_name="text")
    title_image = models.ForeignKey('Image', on_delete=models.PROTECT, null=True, blank=True)
    products = models.ManyToManyField('Product', null=True, blank=True, related_name="Compilations")
    extra_images = models.ManyToManyField('Image', null=True, blank=True, related_name="Compilations")

    def __str__(self):
        return self.title + ' ' + self.sex.title


class MainPage(models.Model):
    compilations = models.ManyToManyField('Compilation', related_name='MainMenu')
    sex = models.ForeignKey('Sex', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.sex.title
