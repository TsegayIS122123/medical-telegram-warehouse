@echo off
echo Setting up Medical Telegram Warehouse Project...

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Create data directories
echo Creating data directories...
if not exist "data\raw\images" mkdir data\raw\images
if not exist "data\raw\telegram_messages" mkdir data\raw\telegram_messages
if not exist "data\processed" mkdir data\processed
if not exist "data\outputs" mkdir data\outputs
if not exist "logs" mkdir logs

:: Create .env file from template if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your credentials
)

:: Initialize dbt project structure
echo Initializing dbt project structure...
cd medical_warehouse
if not exist "models\staging" mkdir models\staging
if not exist "models\marts" mkdir models\marts
if not exist "models\intermediate" mkdir models\intermediate
if not exist "tests\custom" mkdir tests\custom
if not exist "seeds" mkdir seeds
if not exist "macros" mkdir macros
if not exist "snapshots" mkdir snapshots

:: Create basic dbt files if they don't exist
if not exist "dbt_project.yml" (
    echo name: 'medical_warehouse' > dbt_project.yml
    echo version: '1.0.0' >> dbt_project.yml
    echo config-version: 2 >> dbt_project.yml
    echo. >> dbt_project.yml
    echo profile: 'medical_warehouse' >> dbt_project.yml
    echo. >> dbt_project.yml
    echo model-paths: ["models"] >> dbt_project.yml
    echo analysis-paths: ["analyses"] >> dbt_project.yml
    echo test-paths: ["tests"] >> dbt_project.yml
    echo seed-paths: ["seeds"] >> dbt_project.yml
    echo macro-paths: ["macros"] >> dbt_project.yml
    echo snapshot-paths: ["snapshots"] >> dbt_project.yml
    echo. >> dbt_project.yml
    echo target-path: "target" >> dbt_project.yml
    echo clean-targets: >> dbt_project.yml
    echo   - "target" >> dbt_project.yml
    echo   - "dbt_packages" >> dbt_project.yml
    echo. >> dbt_project.yml
    echo models: >> dbt_project.yml
    echo   medical_warehouse: >> dbt_project.yml
    echo     materialized: table >> dbt_project.yml
    echo     staging: >> dbt_project.yml
    echo       materialized: view >> dbt_project.yml
    echo     marts: >> dbt_project.yml
    echo       materialized: table >> dbt_project.yml
)

cd ..
echo Setup complete! 🎉
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Start services: docker-compose up -d
echo 3. Run tests: pytest tests/ -v
pause