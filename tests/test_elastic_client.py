# tests/test_elastic_client.py
import pytest
import asyncio
from elastic_client import ElasticClient
from elasticsearch import ElasticsearchException

# Create a dummy asynchronous Elasticsearch client.
class DummyAsyncElasticsearch:
    async def index(self, index, document):
        return {"_id": "dummy_id"}
    async def search(self, index, body):
        return {"hits": {"hits": [{"_source": {"dummy": "data"}}]}}
    async def ping(self):
        return True
    async def close(self):
        pass

@pytest.fixture
def dummy_es(monkeypatch):
    # Patch ElasticClient.__init__ so that self.client uses our dummy client.
    def dummy_init(self):
        self.client = DummyAsyncElasticsearch()
    monkeypatch.setattr(ElasticClient, "__init__", dummy_init)
    return ElasticClient()

@pytest.mark.asyncio
async def test_index_news(dummy_es):
    # This test ensures that indexing completes without exception.
    result = await dummy_es.index_news("news", {"key": "value"})
    # In our implementation, index_news logs the result; no return value is expected.
    assert result is None

@pytest.mark.asyncio
async def test_search_news(dummy_es):
    result = await dummy_es.search_news("news", {"query": {"match_all": {}}})
    assert result["hits"]["hits"][0]["_source"]["dummy"] == "data"

