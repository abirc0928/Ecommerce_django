from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class DemoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        return Response({"Success": "You are autenticated"})

class ProductView(APIView):
    def get(self, request):
        category = self.request.query_params.get('category')  
        if category:
            product = Product.objects.filter(category__category_name__iexact=category)
            if product.count() == 0:
                return Response({"Error": "No product found for this category"})
        else: 
            product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response({'count' : len(serializer.data) ,'data' :serializer.data})

