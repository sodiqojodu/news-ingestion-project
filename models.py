# models.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NewsItem(BaseModel):
    timestamp: datetime = Field(..., description="ISO format timestamp")
    source: str = Field(..., description="Origin of the news")
    type: str = Field(..., description="e.g., headline, article, scraped, pdf")
    content: str = Field(..., description="The main text or content of the news")

class SearchQuery(BaseModel):
    start_time: Optional[datetime] = Field(None, description="Start of timestamp range")
    end_time: Optional[datetime] = Field(None, description="End of timestamp range")
    keyword: Optional[str] = Field(None, description="Keyword for full-text search")
    source: Optional[str] = Field(None, description="Filter by news source")
