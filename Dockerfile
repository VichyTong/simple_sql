FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN apt-get update

RUN apt-get -y install postgresql

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
