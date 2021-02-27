from django.contrib import admin
from .models import Ingredient,Dish,Order
# Register your models here.


admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(Order)