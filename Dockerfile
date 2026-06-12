FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /data/uploads

COPY app/ /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "60", "server:app"]
