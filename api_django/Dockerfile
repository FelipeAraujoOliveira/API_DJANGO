FROM python:3.10

WORKDIR /opt/api_django

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ..

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.8000"]