from django.urls import include, path


urlpatterns = [
    path('auth/',  include('cashbuddy.routes.auth.auth_url')),
    path('users/', include('cashbuddy.routes.users.users_url')),
]
