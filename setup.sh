python manage.py migrate &
python manage.py runserver 0.0.0.0:8000 & 
celery -A carricksum-portal worker -l info