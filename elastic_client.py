# elastic_client.py
import logging
from elasticsearch import AsyncElasticsearch
from elastic_transport import TransportError

from config import settings

logger = logging.getLogger("news_ingestion.elastic")

class ElasticClient:
    def __init__(self):
        self.client = AsyncElasticsearch(
             hosts=["https://localhost:9200"],
             basic_auth=("elastic", "BsLIqRN5TxTQGeOQl3l-"),
             verify_certs=False 
            )

    async def index_news(self, index: str, document: dict) -> None:
        try:
            response = await self.client.index(index=index, document=document)
            logger.info(f"Indexed document {response.get('_id')}")
        except TransportError as e:
            logger.error(f"Failed to index document: {e}")
            raise

    async def search_news(self, index: str, body: dict) -> dict:
        try:
            result = await self.client.search(index=index, body=body)
            return result
        except TransportError as e:
            logger.error(f"Search error: {e}")
            raise

    async def ping(self) -> bool:
        try:
            return await self.client.ping()
        except Exception as e:
            logger.error(f"Ping failed: {e}")
            return False

    async def close(self):
        await self.client.close()

