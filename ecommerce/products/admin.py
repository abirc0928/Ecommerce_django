from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(QuentityVariant)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)
admin.site.register(Product_image)