python manage.py makemigrations
python manage.py migrate
gunicorn bucketlist_application.wsgi --log-file=-