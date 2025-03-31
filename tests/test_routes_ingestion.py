# tests/test_routes_ingestion.py
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_ingest_endpoint():
    news_item = {
        "timestamp": datetime.now().isoformat(),
        "source": "test",
        "type": "headline",
        "content": "Testing ingestion"
    }
    response = client.post("/ingest", json=news_item)
    assert response.status_code == 202
    json_resp = response.json()
    assert json_resp["status"] == "accepted"
