# routes/search.py
from fastapi import APIRouter, HTTPException
from models import SearchQuery, NewsItem
from ingestion_service import NewsIngestionService
import logging

router = APIRouter()
ingestion_service = NewsIngestionService()
logger = logging.getLogger("news_ingestion.routes.search")

@router.post("/search", response_model=list[NewsItem])
async def search_news(query: SearchQuery):
    try:
        results = await ingestion_service.search(query)
        return results
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        raise HTTPException(status_code=500, detail="Search error")
