from django.contrib import admin
from .models import Customer,Admin
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(is_staff=False)


class adminsAdmin(admin.ModelAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(is_staff=True)


admin.site.register(Customer,CustomerAdmin)
admin.site.register(Admin,adminsAdmin)