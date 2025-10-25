# Dockerfile para Model Watcher
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    httpx==0.26.0 \
    python-dotenv==1.0.0

# Copy watcher script
COPY check_models.py .

# Run watcher
CMD ["python", "check_models.py"]
