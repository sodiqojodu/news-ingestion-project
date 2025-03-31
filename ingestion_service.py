# # ingestion_service.py
# import logging
# from models import NewsItem, SearchQuery
# from elastic_client import ElasticClient

# logger = logging.getLogger("news_ingestion.ingestion_service")

# class NewsIngestionService:
#     def __init__(self, index: str = "news"):
#         self.index = index
#         self.es_client = ElasticClient()
    
#     async def ingest(self, news_item: NewsItem) -> None:
#         document = news_item.dict()
#         await self.es_client.index_news(index=self.index, document=document)
    
#     async def search(self, query: SearchQuery):
#         must_clauses = []
#         if query.keyword:
#             must_clauses.append({
#                 "match": {"content": query.keyword}
#             })
#         if query.source:
#             must_clauses.append({
#                 "term": {"source": query.source}
#             })
#         filter_clauses = []
#         if query.start_time or query.end_time:
#             range_filter = {"range": {"timestamp": {}}}
#             if query.start_time:
#                 range_filter["range"]["timestamp"]["gte"] = query.start_time.isoformat()
#             if query.end_time:
#                 range_filter["range"]["timestamp"]["lte"] = query.end_time.isoformat()
#             filter_clauses.append(range_filter)
        
#         body = {
#             "query": {
#                 "bool": {
#                     "must": must_clauses,
#                     "filter": filter_clauses
#                 }
#             },
#             "sort": [{"timestamp": {"order": "desc"}}]
#         }
#         result = await self.es_client.search_news(index=self.index, body=body)
#         hits = result["hits"]["hits"]
#         logger.info(f"Search returned {len(hits)} results")
#         return [hit["_source"] for hit in hits]

#     async def close(self):
#         await self.es_client.close()


# ingestion_service.py
import json
from async_lru import alru_cache
import logging
from models import NewsItem, SearchQuery
from elastic_client import ElasticClient

logger = logging.getLogger("news_ingestion.ingestion_service")

class NewsIngestionService:
    def __init__(self, index: str = "news"):
        self.index = index
        self.es_client = ElasticClient()
    
    async def ingest(self, news_item: NewsItem) -> None:
        document = news_item.dict()
        await self.es_client.index_news(index=self.index, document=document)
    
    # This method caches search results for a given set of parameters.
    @alru_cache(maxsize=128)
    async def cached_search(
        self, 
        keyword: str = None, 
        source: str = None, 
        start_time: str = None, 
        end_time: str = None
    ) -> list:
        # Build the Elasticsearch query dynamically
        must_clauses = []
        if keyword:
            must_clauses.append({"match": {"content": keyword}})
        if source:
            must_clauses.append({"term": {"source": source}})
        
        filter_clauses = []
        if start_time or end_time:
            range_filter = {"range": {"timestamp": {}}}
            if start_time:
                range_filter["range"]["timestamp"]["gte"] = start_time
            if end_time:
                range_filter["range"]["timestamp"]["lte"] = end_time
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
    
    # This is the public search method that calls the cached version.
    async def search(self, query: SearchQuery) -> list:
        # Pass parameters as strings (or serialized values) to ensure caching works as expected.
        # For datetime fields, you might convert them to ISO format.
        keyword = query.keyword if query.keyword else ""
        source = query.source if query.source else ""
        start_time = query.start_time.isoformat() if query.start_time else ""
        end_time = query.end_time.isoformat() if query.end_time else ""
        return await self.cached_search(keyword, source, start_time, end_time)

    async def close(self):
        await self.es_client.close()
