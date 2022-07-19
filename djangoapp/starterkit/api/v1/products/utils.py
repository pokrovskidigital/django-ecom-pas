import api.v1.products.models as models

def create_recomendations():
    prods = models.Product.objects.all()
    for prod in prods:
        recom_products = prods.filter(price__gt=(prod.price - prod.price * 0.3),
                                      price__lt=(prod.price + prod.price * 0.3),
                                      category= prod.category)
        print(recom_products.count())