# udp_server.py
import asyncio
import json
import logging
from models import NewsItem
from ingestion_service import NewsIngestionService

logger = logging.getLogger("news_ingestion.udp_server")

class UDPHandler(asyncio.DatagramProtocol):
    def __init__(self, ingestion_service: NewsIngestionService):
        self.ingestion_service = ingestion_service

    def datagram_received(self, data, addr):
        try:
            data_str = data.decode("utf-8")
            item_data = json.loads(data_str)
            # Process the valid JSON packet
            asyncio.create_task(self.ingestion_service.ingest(item_data))
            logger.info(f"UDP packet processed from {addr}")
        except UnicodeDecodeError:
            logger.error(f"Invalid UTF-8 data from {addr}. Skipping.")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON data from {addr}. Skipping.")


async def start_udp_server(host: str, port: int, ingestion_service: NewsIngestionService):
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: UDPHandler(ingestion_service),
        local_addr=(host, port)
    )
    logger.info(f"UDP server listening on {host}:{port}")
    try:
        # Keep running indefinitely
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.info("UDP server shutting down")
    finally:
        transport.close()
