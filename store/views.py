from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'This product can not be deleted because it is associated with an order item'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'This collection can not be deleted because it is included one or more product'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
