#!/bin/bash
set -e

case "$1" in
    web)
        python manage.py migrate --noinput
        python manage.py super_user_creation --username root --password root --preserve  --noinput
        python manage.py runserver 0.0.0.0:8080
        ;;
    celery)
        celery -A VideoProcessor worker -l INFO
        ;;
    *)
        exec "$@"
esac