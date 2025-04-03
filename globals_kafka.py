# globals_kafka.py
from kafka_connector import KafkaProducerClient, KafkaConsumerClient

kafka_producer = KafkaProducerClient(
    bootstrap_servers="localhost:9092",
    topic="news_ingestion"
)

kafka_consumer = KafkaConsumerClient(
    bootstrap_servers="localhost:9092",
    topic="news_ingestion",
    group_id="news_indexer"
)
