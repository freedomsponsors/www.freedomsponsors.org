FROM python:2.7
RUN pip install uwsgi
RUN apt-get update --fix-missing
RUN apt-get -y install python-dev python-lxml libxslt-dev libpq-dev pgadmin3 libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY djangoproject /usr/src/app
CMD cd /usr/src/app && python manage.py migrate && python manage.py runserver 0.0.0.0:8000