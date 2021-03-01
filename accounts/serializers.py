from accounts.models import Customer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




class CustomerRegister(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username','first_name','last_name','email','password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'},trim_whitespace=False,write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                raise serializers.ValidationError("Unable to Login with provided credentials", code='authorization')
        else:
            raise serializers.ValidationError('Must include "username" and "password".', code='authorization')

        data['user'] = user
        return data