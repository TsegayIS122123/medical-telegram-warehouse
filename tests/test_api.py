import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Medical Telegram Warehouse API"
    assert "endpoints" in data

def test_health_endpoint():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "medical-telegram-warehouse"}

def test_docs_endpoint():
    """Test that docs endpoint exists."""
    response = client.get("/docs")
    assert response.status_code == 200
