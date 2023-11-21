# auth_urls.py
from django.urls import path
from .auth_views import signup, login, reset_password, verify_reset_password

urlpatterns = [
    path('signup', signup, name='signup'),
path('login', login, name='login'),
    path('reset-password', reset_password, name='reset-password'),
    path('verify-reset-password', verify_reset_password, name='verify-reset-password'),
]
