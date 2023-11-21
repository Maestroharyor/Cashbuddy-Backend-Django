# serializers.py
from rest_framework import serializers
from .models import CustomUser
# from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.password_validation import validate_password
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Use the correct attribute for user_id
#         user_id_field = user.user_id
#         token['user_id'] = str(user_id_field)  # Convert to string if necessary

#         return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'country']

class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'country']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user