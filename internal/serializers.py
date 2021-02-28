from rest_framework import serializers
from .models import Order,Ingredient,Dish



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredient
        fields = '__all__'




class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model=Dish
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = '__all__'



    