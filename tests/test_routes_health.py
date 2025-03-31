# tests/test_routes_health.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    # The endpoint might return 200 or 503 based on whether Elasticsearch (dummy or real) is reachable.
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
