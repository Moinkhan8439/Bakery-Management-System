from django.db import models
from django.contrib.auth.models import User,BaseUserManager,PermissionsMixin
from django.utils import timezone

# Create your models here.

class AdminsManager(BaseUserManager):
    def create_admin(self, username,first_name, last_name, email, password=None):
        now=timezone.now()
        user = self.model(username=username,first_name=first_name,last_name=last_name,
                    email=self.normalize_email(email),is_staff=True, is_active=True,date_joined=now)
        user.set_password(password)
        user.save()
        return user

    def get_queryset(self):
        return User.get_queryset().filter(is_staff=True)

class CustomerManager(models.Manager):

    def create_customer(self, **kwargs):
        kwargs.update({'is_staff': False})
        return super(CustomerManager, self).create(**kwargs)


    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(is_staff=False)




class Customer(User):
    objects=CustomerManager()
    class Meta:
        proxy =True

class Admin(User):
    class Meta:
        proxy=True


