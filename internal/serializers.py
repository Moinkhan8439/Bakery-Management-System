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

class SaleReportSerializer(serializers.Serializer):
    total_product_sold=serializers.IntegerField(min_value=0)
    total_profit=serializers.DecimalField(max_digits=None,min_value=0,decimal_places=2)

    