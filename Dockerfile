FROM python:3.10-alpine

COPY requirements.txt .

RUN apk update --no-cache \
&& apk add build-base postgresql-dev libpq --no-cache --virtual .build-deps \
&& pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r /requirements.txt

WORKDIR /app/

COPY . /app/

CMD ["python", "app.py"]
