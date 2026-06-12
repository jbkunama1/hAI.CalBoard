FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests flask-cors gunicorn werkzeug
RUN mkdir -p /data/uploads
COPY app/ .
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--reload", "--timeout", "60", "server:app"]
