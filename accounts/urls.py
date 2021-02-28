from django.urls import path
from .views import (CustomerRegisterAPI , user_login,user_logout)

urlpatterns = [
    path('register/',CustomerRegisterAPI.as_view()),
    path('login/', user_login),
    path('logout/',user_logout),
]
