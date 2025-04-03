# kafka_client.py
import asyncio
import json
import logging
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from models import NewsItem
from ingestion_service import NewsIngestionService
from config import settings
import logging

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger("news_ingestion.kafka")

class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "news_ingestion"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()
        logger.info("Kafka producer started")

    async def send_news(self, news_item: NewsItem):
        if self.producer is None:
            raise Exception("Producer not started")
        message = news_item.json()
        await self.producer.send_and_wait(self.topic, message.encode("utf-8"))
        logger.info("News item sent to Kafka")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "news_ingestion", group_id: str = "news_indexer"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        # Use the same ingestion service for indexing
        self.ingestion_service = NewsIngestionService()

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        logger.info("Kafka consumer started")

    async def consume(self):
        try:
            async for msg in self.consumer:
                data = msg.value.decode("utf-8")
                news_data = json.loads(data)
                news_item = NewsItem(**news_data)
                # Index the news item into Elasticsearch
                await self.ingestion_service.ingest(news_item, use_kafka=False)
                logger.info("News item indexed from Kafka")
        except Exception as e:
            logger.error(f"Error consuming Kafka messages: {e}")

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")
