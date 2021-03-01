from django.shortcuts import render
from accounts.serializers import CustomerRegister , UserLoginSerializer
from rest_framework.response import Response
from rest_framework import generics,status,permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,AllowAny



#----------------------------------------------------CUSTOMER-REGISTER-VIEW-----------------------------------------------------

# Create your views here.
class CustomerRegisterAPI(generics.CreateAPIView):
    serializer_class=CustomerRegister
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_staff=False,is_active=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

"""
class LoginAPI(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class=UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response("Successfully logged In !!", status=status.HTTP_201_CREATED)
"""


#----------------------------------------------------USER-LOGIN-VIEW-----------------------------------------------------



class LoginAPI(APIView):
    serializer_class=UserLoginSerializer

    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},status=status.HTTP_200_OK)


#----------------------------------------------------USER-LOGOUT-VIEW-----------------------------------------------------

"""

@api_view(['GET'])       
def user_logout(request):
    print(request.user)
    logout(request)
    data = {'success': 'Sucessfully logged out'}
    print(request.user)
    return Response(data=data, status=status.HTTP_200_OK)

"""