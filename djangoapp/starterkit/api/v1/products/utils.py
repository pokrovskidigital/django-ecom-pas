from .models import Product


def create_recomendations():
    prods = Product.objects.all()
    for prod in prods:
        recom_products = prods.filter(price__gt=(prod.price - prod.price * 0.3),
                                      price__lt=(prod.price + prod.price * 0.3),
                                      category=prod.category)
        prod.similar_products.add(recom_products[:5])
        prod.save()
        print(prod.similar_products.all())