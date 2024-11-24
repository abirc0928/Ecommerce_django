from django.db import models
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.category_name


class QuentityVariant(models.Model):
    varient_name = models.CharField(max_length=100)

    def __str__(self):
        return self.varient_name

class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name

class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)

    def __str__(self):
        return self.size_name
        
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/products')
    price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField()

    quentity_type = models.ForeignKey(QuentityVariant, on_delete=models.PROTECT, null=True, blank=True)
    color_type = models.ForeignKey(ColorVariant, on_delete=models.PROTECT, null=True, blank=True)
    size_type = models.ForeignKey(SizeVariant, on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return self.product_name

class Product_image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='static/products')