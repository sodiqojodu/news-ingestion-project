# routes/health.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ingestion_service import NewsIngestionService
import logging

router = APIRouter()
ingestion_service = NewsIngestionService()
logger = logging.getLogger("news_ingestion.routes.health")

@router.get("/health")
async def health_check():
    try:
        healthy = await ingestion_service.es_client.ping()
        if healthy:
            return JSONResponse(status_code=200, content={"status": "healthy"})
        else:
            return JSONResponse(status_code=503, content={"status": "unhealthy"})
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(status_code=503, content={"status": "unhealthy"})
