from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(APIView):
    
    def post(self , request):
        username = request.data['username']
        password = request.data['password']
        print(username , password)
        user = User(username=username)
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status":"success" ,
                'user_id' :user.id , 
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
    

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # Call the original view logic
        tokens = response.data  # This contains 'access' and 'refresh'

        # Set the tokens in cookies
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,  # Prevent JavaScript from accessing the cookie
            secure=True,    # Use only with HTTPS
            samesite='Lax', # Restrict cookie to same-site requests
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='Lax',
        )

        return response
    
class LogoutView(APIView):
    def post(self, request):
        # Create a response
        response = Response({"success": "Logged out successfully"})

        # Delete the access and refresh token cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response