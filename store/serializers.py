from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'tax', 'price_with_tax',
                  'collection']

    tax = serializers.SerializerMethodField(method_name='get_tax')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def get_tax(self, product: Product):
        return round(product.unit_price * Decimal(0.1), 2)

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)
