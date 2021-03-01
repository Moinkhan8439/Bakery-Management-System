from django.contrib import admin
from django.urls import path,include
from .views import (api_overview , IngredientAPI , IngredientDetailAPI , DishAPI , CustomerDishAPI ,  DishDetailAPI , OrderAPI ,
                     OrderDetailAPI ,OrderHistoryAPI , monthly_report
                    )


urlpatterns = [
    path('',api_overview,),
    
    #URLS FOR Ingredients
    path('ingredients/',IngredientAPI.as_view()),
    path('ingredients/<int:pk>/',IngredientDetailAPI.as_view()),

    #URLS FOR Menu 
    path('menu/',DishAPI.as_view()),
    path('customer/menu/',CustomerDishAPI.as_view()),
    path('menu/<int:pk>/',DishDetailAPI.as_view()),

    #URLS FOR ORDER 
    path('order/',OrderAPI.as_view()),
    path('order/<int:pk>/',OrderDetailAPI.as_view()),
    path('order/history/',OrderHistoryAPI.as_view()),

    #reports sales 
    #path('reports/sales/<int:month>/',ReportSaleAPI.as_view()),
    path('sales/report/',monthly_report)
]
