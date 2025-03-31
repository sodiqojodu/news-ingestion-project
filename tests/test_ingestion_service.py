# tests/test_ingestion_service.py
import pytest
from datetime import datetime
from ingestion_service import NewsIngestionService
from models import NewsItem, SearchQuery

# Create a dummy ElasticClient to simulate responses.
# tests/test_ingestion_service.py

# tests/test_ingestion_service.py

class DummyElasticClient:
    async def index(self, index, document):
        return {"_id": "dummy_id"}

    # IMPORTANT: Name must match the production code usage
    async def search(self, index, body):
        return {
            "hits": {
                "hits": [{
                    "_source": {
                        "timestamp": "2025-03-29T00:00:00",
                        "source": "dummy",
                        "type": "article",
                        "content": "dummy content"
                    }
                }]
            }
        }

    async def ping(self):
        return True

    async def close(self):
        pass

@pytest.fixture
def dummy_ingestion_service():
    service = NewsIngestionService()
    # Patch the internal 'client' with our DummyElasticClient
    service.es_client.client = DummyElasticClient()
    return service


@pytest.fixture
def dummy_ingestion_service():
    service = NewsIngestionService()
    # Patch the internal 'client' with our DummyElasticClient
    service.es_client.client = DummyElasticClient()
    return service


@pytest.mark.asyncio
async def test_ingest(dummy_ingestion_service):
    news_item = NewsItem(
        timestamp=datetime.now(),
        source="test",
        type="headline",
        content="Test content"
    )
    # Should not raise an exception.
    await dummy_ingestion_service.ingest(news_item)

@pytest.mark.asyncio
async def test_search(dummy_ingestion_service):
    query = SearchQuery(keyword="dummy", source="dummy")
    results = await dummy_ingestion_service.search(query)
    assert isinstance(results, list)
    assert len(results) > 0
    assert results[0]["source"] == "dummy"
