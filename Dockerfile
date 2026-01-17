FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data/raw/images data/raw/telegram_messages logs

# Initialize dbt project structure
RUN cd medical_warehouse && \
    echo "Creating dbt project structure..." && \
    mkdir -p models/staging models/marts models/intermediate tests/custom seeds macros snapshots

# Expose ports
EXPOSE 8000 3000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
