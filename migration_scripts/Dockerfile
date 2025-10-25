# Dockerfile para Migration Tool
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    pymongo==4.6.1 \
    psycopg2-binary==2.9.9 \
    python-dotenv==1.0.0

# Copy migration script
COPY migrate.py .

# Run migration
CMD ["python", "migrate.py"]
