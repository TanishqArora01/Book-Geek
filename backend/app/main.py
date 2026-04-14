"""FastAPI application for BookGeek-AI."""
from contextlib import asynccontextmanager
from typing import Any, Literal
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import Config
from app.core.logger import logger
from app.core.models import (
    BookInfo,
    ErrorResponse,
    HealthResponse,
    RecommendResponse,
    SearchResult,
)
from app.services.recommendation_engine import RecommendationEngine

# Global recommendation engine instance
engine: RecommendationEngine | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    global engine

    # Startup: Load models
    logger.info("Starting BookGeek-AI application...")
    Config.ensure_directories()

    engine = RecommendationEngine()
    if not engine.load_trained_models():
        logger.warning(
            "No pre-trained models found. "
            "Please train models first using the training script."
        )

    yield

    # Shutdown
    logger.info("Shutting down BookGeek-AI application...")


# Create FastAPI app
app = FastAPI(
    title="BookGeek-AI",
    description="AI-powered book recommendation system",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _structured_error_response(
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    """Create a consistent API error shape while keeping `detail` compatibility."""
    payload = ErrorResponse(
        detail=message,
        error={
            "code": code,
            "message": message,
            "details": details,
        },
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    request_id = str(uuid4())
    logger.warning(f"Validation error for {request.url.path} (request_id={request_id}): {exc.errors()}")
    return _structured_error_response(
        status_code=422,
        code="VALIDATION_ERROR",
        message="Request validation failed",
        details={"errors": exc.errors(), "request_id": request_id},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    request_id = str(uuid4())
    detail = str(exc.detail)
    logger.warning(
        f"HTTP error on {request.url.path} status={exc.status_code} (request_id={request_id}): {detail}"
    )
    return _structured_error_response(
        status_code=exc.status_code,
        code="HTTP_ERROR",
        message=detail,
        details={"request_id": request_id},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    request_id = str(uuid4())
    logger.exception(f"Unhandled error on {request.url.path} (request_id={request_id})")
    return _structured_error_response(
        status_code=500,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected server error occurred",
        details={"request_id": request_id},
    )


@app.get("/api/popular", response_class=JSONResponse, response_model=list[BookInfo])
async def get_popular_books() -> list[dict[str, Any]]:
    """Get popular books."""
    popular_books = []
    if engine and engine.is_trained:
        popular_books = engine.get_popular_books(limit=10)
    return popular_books


@app.post("/api/recommend", response_class=JSONResponse, response_model=RecommendResponse)
async def recommend(
    book_title: str = Form(...),
    method: Literal["hybrid", "collaborative", "content"] = Form(default="hybrid")
) -> dict[str, Any]:
    """Get book recommendations."""
    normalized_title = " ".join(book_title.strip().split())
    if not normalized_title:
        raise HTTPException(status_code=400, detail="Book title cannot be empty")

    recommendations: list[dict[str, Any]] = []
    selected_book: dict[str, Any] | None = None

    if not engine or not engine.is_trained:
        logger.warning("Recommendation requested while engine is not ready")
        return {
            "recommendations": recommendations,
            "book_title": normalized_title,
            "method": method,
            "selected_book": selected_book
        }

    try:
        # Get selected book details
        selected_book = engine.get_book_info(normalized_title)
        if not isinstance(selected_book, dict):
            selected_book = None

        # Get recommendations
        recommendations = engine.get_recommendations(
            book_title=normalized_title,
            method=method,
            top_n=10
        )
        logger.info(
            f"Generated {len(recommendations)} {method} recommendations "
            f"for '{normalized_title}'"
        )
    except Exception as exc:
        logger.exception("Recommendation request failed")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations") from exc

    return {
        "recommendations": recommendations,
        "book_title": normalized_title,
        "method": method,
        "selected_book": selected_book
    }


@app.get("/api/search_books", response_class=JSONResponse, response_model=list[SearchResult])
async def search_books(
    query: str = Query(default="", max_length=120)
) -> list[dict[str, Any]]:
    """
    Search for books by title.
    """
    normalized_query = " ".join(query.strip().split())
    if len(normalized_query) < 2:
        return []

    if not engine or not engine.is_trained:
        logger.warning("Engine not ready for search")
        return []

    query_lower = normalized_query.lower()

    # Search in books_content
    books_content = engine.processed_data["books_content"]
    matching_books = books_content[
        books_content["title"].str.lower().str.contains(
            query_lower, na=False
        )
    ]

    # If not enough results, search in books
    if len(matching_books) < 5:
        books = engine.processed_data["books"]
        additional = books[
            books["title"].str.lower().str.contains(query_lower, na=False)
        ]
        matching_books = pd.concat(
            [matching_books, additional]
        ).drop_duplicates("title")

    results = []
    for _, row in matching_books.head(9).iterrows():
        img_url = row["img_url"]
        if not isinstance(img_url, str) or not img_url.startswith("http"):
            img_url = Config.DEFAULT_IMAGE_URL

        results.append({
            "title": row["title"],
            "author": row["author"],
            "image_url": img_url
        })

    logger.debug(f"Search for '{normalized_query}' returned {len(results)} results")
    return results


@app.get("/api/health", response_model=HealthResponse)
async def health_check() -> dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "models_loaded": engine.is_trained if engine else False,
        "version": "2.0.0"
    }


# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    )
