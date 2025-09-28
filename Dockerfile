# Dockerfile
FROM python:3.12-slim

# Install system dependencies (optional: for lxml if you prefer it over pure bs4)
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Default command (can be overridden in docker-compose)
CMD ["python", "main.py"]
