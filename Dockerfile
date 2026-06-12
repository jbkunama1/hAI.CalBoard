FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests flask-cors gunicorn
COPY app/ .
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--reload", "server:app"]
