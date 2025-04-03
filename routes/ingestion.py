
# routes/ingestion.py
from fastapi import APIRouter, status
from models import NewsItem
from globals_kafka import kafka_producer  # <--- Import from here
import logging

router = APIRouter()
logger = logging.getLogger("news_ingestion.routes.ingestion")

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_news(item: NewsItem):
    await kafka_producer.send_news(item)
    return {"status": "accepted", "message": "News item is being sent to Kafka"}