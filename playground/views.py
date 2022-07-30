from django.shortcuts import render
from store.models import Product, OrderItem


def say_hello(request):
    ordered_products = OrderItem.objects.values('product__id').distinct();
    print(ordered_products)
    products = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')[:5]

    return render(request, 'hello.html', {'name': 'Mosh', 'products': list(products)})
