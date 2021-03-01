release : python manage.py makemiragrations --no-input
release : python manage.py migrate --no-input

web: gunicorn Bakery.wsgi
