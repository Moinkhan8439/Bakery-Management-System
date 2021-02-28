# Bakery Management System

This ** Bakery Management System ** is based on Django Rest framework and Uses the Token Authentications.The API has two types of User 
ADMIN and CUSTOMER.We have used three different table to register three main objects i.e Ingredients , Dishes and Orders . These tables 
are inter-connected in such a way that a single dish can be made up of more than one Ingredients and a paticular User(CUSTOMER) can order
many dishes at once.

## steps to run the API:

1. Install requirements.txt 
2. Run- python manage.py makemigrations
3. Run- python manage.py migrate
4. Run- python manage.py runserver 



## API-OVERVIEW

Now enter http://127.0.0.1:8000/ in your Browser this will give the details about the functionality offered.
To perform any of the operations mentioned just add the corresponding relative url to this http://127.0.0.1:8000/ .
*Note : All the endpoints corresponding to Ingredients and Dishes are only accessible to ADMIN. *

## MANAGING THE ACCOUNTS REGISTRATION AND  AUTHENTICATION

**Registering a ADMIN**
We can only register admin through the Django admin panel. To acces Django Admin panel you have to create a superuser
Follows these steps to register an ADMIN user:
1. python manage.py createsuperuser
2. Fill all details(username ,email and pasword)
3. Now got to http://127.0.0.1:8000/admin/ and login through the credentials you just entered.
4. Register admin through the USERS section(please tick the is_staff then only you will be considered as ADMIN)



**Registering a CUSTOMER**

URL - http://127.0.0.1:8000/accounts/register/  REQUEST-TYPE =[POST]:
This uses POST request and expects username,email,password,first_name,last_name to be entered through JSON object or a Form data.The username needs to be UNIQUE


**LOGGING IN A USER**

URL - http://127.0.0.1:8000/accounts/login/  REQUEST-TYPE =[POST]:
This uses POST request and expects username and password.After successfull login this will return a Token and Expiry.
Expiry denotes for how long is the token valid ,after the expiry you need to login again.


**LOGGING OUT A USER** 

URL - http://127.0.0.1:8000/accounts/logout/  REQUEST-TYPE =[]:
For this provide the token in the header.The user whose token you entered will be logged out.

## OPERATIONS ON INGREDIENTS(ACCESSIBLE ONLY TO ADMINS)

**Adding an Ingredient**

URL - http://127.0.0.1:8000/ingredients/  REQUEST-TYPE =[POST] :
This uses POST request and expects name,quantity,quantity_type,cost_price to be entered through JSON object or a Form data.The name needs to be UNIQUE
and Django adds a primary key by name "id" by default.The quantity_type contains three choices only in which you can enter a single one either 'kg' for
kilogram ,'lt' for litre and "_" for only numbers.

**Get list of all Ingredients**

URL - http://127.0.0.1:8000/ingredients/   REQUEST-TYPE =[GET]:
This  returns a Json value containing the list of all ingredients.

**Getting details of a single Ingredients**

URL - http://127.0.0.1:8000/ingredients/id/ REQUEST-TYPE =[GET]:
The "id" mentioned in the above url must be an integer referring to the "id" of the ingredient you want to fetch.This returns details of the 
ingredient you mentioned.

**Deleting a single Ingredients**

URL - http://127.0.0.1:8000/ingredients/id/ REQUEST-TYPE =[DELETE]:
The "id" mentioned in the above url must be an integer referring to the "id" of the ingredient you want to fetch.This deletes the 
ingredient you mentioned.



## OPERATIONS ON MENU(ACCESSIBLE ONLY TO ADMINS)


**Adding an dish to menu**

URL - http://127.0.0.1:8000/menu/  REQUEST-TYPE =[POST] :
This uses POST request and expects name , quantity , description , cost_price , selling_price , ingredients to be entered through JSON object or a Form data.The name needs to be UNIQUE
and Django adds a primary key by name "id" by default.The ingredients field can contain multiple ingredients id.

**Get list of all dishes(Available to CUSTOMER also)**

URL - http://127.0.0.1:8000/menu/   REQUEST-TYPE =[GET]:
This  returns a Json value containing the list of details of all  dishes.
*Note-This API depend on the type of User logged in. If the Customer user is logged in than this will the name and prices only*

**Getting details of a single Dish**

URL - http://127.0.0.1:8000/menu/id/ REQUEST-TYPE =[GET]:
The "id" mentioned in the above url must be an integer referring to the "id" of the Dish you want to fetch.This returns details of the 
Dish you mentioned.

**Deleting a single Dish**

URL - http://127.0.0.1:8000/ingredients/id/ REQUEST-TYPE =[DELETE]:
The "id" mentioned in the above url must be an integer referring to the "id" of the Dish you want to fetch.This deletes the 
Dish you mentioned

## OPERATIONS ON ORDER(ACCESSIBLE TO THE CUSTOMER )


**Adding/Placing an order **

URL - http://127.0.0.1:8000/order/  REQUEST-TYPE =[POST] :
This uses POST request and expects orderby,items_ordered to be entered through JSON object or a Form data.Django adds a primary key by name "id" by default.
The items_ordered field can contain multiple dishes id.


**Getting details of a single Order **

URL - http://127.0.0.1:8000/order/id/ REQUEST-TYPE =[GET]:
The "id" mentioned in the above url must be an integer referring to the "id" of the Order you want to fetch.This returns details of the 
Order you mentioned.

**Deleting a single Order **

URL - http://127.0.0.1:8000/order/ REQUEST-TYPE =[DELETE]:
The "id" mentioned in the above url must be an integer referring to the "id" of the Order you want to delete.This deletes the 
Order you mentioned

**Order History **

URL - http://127.0.0.1:8000/order/history/ REQUEST-TYPE =[GET]:
This will return the all the orders placed by the Customer making the request.(Latest first) 



