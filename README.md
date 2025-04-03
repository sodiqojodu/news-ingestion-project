# Real-time News Ingestion System

This project is a production-grade, real-time news ingestion system built with FastAPI. It ingests various news content formats (e.g., headlines, full-text articles, scraped content, documents) via REST API, WebSocket, and UDP, and leverages Kafka for decoupled, high-throughput message buffering. The data is then indexed in Elasticsearch for efficient full-text search and fast retrieval. An in-memory cache (using async_lru) is implemented to speed up frequently queried news articles.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Database/Storage Choice and Trade-offs](#database-storage-choice-and-trade-offs)
- [Indexing Strategy](#indexing-strategy)
- [Scaling Considerations](#scaling-considerations)
- [Additional Enhancement](#Additional Enhancement)
- [Installation and Setup](#installation-and-setup)
- [How to Run the System](#how-to-run-the-system)
- [How to Query the System](#how-to-query-the-system)
- [Optional: In-Memory Caching](#optional-in-memory-caching)
- [Troubleshooting](#troubleshooting)

---

## System Architecture

- **Ingestion Service:**  
  Built using FastAPI with support for:
  - **REST API** (POST `/ingest`)
  - **WebSocket** (for real-time streaming)
  - **UDP Server** (for high-throughput ingestion)

- **Message Broker:**
  Kafka is integrated as a message broker to decouple ingestion from processing. Incoming news items are published to Kafka, allowing the system to buffer bursts of high-volume data and process them asynchronously.

- **Database:**  
  Elasticsearch is used as the backend database because of its high write/read throughput, full-text search capabilities, and scalability.

- **Query API:**  
  Provides a `/search` endpoint that supports complex queries based on timestamp range, keywords, and source filtering.

---

## Database/Storage Choice and Trade-offs
## Why Elasticsearch?
  Elasticsearch was chosen because it best fits the needs of a real-time, high-volume ingestion system:

  **Read/Write Speed:**
  Elasticsearch supports high ingestion rates with its bulk indexing capabilities and provides low-latency search responses, which is crucial for real-time applications.

  **Scalability:**
  It scales horizontally through clustering. As data volume grows, additional nodes can be added to the cluster to handle increased load.

  **Full-text Search Capabilities:**
  Built-in analyzers and query capabilities enable powerful full-text search, which is essential for processing unstructured news data and performing complex queries.

  **CAP Theorem:**
  Elasticsearch is designed to favor availability and partition tolerance, accepting eventual consistency as a trade-off. This fits well with the real-time ingestion use case, where immediate consistency is less critical than availability and performance.

- **Elasticsearch:**
  - **Pros:**  
    - High ingestion rate with bulk indexing capabilities.
    - Powerful built-in full-text search.
    - Horizontal scalability (clustering).
  - **Cons:**  
    - Eventual consistency (not strong consistency).
    - Resource intensive (requires sufficient memory and CPU).
  
- **Trade-offs:**  
  We prioritize low latency and high availability over strict consistency, making Elasticsearch a good fit for real-time news ingestion.

---

## Indexing Strategy

- **Mappings:**  
  Documents are indexed with fields such as:
  - `timestamp` (date field for range queries)
  - `source` (keyword field for exact matches)
  - `type` (to differentiate content types)
  - `content` (text field analyzed for full-text search)
  
- **Auto-Creation:**  
  Elasticsearch auto-creates indices on first document ingestion (or can be manually created if needed).

- **Bulk Indexing:**  
  For high throughput, consider leveraging Elasticsearch’s bulk API.

---

## Scaling Considerations

- **Asynchronous Processing:**  
  FastAPI uses asynchronous endpoints to handle 5,000+ requests per second.
- **Horizontal Scaling:**  
  Deploy multiple instances behind a load balancer to distribute the incoming request load.
- **Message Queues:**  
  Integrating Kafka decouples ingestion from processing, ensuring that bursts of data are buffered and processed asynchronously. This allows the system to handle even higher data loads by offloading processing tasks.
- **Caching:**  
  The use of in-memory caching (via async_lru) reduces repeated queries against Elasticsearch, further improving read performance under high load.
- **Monitoring & Alerts:**  
Integrate monitoring solutions (e.g., Prometheus, Grafana) and logging (e.g., ELK stack) to track system performance and errors in real time.

## Kafka Integration

**Decoupling Ingestion from Processing:**
With Kafka integrated as a message broker, the ingestion service now publishes incoming news items to a Kafka topic. This decouples the ingestion layer from downstream processing, ensuring that the system can absorb bursts of high traffic without overwhelming Elasticsearch.

**Increased Resilience:**
Kafka provides durability and fault tolerance. In case Elasticsearch experiences temporary downtime or delays, the messages remain safely buffered in Kafka until they can be processed.

**Improved Scalability:**
The integration allows you to scale the consumer side independently. You can add more Kafka consumers to handle higher ingestion rates, making the system more scalable for real-time, high-volume data streams.

## Justification for Database Choice (Elasticsearch)
Elasticsearch was chosen for its:

High read/write speeds, enabling real-time processing of news items.

Horizontal scalability, which is critical as data volumes grow.

Native full-text search capabilities, ideal for handling unstructured text and complex queries.

CAP Theorem alignment, prioritizing availability and partition tolerance, which is acceptable for news ingestion where eventual consistency is sufficient.

## How to Scale the System for Higher Data Loads
Increase Kafka Consumers:
As ingestion rates grow, you can add additional consumer instances to process messages in parallel from Kafka.

Scale Elasticsearch Cluster:
Add more nodes to your Elasticsearch cluster to distribute indexing and search load. Use index sharding and replication to optimize performance and data availability.

Load Balancing FastAPI Instances:
Deploy multiple FastAPI instances behind a load balancer to distribute incoming REST/WebSocket/UDP traffic evenly.

Implement Bulk Indexing:
Use Elasticsearch’s bulk indexing API to reduce overhead when processing a high volume of messages.

Enhanced Caching:
Expand in-memory caching strategies to reduce the load on Elasticsearch for frequently queried data.


---

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sodiqojodu/news-ingestion-project.git
   cd news-ingestion-system

2. **Create and Activate a Virtual Environment:**
python -m venv venv
.\venv\Scripts\Activate.ps1


3. **Install Dependencies:** 
pip install -r requirements.txt
Dependencies include: FastAPI, Uvicorn, elasticsearch, async-lru, and others.


4. **Set Up Elasticsearch** 
Using Docker:
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:8.10.0

Confirm with:
curl -k -u "elastic:YOUR_PASSWORD" https://localhost:9200

5. **Set Up Kafka:**
Using Docker Compose, create a docker-compose.yml:
```bash
version: '2'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.2.1
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"
  kafka:
    image: confluentinc/cp-kafka:7.2.1
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

```

Then run:
docker-compose up -d

5. **Install Testing Dependencies:**

   Ensure you have the necessary testing packages installed:
   ```bash
   pip install pytest pytest-asyncio httpx
                                    ################################
                                    #### How to Run the System #####
                                    ################################


1. **Start the FastAPI Application:**
    uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info
    or
    python main.py # This starts the FastAPI service with REST endpoints and the UDP server.


2. **Monitor the Logs:**
    Check that the UDP server is listening on port 9999.
    Ensure that the application logs confirm successful Elasticsearch connections (e.g., ping returns True).

                                    ################################
                                    #### How to Query the System ###
                                    ################################

1. **Swagger UI:**
Open your browser and navigate to http://localhost:8000/docs.

    Health Check:
    Use GET /health to ensure the service is running.

    Ingest Data:
    Use POST /ingest with a JSON body, for example:
    {
        "timestamp": "2025-03-29T18:40:29.534Z",
        "source": "TestSource",
        "type": "headline",
        "content": "This is a test headline."
    }

    Search Data:
    Use POST /search with a JSON body to retrieve relevant news articles. For example:
    
    {
    "query": {
        "match_all": {}
    }
    }

2. **Direct cURL Queries (Optional):**
Index Check:
curl -k -u "elastic:YOUR_PASSWORD" https://localhost:9200/news/_search?pretty

Match All Query:
curl -k -u "elastic:YOUR_PASSWORD" -X POST -H "Content-Type: application/json" \
     -d '{"query": {"match_all": {}}}' https://localhost:9200/news/_search?pretty

POST /ingest
Purpose:
Accepts a news item (e.g., headline, full article, scraped content, or document) and schedules it for indexing into Elasticsearch.

Payload Example:
{
  "timestamp": "2025-03-29T12:00:00",
  "source": "Reuters",
  "type": "headline",
  "content": "Breaking News: Major event in the city."
}

Response:
Returns a status message indicating that the news item is being processed.

curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"timestamp": "2025-03-29T12:00:00", "source": "Reuters", "type": "headline", "content": "Breaking News: Major event in the city."}'

 POST /search
Purpose:
Allows users to query the stored news documents based on a combination of filters such as timestamp range, keyword, and source.

Payload Example:
{
  "start_time": "2025-03-28T00:00:00",
  "end_time": "2025-03-29T23:59:59",
  "keyword": "event",
  "source": "Reuters"
}
Response:
Returns a list of news items that match the criteria. Each item will include fields like timestamp, source, type, and content.

Usage Example (cURL):
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"start_time": "2025-03-28T00:00:00", "end_time": "2025-03-29T23:59:59", "keyword": "event", "source": "Reuters"}'

GET /health
Purpose:
Provides a health check for the service. It verifies that the application is running and that Elasticsearch is reachable.

Response Example:
{
  "status": "healthy"
}
Usage Example (cURL):
curl http://localhost:8000/health

Additional Endpoint: WebSocket /ws
Although not a REST API endpoint, the system also provides a WebSocket endpoint to support real-time ingestion.

Path: /ws

Purpose:
Opens a persistent connection for receiving continuous streams of news items in real time.

Usage:
Connect via a WebSocket client, send JSON-encoded news items, and receive acknowledgment messages.

Troubleshooting
Elasticsearch Connection Issues:
Ensure that your ES_HOST is set correctly (e.g., https://localhost:9200) and that credentials match those in Elasticsearch.

422 Errors:
Validate that your JSON payloads match the expected Pydantic model (e.g., correct timestamp format).

Port Conflicts:
If you see errors related to ports, ensure no other process is using the required ports (8000 for FastAPI, 9999 for UDP, etc.).

Cache Issues:
If using caching, verify that search parameters are serialized correctly so that cache keys are consistent.

Conclusion
This project meets the deliverables by providing:

A robust ingestion service for multiple data formats.

A scalable database implementation using Elasticsearch.

A query API for efficient retrieval of news content.

Detailed documentation on system architect