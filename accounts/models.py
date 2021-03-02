from django.db import models
from django.contrib.auth.models import User,BaseUserManager,PermissionsMixin
from django.utils import timezone

# Create your models here.



class AdminsManager(BaseUserManager):
    
    def create_user(self,username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_staff=True
        user.save()
        return user

    def get_queryset(self):
        return User.get_queryset().filter(is_staff=True)



class CustomerManager(BaseUserManager):

    def create_user(self,username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=False,is_active=True,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
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


