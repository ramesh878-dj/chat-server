web: gunicorn backendapi.wsgi:application --log-file -
web2: daphne backendapi.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
