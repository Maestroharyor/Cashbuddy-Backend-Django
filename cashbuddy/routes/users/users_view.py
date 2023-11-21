# views.py
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.mail import send_mail
from django.conf import settings
import random

from ...models import CustomUser
from ...serializers import UserSerializer

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    
    return Response({
        'success': True,
        'message': 'All users retrieved successfully',
        'data': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    serializer = UserSerializer(user)
    
    return Response({
        'success': True,
        'message': f'User details for user ID {user_id} retrieved successfully',
        'data': serializer.data
    })