from django.urls import path
from .views import *
urlpatterns = [
    path('products/', ProductView.as_view() , name='products'),
    path('demo/', DemoView.as_view() , name='DemoView'),
]
