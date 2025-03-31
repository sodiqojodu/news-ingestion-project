# tests/test_routes_websocket.py
import json
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_websocket_endpoint():
    with client.websocket_connect("/ws") as websocket:
        news_item = {
            "timestamp": datetime.now().isoformat(),
            "source": "ws-test",
            "type": "article",
            "content": "WebSocket test content"
        }
        websocket.send_text(json.dumps(news_item))
        response = websocket.receive_text()
        # Expect a confirmation message; adjust as per your implementation.
        assert "News item received" in response
