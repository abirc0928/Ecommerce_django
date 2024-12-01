from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from products.models import Product
from rest_framework import status
# Create your views here.


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user, ordered=False)
        except Cart.DoesNotExist:
            return Response({"message": "The cart does not exist."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = CartItems.objects.filter(user=user, cart=cart)
        if not cart_items.exists():
            return Response({"message": "The cart is empty."}, status=status.HTTP_200_OK)

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

        # Delete the specified cart item
        cart_items = CartItems.objects.filter(id=data['id'])
        if not cart_items.exists():
            return Response({"message": "Item not found."}, status=404)

        cart_items.delete()

        # Get remaining cart items
        cart = Cart.objects.get(user=user, ordered=False)
        remaining_cart_items = CartItems.objects.filter(user=user, cart=cart)

        # Serialize and return updated cart items
        serializer = CartItemsSerializer(remaining_cart_items, many=True)
        return Response(serializer.data)
        
    def put(self, request):
        user = request.user
        data = request.data

        cart_items = CartItems.objects.get(id=data.get('id'))
        cart_items.quantity += int(data['quantity'])
        cart_items.save()
        
        cart = Cart.objects.get(user=user, ordered=False)
        cart_items = CartItems.objects.filter(user=user, cart=cart)
        serializer = CartItemsSerializer(cart_items, many=True)

        return Response(serializer.data)
        

class OrderView(APIView):

    def get(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
      

class PlaceOrderView(APIView):
    def get(self, request):
        user = request.user
        order_item = Order.objects.filter(user=user)
        serializer = OrderSerializer(order_item, many=True)
        return Response(serializer.data)
    def post(self, request):
        user = request.user  # Get the logged-in user

        try:
            # Step 1: Get the user's active cart and items
            cart = Cart.objects.get(user=user, ordered=False)
            cart_items = CartItems.objects.filter(cart=cart)

            if not cart_items.exists():
                return Response({"message": "Your cart is empty!"}, status=status.HTTP_400_BAD_REQUEST)

            # Step 2: Calculate the total amount
            total_amount = sum(item.price for item in cart_items)

            # Step 3: Create the order
            order = Order.objects.create(
                user=user,
                cart=cart,
                ammount=total_amount,
                order_id=f"ORD-{user.id}-{cart.id}"  # Example order ID
            )

            # Step 4: Create order items
            for item in cart_items:
                OrderItems.objects.create(
                    user=user,
                    order=order,
                    product_name=item.product.product_name,  # Snapshot of the product
                    quantity=item.quantity,
                    total_price=item.price
                )

            # Step 5: Mark the cart as ordered
            cart.ordered = True
            cart.save()

            # Step 6: Serialize and return the order details
            serializer = OrderSerializer(order)
            print("serializer.data", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"message": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)

        