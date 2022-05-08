FROM python:3.8.13-slim
RUN mkdir /usr/app
WORKDIR /usr/app
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]