import json

import pymssql
from slugify import slugify

from ..models import Size, Leftover, Tag, Color, Sex, Category, Product, Brand, Image
from ..serializers import CategoryCreateSerializer, SexCreateSerializer, BrandCreateSerializer, \
    ProductCreateSerializer, TagCreateSerializer
from .parser_test import parse_offers
from progress.bar import *
from django.conf import settings

def clear_all():
    Image.objects.all().delete()
    # Product.objects.all().delete()
    # Category.objects.all().delete()
    # Sex.objects.all().delete()
    # Color.objects.all().delete()
    # Tag.objects.all().delete()
    # Brand.objects.all().delete()
    # Leftover.objects.all().delete()
    # Size.objects.all().delete()


class DBParser():
    remote_db_host = '192.168.7.40'
    remote_db_database_name = 'inout_demo'
    remote_db_login = 'webdev'
    remote_db_password = 'wB95Dv34%'
    cursor = None
    conn = None
    sex_data = []

    def connect(self):
        print('Trying connect...')
        self.conn = pymssql.connect(self.remote_db_host, self.remote_db_login, self.remote_db_password,
                                    self.remote_db_database_name)
        self.cursor = self.conn.cursor(as_dict=True)

        print('Connect successful')

    def fetch_all_products(self):
        self.cursor.execute('SELECT * FROM [iShop].[Articles] ORDER BY [Article_Id];')
        rows = self.cursor.fetchall()
        return rows

    def __init__(self):
        self.connect()

    def close(self):
        self.conn.close()

    def parse_sex(self):
        rows = self.fetch_all_products()
        sex = []
        sex_objects = []
        print('Start parse sex...')
        for row in rows:
            if not row['Gender'] in sex:
                sex.append(row['Gender'])
        bar = IncrementalBar('Countdown', max=len(sex))
        for s in sex:
            ser = SexCreateSerializer(data={'title': s, 'slug': slugify(s)})
            ser.is_valid()
            sex_object = ser.save()
            sex_objects.append(sex_object[0])
            bar.next()
        bar.finish()
        return sex_objects

    def parse_categories(self):
        self.cursor.execute('SELECT * FROM [iShop].[Categories] ORDER BY [Sort];')
        rows = self.cursor.fetchall()
        self.sex_data = self.parse_sex()
        print('Start parse categories...')
        bar = IncrementalBar('Countdown', max=len(rows))
        for row in rows:
            for sex in self.sex_data:
                category = {
                    'slug': row['Category_Id'],
                    'sort': row['Sort'],
                    'title': row['Name'],
                    'sex': sex.pk,
                }
                ser = CategoryCreateSerializer(data=category)
                ser.is_valid()
                data = ser.create(ser.validated_data)
                data[0].pk
            bar.next()
        bar.finish()
        return rows

    def parse_subcategory(self):
        self.cursor.execute('SELECT * FROM [iShop].[SubCategories] ORDER BY [Sort];')
        rows = self.cursor.fetchall()
        print('Start parse subcategories...')
        bar = IncrementalBar('Countdown', max=len(rows))

        for row in rows:
            for sex in self.sex_data:
                # try:
                if row['SubCategory_Id'] == "BZ0000000000001":
                    parent_category = None
                else:
                    self.cursor.execute(
                        f"SELECT * FROM [iShop].[CategoriesRelations] WHERE [SubCategory_Id]='{row['SubCategory_Id']}';")
                    car_rel_row = self.cursor.fetchall()
                    parent_category = Category.objects.filter(slug=car_rel_row[0]['Category_Id'], sex__pk=sex.pk)[0].pk

                sub_category = {
                    'slug': row['SubCategory_Id'],
                    'sort': row['Sort'],
                    'title': row['Name'],
                    'sex': sex.pk,
                    'parent': parent_category
                }
                ser = CategoryCreateSerializer(data=sub_category)
                ser.is_valid(raise_exception=True)
                data = ser.create(ser.validated_data)
            bar.next()
        bar.finish()
        return rows

    def parse_brands(self):
        brands = {'brands': []}
        self.cursor.execute('SELECT * FROM [iShop].[Trademarks] ORDER BY [Trademark_Id];')
        rows = self.cursor.fetchall()
        print('Start parse brand...')
        bar = IncrementalBar('Countdown', max=len(rows))

        for row in rows:
            brand = {
                'id_1c': row['Trademark_Id'],
                "title": row['Name'],
                'slug': slugify(row['Name'])
            }
            brands["brands"].append(brand)
            try:
                ser = BrandCreateSerializer(data=brand)
                ser.is_valid()
                ser.save()
            except:
                pass
            bar.next()
        bar.finish()

    def parse_photos(self):
        self.cursor.execute('SELECT * FROM [iShop].[Pictures] ORDER BY [Angle_id];')
        rows = self.cursor.fetchall()

    def parse_products(self, ):
        product_sku = []
        rows = self.fetch_all_products()
        count = 0
        print('Start parse products...')
        bar = IncrementalBar('Countdown', max=len(rows))
        for row in rows:
            try:
                brand = Brand.objects.filter(id_1c=row['Trademark_Id'])[0]
            except:
                brand = None
            sex = Sex.objects.filter(title=row['Gender'])[0]
            category = Category.objects.filter(slug=row['SubCategory_Id'], sex=sex)[0]
            if not brand or 'MaxMara' in brand.title or brand.title == "Brunello Cucinelli" or brand.title == "Kiton":
                continue
            else:
                product = {
                    'title': row['Name'],
                    'id_1c': row['Article_Id'],
                    'brand': brand.pk,
                    'sku': row['Article'],
                    'sex': sex.pk,
                    'category': category.pk,
                    'slug': slugify(row['Name'] + " " + brand.title + ' ' + row['Article_Id'])
                }
                ser = ProductCreateSerializer(data=product)
                ser.is_valid(raise_exception=True)
                prod = ser.save()
                product_sku.append(prod.sku)
            count += 1
            bar.next()
            if count > 2000:
                break
        bar.finish()

        offers = parse_offers(product_sku)
        print('Start compare offers with product...')
        bar = IncrementalBar('Countdown', max=len(offers))

        for offer in offers:
            prod = Product.objects.filter(sku=offer['sku'])[0]
            print(offer['color'])
            if prod is not None:
                if not prod.color:
                    if offer['color'] is not None:
                        prod.color = Color.objects.get(pk=offer['color'])
                        prod.save()
                if prod.color is None and offer['color'] is None:
                    prod.price = offer['price']
                    prod.leftovers.add(*offer['leftover'])
                    prod.save()
                elif prod.color is None:
                    new_prod = prod
                    new_prod.pk = None
                    new_prod.save()
                    new_prod.slug += slugify(offer['sku'])
                    new_prod.price = offer['price']
                    new_prod.leftovers.add(*offer['leftover'])
                    new_prod.save()
                elif prod.color.pk != offer['color']:
                    new_prod = prod
                    new_prod.pk = None
                    new_prod.save()
                    new_prod.color = Color.objects.get(pk=offer['color'])
                    new_prod.slug += slugify(new_prod.color.title)
                    new_prod.price = offer['price']
                    new_prod.leftovers.add(*offer['leftover'])
                    new_prod.save()
                else:
                    prod.price = offer['price']
                    prod.leftovers.add(*offer['leftover'])
                    prod.save()

            bar.next()
        else:
            bar.next()
        bar.finish()

    def compare_produts_variants(self):
        print('Start compare product variants...')

        products = Product.objects.all()
        bar = IncrementalBar('Countdown', max=len(products))

        for prod in products:
            if products.filter(sku=prod.sku):
                for variants in products.filter(sku=prod.sku):
                    if variants not in prod.variants.all():
                        prod.variants.add(variants)
            bar.next()
        bar.finish()

    def parse_description_fashion_season_and_tags(self):
        rows = self.fetch_all_products()

        for row in rows:
            tags_pk = []
            products = Product.objects.filter(sku=row['Article'])
            description_not_edited = row['Description']
            if '#' in description_not_edited:
                tags = description_not_edited.split('#')[1:]
                for tag in tags:
                    ser = TagCreateSerializer(data={'title': tag, 'slug': slugify(tag)})
                    ser.is_valid()
                    tag_saved = ser.save()
                    tags_pk.append(tag_saved.pk)
                for product in products:
                    product.tags.add(*tags_pk)
                    product.description = description_not_edited.split('#')[0]
                    product.save()
            else:
                for product in products:
                    product.description = description_not_edited
                    product.save()
            for product in products:
                product.fashion_collection = row['Season']
                product.save()

    def parse_photos(self):
        print('Start parse photos...')

        self.cursor.execute('SELECT * FROM [iShop].[Pictures] ORDER BY [ArticleIDD];')
        rows = self.cursor.fetchall()
        bar = IncrementalBar('Countdown', max=len(rows))

        for row in rows:
            prods = Product.objects.filter(id_1c=row['ArticleIDD'])
            if prods:
                code = row['FileName'].split('_')[-2]
                if not code == 'NA':
                    if prods.filter(color__code_1c=code) or prods.filter(color__synonyms__icontains=code):
                        img = None
                        if 'LARGE' in row['FileName']:
                            img = Image.objects.update_or_create(
                                image_l=f'{settings.MEDIA_ROOT}/img/products/LARGE/' + row['FileName'].split('\\')[-1],
                                title=row['ArticleIDD'])
                        elif 'MEDIUM' in row['FileName']:
                            img = Image.objects.update_or_create(
                                image_m=f'{settings.MEDIA_ROOT}/img/products/MEDIUM/' + row['FileName'].split('\\')[-1],
                                title=row['ArticleIDD'])
                        elif 'SMALL' in row['FileName']:
                            img = Image.objects.update_or_create(
                                image_l=f'{settings.MEDIA_ROOT}/img/products/SMALL/' + row['FileName'].split('\\')[-1],
                                title=row['ArticleIDD'])
                        prods[0].image.add(img[0].pk)
                else:
                    img = None
                    if 'LARGE' in row['FileName']:
                        img = Image.objects.update_or_create(
                            image_l=f'{settings.MEDIA_ROOT}/img/products/LARGE/' + row['FileName'].split('\\')[-1],
                            title=row['ArticleIDD'])
                    elif 'MEDIUM' in row['FileName']:
                        img = Image.objects.update_or_create(
                            image_m=f'{settings.MEDIA_ROOT}/img/products/MEDIUM/' + row['FileName'].split('\\')[-1],
                            title=row['ArticleIDD'])
                    elif 'SMALL' in row['FileName']:
                        img = Image.objects.update_or_create(
                            image_l=f'{settings.MEDIA_ROOT}/img/products/SMALL/' + row['FileName'].split('\\')[-1],
                            title=row['ArticleIDD'])
                    for prod in prods:
                        prod.image.add(img[0].pk)
            bar.next()
        bar.finish()

    def close(self):
        self.conn.close()


def parse():
    parser = DBParser()
    # clear_all()
    # parser.parse_categories()
    # parser.parse_subcategory()
    # parser.parse_brands()
    # parser.parse_products()
    parser.parse_description_fashion_season_and_tags()
    parser.compare_produts_variants()
    parser.parse_photos()
    parser.close()