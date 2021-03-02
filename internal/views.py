from datetime import datetime,date

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics,mixins,status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .models import Ingredient, Dish , Order
from .serializers import IngredientSerializer,DishSerializer, CustomerDishSerializer , OrderSerializer 
from internal.utils import months_in_reverse
from internal.permissions import IsCustomer
# Create your views here.



@api_view(['GET'])
def api_overview(request):
    IngredientDict={
            'To get list of Ingrdients  REQUEST-TYPE = GET              '  :                '/ingredients/',
            'Adding an Ingredient  REQUEST-TYPE = POST                  '  :                '/ingredients/',
            'Detail of single Ingrdient  REQUEST-TYPE = GET             '  :                '/ingredients/<int:id>/',
            'Deleting an Ingredient  REQUEST-TYPE = DELETE              '  :                '/ingredients/<int:id>/',
    }
    MenuDict={
            'To get list of DISHES  REQUEST-TYPE = GET                  '  :                '/menu/',
            'To get list of DISHES for Customer  REQUEST-TYPE = GET     '  :                'customer/menu/',
            'Adding a DISH  REQUEST-TYPE = POST                         '  :                '/menu/',
            'Detail of single DISH  REQUEST-TYPE = GET                  '  :                '/menu/<int:id>/',
            'Deleting a DISH  REQUEST-TYPE = DELETE                     '  :                '/menu/<int:id>/',
    }
    OrderDict={
            'To get list of ORDERS  REQUEST-TYPE = GET                  '  :                '/order/',
            'Adding an ORDER  REQUEST-TYPE = POST                       '  :                '/order/',
            'Detail of single ORDER  REQUEST-TYPE = GET                 '  :                '/order/<int:id>/',
            'Deleting an ORDER  REQUEST-TYPE = DELETE                   '  :                '/order/<int:id>/',
            'To get ORDER History of single USER REQUEST-TYPE = GET     '  :                '/order/history/',
        }
    
    url_list={
        
        'ADMIN PANEL                                                    '  :                 '/admin/',
        'REGISTER                                                       '  :                 'accounts/regsiter/',
        'LOGIN                                                          '  :                 'accounts/login/',
        'Monthly Sales Report                                           '  :                 '/sales/report/',
        'ENDPOINTS FOR INGREDIENT                                       '  :                 IngredientDict ,
        'ENDPOINTS FOR MENU                                             '  :                 MenuDict,
        'ENDPOINTS FOR ORDERS                                           '  :                 OrderDict,
                                                                     
    }
    return Response(url_list)



#-----------------------------------------------VIEWS FOR INGREDIENTS---------------------------------------------------------



class IngredientAPI(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser]
    serializer_class = IngredientSerializer
    queryset=Ingredient.objects.all()
    
    
    def perform_create(self, serializer):
        serializer.save()


class IngredientDetailAPI(generics.RetrieveDestroyAPIView):
    permission_classes=[IsAdminUser]
    serializer_class = IngredientSerializer
    

    def get_queryset(self):
        id=self.kwargs['pk']
        return Ingredient.objects.filter(id=id)   

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            msg={"detail" : "Deleted Successfully"}
            return Response(msg)
        else:
            raise ValidationError("This Ingredients doesn't exist!!")



#------------------------------------------------------VIEWS FOR MENU-------------------------------------------------------------



class DishAPI(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser]
    serializer_class = DishSerializer
    queryset=Dish.objects.all()
    
    
    def perform_create(self, serializer):
        serializer.save()

class CustomerDishAPI(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = CustomerDishSerializer
    queryset=Dish.objects.all()
    
    

class DishDetailAPI(generics.RetrieveDestroyAPIView):
    permission_classes=[IsAdminUser]
    serializer_class = DishSerializer
    

    def get_queryset(self):
        id=self.kwargs['pk']      
        try:
            return Dish.objects.filter(id=id)   
        except Dish.DoesNotExist:
            raise ValidationError("The Ingredients with this id doesn't exists!")


    def delete(self,request,*args,**kwargs):
        if self.get_queryset():
            self.get_queryset().delete()
            msg={"detail" : "Deleted Successfully"}
            return Response(msg)
        else:
            raise ValidationError("This Dish doesn't exist!!")



#----------------------------------------------------------VIEWS FOR ORDER-------------------------------------------------------------



class OrderAPI(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = OrderSerializer
    queryset=Order.objects.all()
    
    
    def perform_create(self, serializer):
        serializer.save(order_by=self.request.user)


class OrderDeleteAPI(generics.RetrieveDestroyAPIView):
    permission_classes=[IsAuthenticated]            
    serializer_class = OrderSerializer
    """ 
        By changing the permission class to IsCustomer. We can only allow the Customer to use this 
        View ,Admin user wont be able to use this. IsCustomer is defined in internal/permissions.py    
    """
    

    def get_queryset(self):
        id=self.kwargs['pk']
        try:
            o=Order.objects.filter(id=id)
            if(self.request.user.username == o[0].order_by):
                return o
            else:
                raise ValidationError("You are not authorized for this!")
        except (Order.DoesNotExist ,IndexError):
                raise ValidationError("The Order with this id doesn't exists!")

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            msg={"detail" : "Deleted Successfully"}
            return Response(msg)
        else:
            raise ValidationError("This Dish doesn't exist!!")


class OrderHistoryAPI(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrderSerializer
    

    def get_queryset(self):
        return Order.objects.filter(order_by=self.request.user.username).order_by('-order_date')
        




#------------------------------------------------MONTHLY-SALES-REPORT-VIEW-------------------------------------------------



@api_view(['GET'])
@permission_classes([IsAdminUser])
def monthly_report(request):
    cur_year=datetime.today().year
    cur_month=datetime.today().month

    #This method is imported from internal.utils (Returns list of months in reverse order like [2,1,12,11,10,9,8,7,6,5,4,3])
    k=months_in_reverse()
    d=dict()
    for i in k:
        year=cur_year if cur_month - i >0  else cur_year-1
        
        #This query willreturn queryset with the product sold and count of each product sold.
        p=Order.objects.all().values('items_ordered').annotate(count=Count('items_ordered'),).filter(order_date__month=int(i))
        total_profit=0
        total_sold=0
        per_monthly_record=dict()
        for i in p:
            item=i['items_ordered']
            c=i['count']
            dish=Dish.objects.filter(id=item)[0]
            total_profit+=dish.profit()*c
            total_sold+=c

            #adding no. of product sold per month to per_monthly_record
            per_monthly_record[dish.name]=c

        #adding total profit made and total products sold during a month to per_monthly_record
        per_monthly_record['total_product_sold']=total_sold
        per_monthly_record['total_profit']=total_profit

        #creating which month and year we are currently posting the record for
        dt=date(year,int(i),1)
        
        #finally adding the per_month_record with the detail of the month to the dictionary to be diplayed
        d[str(dt)]=per_monthly_record
    return JsonResponse(d)
        
        
           
        




