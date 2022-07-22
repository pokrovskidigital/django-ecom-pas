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
        size = size_ser.create(size_ser.validated_data)[0].pk
        leftovers_ser = LeftoverCreateSerializer(data={'parent_size': size, "count": count})
    except:
        leftovers_ser = LeftoverCreateSerializer(data={"count": count})

    leftovers_ser = LeftoverCreateSerializer(data={'parent_size': size, "count": count})
    leftovers_ser.is_valid(raise_exception=True)
    return leftovers_ser.save()


def parse_offers(sku_list):
    data_offers = []
    data = []
    with open("api/v1/products/Service/offers0_1.xml", 'r', encoding="utf-8") as f:
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
    colors = Color.objects.all()
    for offer in data:
        if offer['color'] is not None:
            for of in data:
                if of['color'] is not None:
                    if (of['sku'] + colors.get(pk=of['color']).title) == (
                            offer['sku'] + colors.get(pk=offer['color']).title):
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
