FROM python:3.10-alpine AS builder

RUN apk add update && \
    apk add musl-dev libpq-dev gcc

RUN python -m venv /opt/venv

ENV PATH = '/opt/venv/bin:$PATH'

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-alpine

WORKDIR /app

RUN apk update && \
    apk add libpq-dev

COPY --from=builder /opt/venv /opt/venv

ENV PATH="opt/venv/bin:$PATH"

CMD ["python", "app.py"]
