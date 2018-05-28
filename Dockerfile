 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 RUN python3 service_TM/manage.py makemigrations
 RUN python3 service_TM/manage.py migrate
 ADD . /code/
