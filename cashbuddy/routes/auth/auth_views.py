# views.py
from datetime import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
# import random

from ...models import CustomUser, PasswordResetCode
from ...serializers import UserSerializer, OTPSerializer, SignUpSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from ...utils.functions import generate_username, generate_otp


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
def signup(request):
    # Make phone_number optional
    phone_number = request.data.get('phone_number')

    # Define the required fields
    required_fields = ['first_name', 'last_name', 'email', 'password']

    # Check if all required fields are present in the request data
    missing_fields = [field for field in required_fields if field not in request.data]

    if missing_fields:
        raise ValidationError({
            'success': False,
            'message': 'Missing required fields',
            'data': {
                'missing_fields': missing_fields
            }
        }, code=status.HTTP_400_BAD_REQUEST)

    # Generate a unique username based on the first name
    request.data['username'] = generate_username(request.data['first_name'])

    serializer = SignUpSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        error_detail = {}
        for field, errors in validation_error.detail.items():
            error_detail[field] = errors
        return Response({
            'success': False,
            'message': 'Validation error',
            'data': error_detail
        }, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    # Generate JWT token
    refresh = RefreshToken.for_user(user)

    return Response({
        'success': True,
        'message': 'User registered successfully',
        'data': {
            'user': UserSerializer(user).data,
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = CustomUser.objects.filter(email=email).first()

    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'success': True,
            'message': 'User logged in successfully',
            'data': {
                'user': UserSerializer(user).data,
                'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            }
        })
    else:
        return Response({
            'success': False,
            'message': 'Invalid credentials',
            
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reset_password(request):
    try:
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)

        # Generate unique alphanumeric 6-digit code
        code = generate_otp()

        # Save the code in the PasswordResetCode model
        password_reset_code = PasswordResetCode.objects.create(user=user, code=code)

        # Send the code to the user's email
        send_mail(
            'Password Reset Code',
            f'Your password reset code is: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            'success': True,
            'message': 'OTP Code sent successfully',
            
        })
    except CustomUser.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User with the provided email does not exist',
            
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e),
            
        })


@api_view(['POST'])
def verify_reset_password(request):
    try:
        email = request.data.get('email')
        code = request.data.get('otp')
        new_password = request.data.get('new_password')

        user = CustomUser.objects.get(email=email)
        print(user)
        password_reset_code = PasswordResetCode.objects.get(user=user, code=code)

        print(user)
        print(password_reset_code)

        # Check if the code has expired (15 minutes)
        if password_reset_code.is_expired():
            password_reset_code.delete()
            return Response({
                'success': False,
                'message': 'Code has expired',
            })

        # Reset the user's password
        user.set_password(new_password)
        user.save()

        # Delete the used code
        password_reset_code.delete()

        return Response({
            'success': True,
            'message': 'Password reset successfully',
            
        })
    except CustomUser.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User with the provided email does not exist',
            
        })
    except PasswordResetCode.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Invalid code',
            
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e),
            
        })
