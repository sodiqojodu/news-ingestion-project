# tests/test_routes_search.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_endpoint():
    query = {
        "keyword": "test",
        "source": "test"
    }
    response = client.post("/search", json=query)
    # Since no documents may be indexed in a test run, an empty list is acceptable.
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
