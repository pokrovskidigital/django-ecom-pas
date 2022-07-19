from .models import Product


def create_recomendations():
    prods = Product.objects.all()
    for prod in prods:
        recom_products = prods.filter(price__gt=(prod.price - prod.price * 0.3),
                                      price__lt=(prod.price + prod.price * 0.3),
                                      category=prod.category)
        print(recom_products[:5].values('pk'))
        # prod.similar_products.add(*(recom_products[:5].values('pk'))['pk'])
        prod.save()
        print(prod.similar_products.all())
