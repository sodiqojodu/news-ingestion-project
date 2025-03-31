# tests/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_app_running():
    response = client.get("/health")
    # Health endpoint should be reachable.
    assert response.status_code in [200, 503]
