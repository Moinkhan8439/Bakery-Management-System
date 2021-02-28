from django.db import models
from django.contrib.auth.models import User,BaseUserManager,PermissionsMixin
from django.utils import timezone

# Create your models here.



class AdminsManager(BaseUserManager):

    def get_queryset(self):
        return User.get_queryset().filter(is_staff=True)



class CustomerManager(models.Manager):

    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(is_staff=False)



#-----------------------------------------PROXY-MODELS----------------------------------------------------
#These models doesn't have separate table in the database ,they are just creating a view of the table for us.


class Customer(User):
    objects=CustomerManager()
    class Meta:
        proxy =True



class Admin(User):
    class Meta:
        proxy=True


