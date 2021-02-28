from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics,mixins,status
from rest_framework.exceptions import ValidationError
from .models import Ingredient, Dish , Order
from .serializers import IngredientSerializer,DishSerializer , OrderSerializer 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime,date
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from internal.utils import months_in_reverse
# Create your views here.

@api_view(['GET'])
def api_overview(request):
    IngredientDict={
            'To get list of Ingrdients  REQUEST-TYPE = GET'                :                '/ingredients/',
            'Adding an Ingredient  REQUEST-TYPE = POST'                    :                '/ingredients/',
            'Detail of single Ingrdient  REQUEST-TYPE = GET'               :                '/ingredients/<int:id>/',
            'Deleting an Ingredient  REQUEST-TYPE = DELETE'                :                '/ingredients/<int:id>/',
    }
    MenuDict={
            'To get list of DISHES  REQUEST-TYPE = GET'                    :                '/menu/',
            'Adding a DISH  REQUEST-TYPE = POST'                           :                '/menu/',
            'Detail of single DISH  REQUEST-TYPE = GET'                    :                '/menu/<int:id>/',
            'Deleting a DISH  REQUEST-TYPE = DELETE'                       :                '/menu/<int:id>/',
    }
    OrderDict={
            'To get list of ORDERS  REQUEST-TYPE = GET'                    :                '/order/',
            'Adding an ORDER  REQUEST-TYPE = POST'                         :                '/order/',
            'Detail of single ORDER  REQUEST-TYPE = GET'                   :                '/order/<int:id>/',
            'Deleting an ORDER  REQUEST-TYPE = DELETE'                     :                '/order/<int:id>/',
            'To get ORDER History of single USER REQUEST-TYPE = GET'       :                '/order/history/',
        }
    url_list={
        'INGREDIENT'                                                        :                 IngredientDict ,
        'MENU'                                                              :                 MenuDict,
        'ORDERS'                                                            :                 OrderDict,
        'Monthly Sales Report'                                              :                 '/sales/report/',
        'ADMIN PANEL'                                                       :                 '/admin/'
    }
    return Response(url_list)



#-----------------------------------------------VIEWS FOR INGREDIENTS---------------------------------------------------------



class IngredientAPI(generics.ListCreateAPIView):
    serializer_class = IngredientSerializer
    queryset=Ingredient.objects.all()
    #permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class IngredientDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = IngredientSerializer
    #permission_classes=[IsAdminUser]

    def get_queryset(self):
        id=self.kwargs['pk']
        try:
            return Ingredient.objects.filter(id=id)   
        except Ingredient.DoesNotExist:
            raise ValidationError("The Ingredients with this id doesn't exists!")

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response("Deleted Successfully",status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("This Ingredients doesn't exist!!")



#------------------------------------------------------VIEWS FOR MENU-------------------------------------------------------------



class DishAPI(generics.ListCreateAPIView):
    serializer_class = DishSerializer
    queryset=Dish.objects.all()
    #permission_classes=[IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save()


class DishDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = DishSerializer
    #permission_classes=[IsAdminUser]

    def get_queryset(self):
        id=self.kwargs['pk']      
        try:
            return Dish.objects.filter(id=id)   
        except Dish.DoesNotExist:
            raise ValidationError("The Ingredients with this id doesn't exists!")


    def delete(self,request,*args,**kwargs):
        if self.get_queryset():
            self.get_queryset().delete()
            return Response("Deleted Successfully",status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("This Dish doesn't exist!!")



#----------------------------------------------------------VIEWS FOR ORDER-------------------------------------------------------------



class OrderAPI(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset=Order.objects.all()
    #permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class OrderDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
    #permission_classes=[IsAuthenticated]

    def get_queryset(self):
        id=self.kwargs['pk']
        try:
            return Order.objects.filter(id=id)   
        except Order.DoesNotExist:
            raise ValidationError("The Ingredients with this id doesn't exists!")

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response("Deleted Successfully",status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("This Dish doesn't exist!!")


class OrderHistoryAPI(generics.ListAPIView):
    serializer_class=OrderSerializer
    #permission_classes=[IsAuthenticated]

    def get_queryset(self):
        orders = Order.objects.filter(order_by=self.request.user).order_by('-order_date')
        return orders



#------------------------------------------------MONTHLY-SALES-REPORT-VIEW-------------------------------------------------



@api_view(['GET'])
def monthly_report(request):
    cur_year=datetime.today().year
    cur_month=datetime.today().month

    #This method is imported from internal.utils (Returns list of months in reverse order like [2,1,12,11,10,9,8,7,6,5,4,3])
    k=months_in_reverse()
    d=dict()
    for i in k:
        year=cur_year if cur_month - i >0  else cur_year-1
        dt=date(year,int(i),1)
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
            per_monthly_record[dish.name]=c
        per_monthly_record['total_product_sold']=total_sold
        per_monthly_record['total_profit']=total_profit
        if(total_sold != 0):
            d[str(dt)]=per_monthly_record
    return JsonResponse(d)
        
        
           
        




