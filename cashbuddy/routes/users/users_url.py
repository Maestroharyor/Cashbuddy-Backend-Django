# user_urls.py
from django.urls import path
from .users_view import get_user_details, get_all_users

urlpatterns = [
    path('', get_all_users, name='all-users'),
    path('<int:user_id>', get_user_details, name='user-details'),

]
