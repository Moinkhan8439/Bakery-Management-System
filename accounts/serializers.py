from accounts.models import Customer
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomerRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        user = Customer.objects.create_customer(**validated_data)
        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')