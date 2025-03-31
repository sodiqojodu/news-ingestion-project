# routes/websocket.py
import json
import asyncio
from fastapi import APIRouter, WebSocket
from models import NewsItem
from ingestion_service import NewsIngestionService
import logging

router = APIRouter()
ingestion_service = NewsIngestionService()
logger = logging.getLogger("news_ingestion.routes.websocket")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    try:
        while True:
            data = await websocket.receive_text()
            try:
                item_data = json.loads(data)
                news_item = NewsItem(**item_data)
                asyncio.create_task(ingestion_service.ingest(news_item))
                await websocket.send_text("News item received")
            except Exception as ex:
                logger.error(f"Error processing WebSocket message: {ex}")
                await websocket.send_text(f"Error: {ex}")
    except Exception as e:
        logger.error(f"WebSocket connection closed with error: {e}")
    finally:
        await websocket.close()
