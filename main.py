# main.py
import asyncio
import uvicorn
import logging
from fastapi import FastAPI
from config import settings
from routes import ingestion, search, websocket, health
from udp_server import start_udp_server
from ingestion_service import NewsIngestionService
#import ingestion_service as ig

# Configure logging for production
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger("news_ingestion.main")

app = FastAPI(title="Production Grade News Ingestion Service")

# Include API routers
app.include_router(ingestion.router)
app.include_router(search.router)
app.include_router(websocket.router)
app.include_router(health.router)

# Create a shared instance of the ingestion service.
ingestion_service = NewsIngestionService()

@app.on_event("startup")
async def startup_event():
    # Start the UDP server as a background task.
    asyncio.create_task(start_udp_server(settings.UDP_HOST, settings.UDP_PORT, ingestion_service))
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    await ingestion_service.close()
    logger.info("Application shutdown complete")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.SERVICE_PORT, log_level=settings.LOG_LEVEL.lower())
