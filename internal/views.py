from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics,mixins,status
from rest_framework.exceptions import ValidationError
from .models import Ingredient, Dish , Order
from .serializers import IngredientSerializer,DishSerializer , OrderSerializer , SaleReportSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.db.models import Count
# Create your views here.

@api_view(['GET'])
def api_overview(request):
    url_list={
        'Product'                                                      :                'INGREDIENT',
        'To get list of Ingrdients  REQUEST-TYPE = GET'                :                '/ingredients/',
        'Adding an Ingredient  REQUEST-TYPE = POST'                    :                '/ingredients/',
        'Detail of single Ingrdient  REQUEST-TYPE = GET'               :                '/ingredients/<int:id>/',
        'Deleting an Ingredient  REQUEST-TYPE = DELETE'                :                '/ingredients/<int:id>/',
       
    }
    return Response(url_list)

#VIEWS FOR INGREDIENTS


class IngredientAPI(generics.ListCreateAPIView):
    serializer_class = IngredientSerializer
    queryset=Ingredient.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()


class IngredientDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        id=self.kwargs['pk']
        try:
            return Ingredient.objects.filter(id=id)    
        except:
            raise ValidationError("The Ingredients with this id doesn't exists!")

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response("Deleted Successfully",status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("This Ingredients doesn't exist!!")


#VIEWS FOR MENU

class DishAPI(generics.ListCreateAPIView):
    serializer_class = DishSerializer
    queryset=Dish.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()


class DishDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = DishSerializer

    def get_queryset(self):
        
        try:
            return Dish.objects.filter(id=self.kwargs['pk'])    
        except:
            raise ValidationError("The Dish with this id doesn't exists!")

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response("Deleted Successfully",status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("This Dish doesn't exist!!")


#VIEWS FOR ORDER

class OrderAPI(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset=Order.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()


class OrderDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        id=self.kwargs['pk']
        try:
            return Order.objects.filter(id=id)    
        except:
            raise ValidationError("The Dish with this id doesn't exists!")

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response("Deleted Successfully",status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("This Dish doesn't exist!!")


class OrderHistoryAPI(generics.ListAPIView):
    serializer_class=OrderSerializer

    def get_queryset(self):
        orders = Order.objects.filter(order_by=self.request.user).order_by('-order_date')
        return orders


class ReportSaleAPI(generics.ListAPIView):
    serializer_class=SaleReportSerializer

    def get_queryset(self):
        total_profit=0
        total_sold=0
        p=Order.objects.all().values('items_ordered').annotate(count=Count('items_ordered')),filter(order_date__month=self.kwargs['month'])
        d=dict()
        for i in p:
            item=i['items_ordered']
            c=i['count']
            dish=Dish.objects.filter(id=item)[0]
            d[dish.name]=c
            total_profit+=dish.profit()*c
            total_sold+=c
        d['total_profit']=float(total_profit)
        
        
           
        




