from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
    QUANTITY_CHOICES = [
        ('kg', 'Kilogram'),
        ('lt', 'Litre'),
        ('_', ''),
    ]

    name=models.CharField(max_length=50,blank=False,unique=True)
    quantity=models.PositiveIntegerField(default=0)
    quantity_type=models.TextField(choices=QUANTITY_CHOICES,default='_')
    cost_price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    #def get_quantity(self):
    #    return str(self.quantity) + self.quantity_type


class Dish(models.Model):
    name=models.CharField(max_length=50,blank=False,unique=True)
    ingredients=models.ManyToManyField(Ingredient,blank=False)
    description=models.CharField(max_length=250)
    quantity=models.IntegerField(default=0)
    cost_price=models.DecimalField(max_digits=10, decimal_places=2)
    selling_price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name 

    #@property
    #def full_description(self):
    #    result=f'INGREDIENTS USED : {self.ingredients.all()[:]} \n {self.description}'
    #    return result

    
    def profit(self):
        result=self.selling_price - self.cost_price
        return result

    class Meta:
        verbose_name_plural = "Dishes"


class Order(models.Model):
    order_by=models.ForeignKey(User,on_delete=models.CASCADE)
    items_ordered=models.ManyToManyField(Dish,blank=False)
    order_date=models.DateField( auto_now_add=False,editable=True)

    def __str__(self):
        return str(self.id) +" / " + str(self.order_date)
    
    def get_month(self):
        return self.order_date.month

