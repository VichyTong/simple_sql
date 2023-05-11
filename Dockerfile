FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
