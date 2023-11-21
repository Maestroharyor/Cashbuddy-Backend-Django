from django.urls import include, path
from .routes_view import welcome


urlpatterns = [
    path('', welcome),
    path('auth/',  include('cashbuddy.routes.auth.auth_url')),
    path('users/', include('cashbuddy.routes.users.users_url')),
]
