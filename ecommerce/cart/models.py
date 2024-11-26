from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=CartItems)
def correct_price(sender, instance, created, **kwargs):
    if created:  
        price_of_product = instance.product.price  #
        instance.price = instance.quantity * float(price_of_product)  
        instance.save(update_fields=['price'])

        cart = instance.cart  
        cart.total_price = sum(item.price for item in cart.cartitems_set.all())  
        cart.save(update_fields=['total_price']) 
    