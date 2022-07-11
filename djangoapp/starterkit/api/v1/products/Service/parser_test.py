import json
import xmltodict
from progress.bar import IncrementalBar
from uuslug import slugify
from ..serializers import CategoryCreateSerializer, ProductCreateSerializer, SexCreateSerializer, \
    ColorCreateSerializer, SizeCreateSerializer, TagCreateSerializer, LeftoverCreateSerializer
from ..models import Product, Category, Sex, Color, Tag, Leftover, Size
import random
import progress

PARSE_COUNT = 100
data_offers = []
option_data = {
    "afb463d2-a9b7-11ec-a78a-005056872661": "Состав",
    "cb1538f5-a9b7-11ec-a78a-005056872661": "Сезон",
    "1fa15c7c-bbc0-11ec-a78b-005056872661": "Модель",
    "3a08a65f-bbc0-11ec-a78b-005056872661": "Размерная сетка",
    "82a4e959-a9b7-11ec-a78a-005056872661": "Коллекция",
    "91631e87-a9b7-11ec-a78a-005056872661": "Линия",
    "9c570722-a9b7-11ec-a78a-005056872661": {
        "9c570722-a9b7-11ec-a78a-005056872661": "Пол",
        "vars": {
            "9d589315-a9b7-11ec-a78a-005056872661": "G",
            "25135b52-af3c-11ec-a78a-005056872661": "Д",
            "a55fa373-a9b7-11ec-a78a-005056872661": "Ж",
            "a55fa383-a9b7-11ec-a78a-005056872661": "У",
            "131b5e16-af3c-11ec-a78a-005056872661": "B",
            "1bfbf191-af3c-11ec-a78a-005056872661": "М"
        }
    }
}


def parse_category():
    with open("/code/api/v1/products/Service/import0_1.xml", 'r', encoding="utf-8") as f:
        data = {'category': []}
        a = f.read()
        parsed_xml = xmltodict.parse(a, encoding="utf-8")
        for cat in parsed_xml['КоммерческаяИнформация']['Классификатор']['Группы']['Группа']:
            category_data = {'id_1c': cat['Ид'], 'title': cat['Наименование']}
            category_data['slug'] = slugify(category_data['title'])
            category_data['discription'] = ""

            data['category'].append(category_data)
        ser = CategoryCreateSerializer(data=data['category'], many=True)
        ser.is_valid(raise_exception=True)
        ser.create(ser.validated_data)


def parse_sex(product):
    sex = {}
    sex_obj = None
    for option in product["ЗначенияСвойств"]["ЗначенияСвойства"]:
        if option['Ид'] == '9c570722-a9b7-11ec-a78a-005056872661':
            title = option_data['9c570722-a9b7-11ec-a78a-005056872661']['vars'][
                option['Значение']]
            sex = {
                'id_1c': option['Значение'],
                'title': title,
                'slug': slugify(title)
            }
            ser = SexCreateSerializer(data=sex)
            ser.is_valid(raise_exception=True)
            sex_obj = ser.create(ser.validated_data)

    return sex_obj


def create_category(cat_data):
    ser = CategoryCreateSerializer(data=cat_data)
    ser.is_valid(raise_exception=True)
    return ser.create(ser.validated_data)


def get_fashion_season(prod):
    for option in prod["ЗначенияСвойств"]["ЗначенияСвойства"]:
        if option['Ид'] == 'cb1538f5-a9b7-11ec-a78a-005056872661':
            return option['Значение']


def create_color(data):
    for options in data['ХарактеристикиТовара']['ХарактеристикаТовара']:

        if options['Ид'] == '72a2b91e-ab2b-11ec-a78a-005056872661':
            try:
                color = {
                    'title': options['Значение'].split('/')[1],
                    'code_1c': options['Значение'].split('/')[0],
                    'slug': slugify(options['Значение'].split('/')[1])
                }
            except:
                color = {
                    'title': options['Значение'],
                    'code_1c': options['Значение'],
                    'slug': slugify(options['Значение'])
                }
            ser = ColorCreateSerializer(data=color)
            ser.is_valid(raise_exception=True)
            return ser.create(ser.validated_data)[0]


def parse_product():
    product_list = []
    with open("/code/api/v1/products/Service/import0_1.xml", 'r', encoding="utf-8") as f:
        data = {}
        a = f.read()
        parsed_xml = xmltodict.parse(a, encoding="utf-8")
        count = 0
        for prod in parsed_xml['КоммерческаяИнформация']['Каталог']["Товары"]['Товар'][300:500]:
            title = prod['Наименование']
            sex = parse_sex(prod)
            sku = prod['Артикул']
            id_1c = prod['Ид']
            category = {'title': prod['Наименование'].split(',')[0],
                        "id_1c": 'a',
                        "slug": slugify(prod['Наименование'].split(',')[0]),
                        'discription': "", "sex": sex[0].pk}
            discription = ''
            tags = []
            # fashion_season
            try:
                fashion_collection = get_fashion_season(prod)
            except:
                fashion_collection = ''
            # tags and disc
            try:
                if 'Описание' in prod:
                    if '#' in prod['Описание']:
                        discription = prod['Описание'].split("|")[0]
                        tag_list = prod['Описание'].split("#")[1:]
                        tag_list = [x for x in tag_list if x]
                        for tag in tag_list:
                            tag_ser = TagCreateSerializer(data={'title': tag, 'slug': slugify(tag)})
                            tag_ser.is_valid(raise_exception=True)

                            tags.append(tag_ser.create(tag_ser.validated_data).pk)
                    else:
                        discription = prod['Описание']
            except:
                discription = ''
                tags = []
            data_offer = next((x for x in data_offers if x["sku"] == sku), None)
            leftovers = [230816]
            price = 10000
            try:
                leftovers = data_offer['leftover']
                price = data_offer['price']
            except:
                pass
            cat = create_category(category)
            count += 1
            sex_pk = None
            if sex:
                sex_pk = sex[0].pk
            try:
                color = create_color(prod)
                data = {
                    "title": title,
                    "sku": sku,
                    "id_1c": id_1c,
                    "category": cat[0].pk,
                    'sex': sex_pk,
                    'fashion_collection': fashion_collection,
                    'color': color.pk,
                    'discription': discription,
                    'leftovers': leftovers,
                    'price': price,
                    'tags': tags,
                    'weight': 'a ',
                    'width': ' d',
                    'height': ' s',
                    'volume': ' a',
                    # 'slug': slugify(title + " " + sex[0].title + " " + color.title + ' ' + sku)
                    'slug': slugify(title + " " + id_1c)

                }
            except:
                data = {
                    "title": title,
                    "sku": sku,
                    "id_1c": id_1c,
                    "category": cat[0].pk,
                    'sex': sex_pk,
                    'discription': discription,
                    'fashion_collection': fashion_collection,
                    'leftovers': data_offer['leftover'],
                    'tags': tags,
                    'weight': 'a ',
                    'width': ' d',
                    'height': ' s',
                    'volume': ' a',
                    'price': data_offer['price'],
                    # 'slug': slugify(title + " " + sex[0].title + " " + color.title + " " + id_1c)
                    'slug': slugify(title + " " + id_1c)
                }
            product_list.append(data)
            ser = ProductCreateSerializer(data=data)
            ser.is_valid(raise_exception=True)
            ser.save()


def parse_options():
    with open("api/v1/products/Service/import0_1.xml", 'r', encoding="utf-8") as f:
        a = f.read()
        parsed_xml = xmltodict.parse(a, encoding="utf-8")

        with open("out_option.json", 'w', encoding="utf-8") as of:

            data_out = {}
            for sv in parsed_xml['КоммерческаяИнформация']['Классификатор']['Свойства']['Свойство']:
                if sv['Наименование'] != 'Пол':
                    data_out |= {sv['Ид']: sv['Наименование']}
                else:
                    s_data = {}
                    for var in sv['ВариантыЗначений']['Справочник']:
                        s_data = s_data | {var['ИдЗначения']: var['Значение']}

                    data_out |= {sv['Ид']: {sv['Ид']: sv['Наименование'], 'vars': s_data}}
                    of.write(json.dumps(data_out, indent=4, ensure_ascii=False))


def clear_all():
    Product.objects.all().delete()
    Category.objects.all().delete()
    Sex.objects.all().delete()
    Color.objects.all().delete()
    Tag.objects.all().delete()
    Leftover.objects.all().delete()
    Size.objects.all().delete()


def parse():
    clear_all()
    parse_offers()
    parse_category()
    parse_product()


def create_leftover(offer):
    size = ''
    count = int(offer['Количество'])
    try:
        for option in offer['ЗначенияСвойств']['ЗначенияСвойства']:
            if option['Наименование'] == 'Размер':
                size = option['Значение']
    except:
        try:
            size = offer['Наименование'].split('Размер:')[1].replace(';)', '')
        except:
            size = None
    try:
        size_ser = SizeCreateSerializer(data={"title": size})
        size_ser.is_valid(raise_exception=True)
        size = size_ser.create(size_ser.validated_data).pk
    except:
        pass

    leftovers_ser = LeftoverCreateSerializer(data={'parent_size': size, "count": count})
    leftovers_ser.is_valid(raise_exception=True)
    return leftovers_ser.save()


def parse_offers(sku_list):
    global data_offers
    data = []
    with open("starterkit/api/v1/products/Service/offers0_1.xml", 'r', encoding="utf-8") as f:
        a = f.read()
        parsed_xml = xmltodict.parse(a, encoding="utf-8")
        count = 0
        print('Start parsing offers...')
        bar = IncrementalBar('Countdown', max=len(
            parsed_xml['КоммерческаяИнформация']['ПакетПредложений']["Предложения"]['Предложение']))
        for offer in parsed_xml['КоммерческаяИнформация']['ПакетПредложений']["Предложения"]['Предложение']:
            if offer['Артикул'] in sku_list:
                leftover = create_leftover(offer)
                try:
                    color_data = offer['Наименование'].split('Цвет:')[1].split(';')[0]
                    try:
                        color = {
                            'title': color_data.split('/')[1],
                            'code_1c': color_data.split('/')[0],
                            'slug': slugify(color_data.split('/')[1])
                        }
                    except:
                        color = {
                            'title': color_data,
                            'code_1c': color_data,
                            'slug': slugify(color_data)
                        }
                    ser = ColorCreateSerializer(data=color)
                    ser.is_valid(raise_exception=True)
                    color = ser.create(ser.validated_data).pk
                except:
                    color = None
                leftover.price = float(offer['Цены']['Цена']["ЦенаЗаЕдиницу"])
                leftover.save()
                offer_data = {
                    'leftover': [leftover.pk],
                    'price': float(offer['Цены']['Цена']["ЦенаЗаЕдиницу"]),
                    'sku': offer['Артикул'],
                    'color': color,
                }
                data.append(offer_data)
            bar.next()
    bar.finish()
    print('Start compare offers...')
    bar = IncrementalBar('Countdown', max=len(data))
    compares = []
    for offer in data:
        if offer['color'] is not None:
            for of in data:
                if of['color'] is not None:
                    if (of['sku'] + Color.objects.get(pk=of['color']).title) == (
                            offer['sku'] + Color.objects.get(pk=offer['color']).title):
                        compares.append(of)
            if offer['sku'] in sku_list:
                for com in compares:
                    offer['leftover'].append(com['leftover'][0])
                    data.remove(com)
                    data_offers.append(offer)
                compares = []
        else:
            data_offers.append(offer)
        bar.next()
    bar.finish()
    return data_offers
