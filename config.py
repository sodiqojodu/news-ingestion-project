# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    ES_HOST: str = "http://localhost:9200"
    ES_USER="elastic"
    ES_PASSWORD="BsLIqRN5TxTQGeOQl3l-"
    UDP_HOST: str = "0.0.0.0"
    UDP_PORT: int = 9999
    SERVICE_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
