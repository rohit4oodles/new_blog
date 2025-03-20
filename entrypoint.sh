#!/bin/bash

until nc -z -v -w30 db 3306; do
  echo "Waiting for MySQL connection..."
  sleep 1
done

# Run migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
