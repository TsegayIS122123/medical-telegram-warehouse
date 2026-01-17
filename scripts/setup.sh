#!/bin/bash

# Setup script for medical-telegram-warehouse

echo "Setting up Medical Telegram Warehouse Project..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "Creating data directories..."
mkdir -p data/raw/images data/raw/telegram_messages data/processed data/outputs logs

# Create .env file from template if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your credentials"
fi

# Initialize dbt project structure
echo "Initializing dbt project structure..."
cd medical_warehouse
mkdir -p models/staging models/marts models/intermediate tests/custom seeds macros snapshots

# Create basic dbt files if they don't exist
if [ ! -f dbt_project.yml ]; then
    cat > dbt_project.yml << 'EOF'
name: 'medical_warehouse'
version: '1.0.0'
config-version: 2

profile: 'medical_warehouse'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  medical_warehouse:
    materialized: table
    staging:
      materialized: view
    marts:
      materialized: table
EOF
fi

echo "Setup complete! 🎉"
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Start services: docker-compose up -d"
echo "3. Run tests: pytest tests/ -v"