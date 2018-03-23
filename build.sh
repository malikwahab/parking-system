python manage.py makemigrations
python manage.py migrate
gunicorn parkingsystem.wsgi --log-file=-