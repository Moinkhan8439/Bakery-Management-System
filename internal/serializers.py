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



class CustomerDishSerializer(serializers.ModelSerializer):
    price=serializers.DecimalField(source='selling_price',max_digits=10,decimal_places=2)
    class Meta:
        model=Dish
        fields = ['id','name','description','price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = '__all__'



    