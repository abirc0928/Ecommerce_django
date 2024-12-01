from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.utils.timezone import now

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name)


@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Product.objects.get(id=cart_items.product.id)
    
    print(cart_items)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    print(cart_items.id)
    
   
@receiver(post_save, sender=CartItems)
def cart_total_price(sender, **kwargs):
    cart_items = kwargs['instance']
    
    total_cart_items = CartItems.objects.filter(user = cart_items.user )
    cart = Cart.objects.get(id = cart_items.cart.id)

    total_price = 0
    for item in total_cart_items:
        total_price += item.price
    cart.total_price = total_price
    cart.save()
    
    
@receiver(post_delete, sender=CartItems)
def cart_total_price_on_delete(sender, instance, **kwargs):
   
    try:
        cart = Cart.objects.get(id=instance.cart.id)
        total_cart_items = CartItems.objects.filter(cart=cart)
        cart.total_price = sum(item.price for item in total_cart_items)
        cart.save()
    except Cart.DoesNotExist:
        # Handle case where the cart no longer exists
        pass

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ammount = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_signature = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default='Pending',
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Completed', 'Completed'),
            ('Canceled', 'Canceled')
        ]
    )
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItems(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product_name = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField( default=0)
    total_price = models.FloatField( default=0)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Item {self.product_name} in Order {self.order.id}"