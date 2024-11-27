from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from products.models import Product
# Create your views here.


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.get(user=user, ordered=False)
        cart_items = CartItems.objects.filter(user=user, cart=cart)
        serializer = CartItemsSerializer(cart_items, many=True)
        return Response(serializer.data)
    def post(self, request):

        data = request.data
        user = request.user

        cart,_ = Cart.objects.get_or_create(user=user, ordered=False)
        product = Product.objects.get(id=data['product_id'])

        price_of_product = float(product.price)  
        quantity = int(data['quantity']) 
        product_price = price_of_product * quantity
        
        cart_items = CartItems.objects.create(cart=cart, user=user, product=product, price=product_price, quantity=quantity)
        cart_items.save()

        total_price = 0
        cart_items = CartItems.objects.filter(user=user, cart=cart)
        for item in cart_items:
            total_price += item.price

        cart.total_price = total_price
        cart.save()
        print(cart, product, price_of_product, quantity)
        return Response({"Success": "add to crt"})  
    

    def delete(self, request): 
        user = request.user
        data = request.data
        cart_items = CartItems.objects.filter( id=data['id'])
        cart_items.delete()

        cart = Cart.objects.get(user=user, ordered=False)
        cart_items = CartItems.objects.filter(user=user, cart=cart)
        serializer = CartItemsSerializer(cart_items, many=True)

        total_price = 0
        cart_items = CartItems.objects.filter(user=user, cart=cart)
        for item in cart_items:
            total_price += item.price

        cart.total_price = total_price
        cart.save()
        return Response(serializer.data)
        
    def put(self, request):
        user = request.user
        data = request.data
       
        cart_items = CartItems.objects.get(id=data.get('id'))
        cart_items.quantity += int(data['quantity'])

        product_id  = cart_items.product_id
        price_of_product = float(Product.objects.get(id=product_id).price)
        product_price = price_of_product * cart_items.quantity
        print(product_price)

        cart_items.price = product_price
        cart_items.save()
        
        cart = Cart.objects.get(user=user, ordered=False)
        cart_items = CartItems.objects.filter(user=user, cart=cart)
        serializer = CartItemsSerializer(cart_items, many=True)

        total_price = 0
        cart_items = CartItems.objects.filter(user=user, cart=cart)
        for item in cart_items:
            total_price += item.price

        cart.total_price = total_price
        cart.save()
        return Response(serializer.data)
        

class OrderView(APIView):

    def get(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
      