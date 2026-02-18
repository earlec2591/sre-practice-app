"""Tests for the SRE Practice App.

WHY TESTS MATTER FOR SREs:
Tests are your safety net. They catch bugs BEFORE code reaches production.
In CI/CD, tests run automatically on every push. If a test fails,
the pipeline stops and the bad code never gets deployed.
This is how you prevent incidents.
"""

import json
from app import app


def test_home():
    """Test that the home endpoint returns expected data."""
    # Flask provides a test client so you don't need a running server
    client = app.test_client()
    response = client.get("/")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["app"] == "SRE Practice App"
    assert "version" in data


def test_health():
    """Test the health check endpoint."""
    client = app.test_client()
    response = client.get("/health")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data


def test_metrics():
    """Test that metrics endpoint returns expected fields."""
    client = app.test_client()
    response = client.get("/metrics")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert isinstance(data["cpu_percent"], float)