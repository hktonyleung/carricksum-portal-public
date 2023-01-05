release: python manage.py migrate
web: daphne carricksum-portal.asgi:application --port $PORT --bind 0.0.0.0
worker: celery -A carricksum-portal worker -l info --concurrency 1


