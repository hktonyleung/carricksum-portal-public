python manage.py migrate &
daphne carricksum-portal.asgi:application --port 8000 --bind 0.0.0.0 &
celery -A carricksum-portal worker -l info