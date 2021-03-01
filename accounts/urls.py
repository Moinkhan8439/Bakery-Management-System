from django.urls import path
from .views import (CustomerRegisterAPI , LoginAPI)

urlpatterns = [
    path('register/',CustomerRegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    #path('logout/',user_logout),
]
