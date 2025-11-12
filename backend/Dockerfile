FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY api.py .
COPY weights/final.pt ./weights/final.pt

# Create results directory
RUN mkdir -p /app/results

# Expose port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
