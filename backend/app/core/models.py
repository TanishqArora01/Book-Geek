"""Pydantic models for request/response schemas."""
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class BookInfo(BaseModel):
    """Book information schema."""

    title: str
    author: str
    year: Optional[str] = None
    publisher: Optional[str] = None
    image_url: str = Field(alias="image_url")

    model_config = ConfigDict(populate_by_name=True)


class BookRecommendation(BaseModel):
    """Book recommendation schema."""

    title: str
    author: str
    year: Optional[str] = None
    publisher: Optional[str] = None
    image_url: str
    score: float
    type: str  # 'collaborative', 'content', 'hybrid'


class RecommendRequest(BaseModel):
    """Recommendation request schema."""

    book_title: str
    method: str = "hybrid"  # 'collaborative', 'content', 'hybrid'


class SearchResult(BaseModel):
    """Search result schema."""

    title: str
    author: str
    image_url: str


class SearchResponse(BaseModel):
    """Search response schema."""

    results: list[SearchResult]


class RecommendResponse(BaseModel):
    """Recommendation API response schema."""

    recommendations: list[BookRecommendation]
    book_title: str
    method: str
    selected_book: Optional[BookInfo] = None


class HealthResponse(BaseModel):
    """Health-check response schema."""

    status: str
    models_loaded: bool
    version: str


class ErrorInfo(BaseModel):
    """Structured error payload for API failures."""

    code: str
    message: str
    details: Optional[dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response envelope.

    Note: `detail` is preserved for backward compatibility with existing clients.
    """

    detail: str
    error: ErrorInfo
