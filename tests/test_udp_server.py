# tests/test_udp_server.py
import asyncio
import json
import pytest
from udp_server import UDPHandler
from models import NewsItem

# A dummy ingestion service to capture ingested news items.
class DummyIngestionService:
    def __init__(self):
        self.ingested_items = []
    async def ingest(self, news_item: NewsItem):
        self.ingested_items.append(news_item)

@pytest.mark.asyncio
async def test_udp_handler():
    dummy_service = DummyIngestionService()
    handler = UDPHandler(dummy_service)
    news_data = {
        "timestamp": "2025-03-29T12:00:00",
        "source": "unit-test",
        "type": "article",
        "content": "UDP test content"
    }
    data_bytes = json.dumps(news_data).encode()
    # Simulate receiving a UDP packet.
    handler.datagram_received(data_bytes, ("127.0.0.1", 12345))
    # Wait shortly to let the asynchronous task complete.
    await asyncio.sleep(0.1)
    assert len(dummy_service.ingested_items) == 1
    item = dummy_service.ingested_items[0]  # 'item' is a dict
    assert item["source"] == "unit-test"

