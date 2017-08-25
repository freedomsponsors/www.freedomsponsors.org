#!/bin/bash
cd /app
export DJANGO_STATIC_ROOT=/uwsgi/static
./manage.py collectstatic --noinput
./manage.py migrate --noinput
uwsgi --ini /uwsgi.ini
