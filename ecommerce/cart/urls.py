from django.urls import path
from .views import *
urlpatterns = [
    path('cart/', CartView.as_view() , name='products'),
    path('place-order/', PlaceOrderView.as_view(), name='place-order'),
]
