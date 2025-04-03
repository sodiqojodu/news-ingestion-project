
# main.py
import asyncio
import uvicorn
import logging
from fastapi import FastAPI
from config import settings
from routes import ingestion, search, websocket, health
from ingestion_service import NewsIngestionService
from udp_server import start_udp_server
from globals_kafka import kafka_producer, kafka_consumer  # Import here, not the other way around

logger = logging.getLogger("news_ingestion.main")
app = FastAPI(title="Production Grade News Ingestion Service with Kafka")

# Include your routers
app.include_router(ingestion.router)
app.include_router(search.router)
app.include_router(websocket.router)
app.include_router(health.router)

# Shared ingestion service
ingestion_service = NewsIngestionService()

@app.on_event("startup")
async def startup_event():
    # Start UDP server
    asyncio.create_task(start_udp_server(settings.UDP_HOST, settings.UDP_PORT, ingestion_service))

    # Start Kafka producer
    await kafka_producer.start()

    # Start Kafka consumer
    asyncio.create_task(kafka_consumer.start())
    asyncio.create_task(kafka_consumer.consume())

    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    await ingestion_service.close()
    await kafka_producer.stop()
    await kafka_consumer.stop()
    logger.info("Application shutdown complete")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.SERVICE_PORT, log_level=settings.LOG_LEVEL.lower())
