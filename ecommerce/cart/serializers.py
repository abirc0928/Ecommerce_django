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

from rest_framework import serializers
from .models import Order, OrderItems

class OrderItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='Product.product_name', read_only=True)
    class Meta:
        model = OrderItems
        fields = ['id', 'user', 'order', 'product_name', 'quantity', 'total_price', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)  # Include order items

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'cart',
            'ammount',
            'is_paid',
            'order_id',
            'payment_id',
            'payment_signature',
            'status',
            'created_at',
            'order_items'
        ]
