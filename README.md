# Real-time News Ingestion System

This project is a production-grade, real-time news ingestion system built with FastAPI. It ingests various news content formats (e.g., headlines, full-text articles, scraped content, documents) via REST API, WebSocket, and UDP, stores the data in Elasticsearch, and provides a query API for fast retrieval. An optional in-memory cache is implemented using `async_lru` to speed up frequently queried news articles.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Database/Storage Choice and Trade-offs](#database-storage-choice-and-trade-offs)
- [Indexing Strategy](#indexing-strategy)
- [Scaling Considerations](#scaling-considerations)
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
  
- **Database:**  
  Elasticsearch is used as the backend database because of its high write/read throughput, full-text search capabilities, and scalability.

- **Query API:**  
  Provides a `/search` endpoint that supports complex queries based on timestamp range, keywords, and source filtering.

---

## Database/Storage Choice and Trade-offs

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
  Deploy multiple instances behind a load balancer.
- **Message Queues:**  
  For extremely high ingestion rates, integrate a broker like Kafka or RabbitMQ.
- **Caching:**  
  In-memory caching with `async_lru` is used to speed up frequently requested queries.

---

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/news-ingestion-system.git
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