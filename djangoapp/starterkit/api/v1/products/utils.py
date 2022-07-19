from .models import Product


def create_recomendations():
    prods = Product.objects.all()
    for prod in prods:
        recom_products = prods.filter(price__gt=(prod.price - prod.price * 0.3),
                                      price__lt=(prod.price + prod.price * 0.3),
                                      category=prod.category)
        for pp in prod.similar_products.all():
            prod.similar_products.remove(pp)
        print(*(recom_products[:5].values_list('pk')))
        for p in recom_products[:5].values_list('pk'):
            try:
                prod.similar_products.add(p[0])
            except:
                print('empty')
        prod.save()
        print(prod.similar_products.all())
