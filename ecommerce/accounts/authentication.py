from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')  # Get token from cookies

        if not access_token:
            return None  # No token, let other authenticators handle it

        try:
            # Validate the access token
            validated_token = AccessToken(access_token)
            user = self.get_user_from_token(validated_token)
            return (user, validated_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

    def get_user_from_token(self, token):
        from django.contrib.auth.models import User
        user_id = token['user_id']  # Extract user ID from token payload
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")