FROM python:3.10
WORKDIR /opt/api_django
COPY . /opt/api_django
RUN pip install django dj-database-url
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.8000"]