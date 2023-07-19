from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Account, TenantUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JSON Web Tokens.
    Adds custom claims to the token, such as 'full_name' and 'email'.
    """

    @classmethod
    def get_token(cls, user):
        """
        Retrieves the token for the specified user, including custom claims.
        """
        token = super().get_token(user)

        # Add custom claims
        token['full_name'] = user.full_name
        token['email'] = user.email

        # ...

        return token

    def validate(self, attrs):
        """
        Validates and processes the token data.
        Converts the email to lowercase for consistency.
        """
        attrs['email'] = attrs['email'].lower()
        resp_data = super().validate(attrs)
        return resp_data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Serializes all fields of the User model.
    """

    class Meta:
        model = User
        fields = '__all__'


class TokenGoogleSerializer(serializers.Serializer):
    """
    Serializer for Google tokens.
    Requires a 'token' field for the Google id_token.
    """
    token = serializers.CharField(required=True, help_text='Google id_token')


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TenantUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TenantUser
        fields = '__all__'
