from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from google.auth.transport import requests
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import CustomTokenObtainPairSerializer, TokenGoogleSerializer, UserSerializer
from utils.auth import get_tokens_for_user
from google.oauth2 import id_token

User = get_user_model()


# Custom TokenObtainPairView for authentication
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# API endpoint for obtaining Google token
class TokenGoogleView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TokenGoogleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_token = serializer.validated_data['token']
        if auth_token is None:
            raise ValidationError(detail='Invalid token', code='invalid')
        try:
            # Verifying Google token
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request(), settings.GOOGLE_CLIENT_ID)
            email = id_info['email'].lower()
            try:
                # Check if user exists
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user if not found
                user = User()
                user.full_name = id_info['name']
                user.profile_pic = id_info.get('picture', None)
                # Generate a random default password for the user
                user.password = make_password(BaseUserManager().make_random_password())
                user.email = email
                user.is_verified = True
                user.auth_type = User.AuthType.GOOGLE
                user.save()
            # Generate tokens for the user (without username & password)
            token = get_tokens_for_user(user)  # generate token without username & password
            update_last_login(None, user)
            return Response(token, status=status.HTTP_200_OK)

        except ValueError:
            raise ValidationError(detail='invalid token', code='invalid')


# Retrieve user profile view
class UserProfileVIew(RetrieveAPIView,):
    serializer_class = UserSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        profile_data = self.get_serializer(instance).data
        return Response(profile_data)

