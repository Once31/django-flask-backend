FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app/main
COPY requirements.txt /app/main/requirements.txt
RUN pip install -r requirements.txt
COPY . /app/main