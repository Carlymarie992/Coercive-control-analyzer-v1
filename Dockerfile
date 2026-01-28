# Dockerfile for Coercive Control Analysis

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/output /app/temp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data
ENV OUTPUT_DIR=/app/output
ENV TEMP_DIR=/app/temp

# Set secure permissions
RUN chmod 700 /app/data /app/output /app/temp

# Create non-root user for security
RUN useradd -m -u 1000 analyzer && \
    chown -R analyzer:analyzer /app

USER analyzer

# Default command
CMD ["python", "analyze.py", "--help"]
