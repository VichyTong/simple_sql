FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN sudo apt-get update

RUN sudo apt-get -y install postgresql

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
