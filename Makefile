# Makefile
.PHONY: help install dev test run docker-up docker-down clean

help:
	@echo "Available commands:"
	@echo "  make install    Install production dependencies"
	@echo "  make dev        Install development dependencies"
	@echo "  make test       Run tests"
	@echo "  make test-cov   Run tests with coverage"
	@echo "  make run        Run complete pipeline"
	@echo "  make api        Run FastAPI server"
	@echo "  make dashboard  Run Streamlit dashboard"
	@echo "  make docker-up  Start Docker containers"
	@echo "  make docker-down Stop Docker containers"
	@echo "  make clean      Clean temporary files"

install:
	pip install -r requirements.txt

dev: install
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov=api --cov-report=term --cov-report=html

run:
	python run.py

api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

dashboard:
	streamlit run dashboard/app.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +