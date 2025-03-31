# routes/ingestion.py
from fastapi import APIRouter, BackgroundTasks, status
from models import NewsItem
from ingestion_service import NewsIngestionService
import logging

router = APIRouter()
# You could share a single instance or instantiate per router as needed.
ingestion_service = NewsIngestionService()
logger = logging.getLogger("news_ingestion.routes.ingestion")
print("Loaded ingestion router!")


@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_news(item: NewsItem, background_tasks: BackgroundTasks):
    background_tasks.add_task(ingestion_service.ingest, item)
    return {"status": "accepted", "message": "News item is being processed"}
