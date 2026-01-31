# backend/Dockerfile
FROM python:3.9-slim

# Working directory set karna
WORKDIR /app

# Dependencies install karna
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Pura code copy karna
COPY . /app/

# Port expose karna
EXPOSE 8000

# Server start command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]