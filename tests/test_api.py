import pytest
import sys
import os

# Add the parent directory to Python path so we can import api
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Medical Telegram Analytics API"
    assert "endpoints" in data

def test_health_endpoint():
    """Test health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data

def test_docs_endpoint():
    """Test that docs endpoint exists."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_top_products_endpoint():
    """Test top products endpoint."""
    response = client.get("/api/reports/top-products?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_search_messages_endpoint():
    """Test search messages endpoint."""
    response = client.get("/api/search/messages?query=test&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)