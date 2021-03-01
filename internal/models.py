from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



# Create your models here.
class Ingredient(models.Model):
    QUANTITY_CHOICES = [
        ('kg', 'Kilogram'),
        ('lt', 'Litre'),
        ('no.', ''),
    ]

    name=models.CharField(max_length=50,blank=False,unique=True)                #Name of Ingredient
    quantity=models.PositiveIntegerField(default=0)                             #Quantity Available
    quantity_type=models.TextField(choices=QUANTITY_CHOICES,default='_')        #Type of Quantity['kg','lt or ' ' ]
    cost_price=models.DecimalField(max_digits=10, decimal_places=2)             #Cost Price of the Ingredient

    #This function make sures that if we print the  name of the Ingredient will be printed
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
    date=datetime.today().strftime('%Y-%m-%d')
    order_by=models.CharField(max_length=50,default=0)
    items_ordered=models.ManyToManyField(Dish,blank=False,help_text='To select multiple hold ctrl and then select')
    order_date=models.DateField(auto_now_add=False,editable=True,default=date)

    def __str__(self):
        return str(self.id) +" / " + str(self.order_by)
    
    def get_month(self):
        return self.order_date.month

