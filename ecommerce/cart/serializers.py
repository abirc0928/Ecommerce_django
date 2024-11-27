from rest_framework import serializers
from .models import *
from products.models import Product
from products.serializers import ProductSerializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart = CartSerializer()
    class Meta:
        model = CartItems
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'