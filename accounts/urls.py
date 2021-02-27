from django.urls import path
from .views import (CustomerRegisterAPI , LoginAPI)
from knox import views as knox_views

urlpatterns = [
    path('register/',CustomerRegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
]
