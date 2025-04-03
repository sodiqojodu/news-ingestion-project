
# ingestion_service.py
import logging
from models import NewsItem, SearchQuery
from elastic_client import ElasticClient

logger = logging.getLogger("news_ingestion.ingestion_service")

class NewsIngestionService:
    def __init__(self, index: str = "news"):
        self.index = index
        self.es_client = ElasticClient()
    
    async def ingest(self, news_item: NewsItem, use_kafka: bool = True):
        """
        When use_kafka is True, the message is expected to be sent to Kafka (handled by KafkaProducer).
        When False, the news item is directly indexed into Elasticsearch (used by KafkaConsumer).
        """
        if not use_kafka:
            document = news_item.dict()
            await self.es_client.index_news(index=self.index, document=document)
            logger.info("News item indexed directly")
    
    async def search(self, query: SearchQuery):
        must_clauses = []
        if query.keyword:
            must_clauses.append({
                "match": {"content": query.keyword}
            })
        if query.source:
            must_clauses.append({
                "term": {"source": query.source}
            })
        filter_clauses = []
        if query.start_time or query.end_time:
            range_filter = {"range": {"timestamp": {}}}
            if query.start_time:
                range_filter["range"]["timestamp"]["gte"] = query.start_time.isoformat()
            if query.end_time:
                range_filter["range"]["timestamp"]["lte"] = query.end_time.isoformat()
            filter_clauses.append(range_filter)
        
        body = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": filter_clauses
                }
            },
            "sort": [{"timestamp": {"order": "desc"}}]
        }
        result = await self.es_client.search_news(index=self.index, body=body)
        hits = result["hits"]["hits"]
        logger.info(f"Search returned {len(hits)} results")
        return [hit["_source"] for hit in hits]

    async def close(self):
        await self.es_client.close()
