"""Tests for FastAPI endpoints."""
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient


class TestEndpoints:
    """Test cases for FastAPI endpoints."""

    @pytest.fixture
    def mock_engine(self):
        """Create mock recommendation engine."""
        engine = MagicMock()
        engine.is_trained = True
        engine.get_popular_books.return_value = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "image_url": "http://example.com/gatsby.jpg"
            }
        ]
        engine.get_recommendations.return_value = [
            {
                "title": "1984",
                "author": "George Orwell",
                "year": "1949",
                "publisher": "Secker & Warburg",
                "image_url": "http://example.com/1984.jpg",
                "score": 0.85,
                "type": "hybrid"
            }
        ]
        engine.processed_data = {
            "books_content": pd.DataFrame({
                "title": ["The Great Gatsby", "1984"],
                "author": ["F. Scott Fitzgerald", "George Orwell"],
                "img_url": [
                    "http://example.com/gatsby.jpg",
                    "http://example.com/1984.jpg"
                ]
            }),
            "books": pd.DataFrame({
                "title": ["The Great Gatsby", "1984"],
                "author": ["F. Scott Fitzgerald", "George Orwell"],
                "img_url": [
                    "http://example.com/gatsby.jpg",
                    "http://example.com/1984.jpg"
                ]
            }),
            "final_rating": pd.DataFrame({
                "title": ["The Great Gatsby", "1984"],
                "rating": [8, 9]
            })
        }
        return engine

    @pytest.fixture
    def client(self, mock_engine):
        """Create test client with mocked engine."""
        with patch("app.main.engine", mock_engine):
            from app.main import app
            client = TestClient(app)
            yield client

    def test_popular_books_endpoint(self, client):
        """Test popular books API returns successfully."""
        response = client.get("/api/popular")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert len(response.json()) > 0

    def test_recommend_endpoint_hybrid(self, client):
        """Test recommendation endpoint with hybrid method."""
        response = client.post(
            "/api/recommend",
            data={"book_title": "The Great Gatsby", "method": "hybrid"}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "recommendations" in response.json()

    def test_recommend_endpoint_collaborative(self, client):
        """Test recommendation endpoint with collaborative method."""
        response = client.post(
            "/api/recommend",
            data={"book_title": "The Great Gatsby", "method": "collaborative"}
        )

        assert response.status_code == 200

    def test_recommend_endpoint_content(self, client):
        """Test recommendation endpoint with content method."""
        response = client.post(
            "/api/recommend",
            data={"book_title": "The Great Gatsby", "method": "content"}
        )

        assert response.status_code == 200

    def test_search_books_endpoint(self, client):
        """Test search books endpoint."""
        response = client.get("/api/search_books?query=gatsby")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_search_books_empty_query(self, client):
        """Test search books with empty query."""
        response = client.get("/api/search_books?query=")

        assert response.status_code == 200
        assert response.json() == []

    def test_search_books_no_query(self, client):
        """Test search books without query parameter."""
        response = client.get("/api/search_books")

        assert response.status_code == 200
        assert response.json() == []

    def test_health_check(self, client, mock_engine):
        """Test health check endpoint."""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "models_loaded" in data
        assert "version" in data


class TestEndpointsNoEngine:
    """Test endpoints when engine is not available."""

    @pytest.fixture
    def client_no_engine(self):
        """Create test client without engine."""
        with patch("app.main.engine", None):
            from app.main import app
            client = TestClient(app)
            yield client

    def test_popular_without_engine(self, client_no_engine):
        """Test popular books when engine is None."""
        response = client_no_engine.get("/api/popular")
        assert response.status_code == 200
        assert response.json() == []

    def test_recommend_without_engine(self, client_no_engine):
        """Test recommendations when engine is None."""
        response = client_no_engine.post(
            "/api/recommend",
            data={"book_title": "Test", "method": "hybrid"}
        )
        assert response.status_code == 200
        assert response.json()["recommendations"] == []

    def test_search_without_engine(self, client_no_engine):
        """Test search when engine is None."""
        response = client_no_engine.get("/api/search_books?query=test")
        assert response.status_code == 200
        assert response.json() == []

    def test_health_without_engine(self, client_no_engine):
        """Test health check when engine is None."""
        response = client_no_engine.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["models_loaded"] is False


class TestSearchBooksEdgeCases:
    """Test edge cases for search_books endpoint."""

    @pytest.fixture
    def mock_engine_with_invalid_image(self):
        """Create mock engine with invalid image URLs."""
        engine = MagicMock()
        engine.is_trained = True
        engine.processed_data = {
            "books_content": pd.DataFrame({
                "title": ["Test Book"],
                "author": ["Test Author"],
                "img_url": [None]  # Invalid image URL
            }),
            "books": pd.DataFrame({
                "title": ["Another Book"],
                "author": ["Another Author"],
                "img_url": ["invalid-url"]  # Non-http URL
            })
        }
        return engine

    @pytest.fixture
    def client_invalid_image(self, mock_engine_with_invalid_image):
        """Create test client with mock engine having invalid images."""
        with patch("app.main.engine", mock_engine_with_invalid_image):
            from app.main import app
            client = TestClient(app)
            yield client

    def test_search_books_with_invalid_image_url(self, client_invalid_image):
        """Test search books returns default image for invalid URLs."""
        response = client_invalid_image.get("/api/search_books?query=test")

        assert response.status_code == 200
        results = response.json()
        if results:
            for result in results:
                assert "image_url" in result

    @pytest.fixture
    def mock_engine_few_results(self):
        """Create mock engine that returns few results in books_content."""
        engine = MagicMock()
        engine.is_trained = True
        engine.processed_data = {
            "books_content": pd.DataFrame({
                "title": ["Test Book"],
                "author": ["Test Author"],
                "img_url": ["http://example.com/test.jpg"]
            }),
            "books": pd.DataFrame({
                "title": ["Test Book", "Test Book 2", "Test Book 3"],
                "author": ["Author 1", "Author 2", "Author 3"],
                "img_url": [
                    "http://example.com/1.jpg",
                    "http://example.com/2.jpg",
                    "http://example.com/3.jpg"
                ]
            })
        }
        return engine

    @pytest.fixture
    def client_few_results(self, mock_engine_few_results):
        """Create test client for fallback testing."""
        with patch("app.main.engine", mock_engine_few_results):
            from app.main import app
            client = TestClient(app)
            yield client

    def test_search_books_fallback_to_books(self, client_few_results):
        """Test search falls back to books when books_content has few results."""
        response = client_few_results.get("/api/search_books?query=test")

        assert response.status_code == 200


class TestLifespan:
    """Test application lifespan events."""

    def test_lifespan_startup_shutdown(self):
        """Test lifespan context manager for startup and shutdown."""
        import asyncio
        from unittest.mock import patch

        mock_engine = MagicMock()
        mock_engine.load_trained_models.return_value = False

        async def run_lifespan_test():
            with patch("app.main.RecommendationEngine", return_value=mock_engine):
                with patch("app.main.Config.ensure_directories"):
                    from app.main import app, lifespan

                    async with lifespan(app):
                        pass

        asyncio.run(run_lifespan_test())

    def test_lifespan_with_trained_models(self):
        """Test lifespan when models are already trained."""
        import asyncio

        mock_engine = MagicMock()
        mock_engine.load_trained_models.return_value = True

        async def run_lifespan_test():
            with patch("app.main.RecommendationEngine", return_value=mock_engine):
                with patch("app.main.Config.ensure_directories"):
                    from app.main import app, lifespan

                    async with lifespan(app):
                        pass

        asyncio.run(run_lifespan_test())
