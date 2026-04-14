"""Tests for Pydantic models."""
import pytest
from pydantic import ValidationError

from app.core.models import (
    BookInfo,
    BookRecommendation,
    RecommendRequest,
    SearchResponse,
    SearchResult,
)


class TestBookInfo:
    """Test cases for BookInfo model."""

    def test_book_info_valid(self):
        """Test creating a valid BookInfo."""
        book = BookInfo(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            year="1925",
            publisher="Scribner",
            image_url="http://example.com/gatsby.jpg"
        )
        assert book.title == "The Great Gatsby"
        assert book.author == "F. Scott Fitzgerald"
        assert book.year == "1925"
        assert book.publisher == "Scribner"
        assert book.image_url == "http://example.com/gatsby.jpg"

    def test_book_info_minimal(self):
        """Test creating BookInfo with minimal fields."""
        book = BookInfo(
            title="1984",
            author="George Orwell",
            image_url="http://example.com/1984.jpg"
        )
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.year is None
        assert book.publisher is None

    def test_book_info_with_alias(self):
        """Test BookInfo with image_url alias."""
        book = BookInfo(
            title="Test",
            author="Author",
            image_url="http://example.com/test.jpg"
        )
        assert book.image_url == "http://example.com/test.jpg"

    def test_book_info_missing_required(self):
        """Test BookInfo with missing required fields."""
        with pytest.raises(ValidationError):
            BookInfo(title="Test")


class TestBookRecommendation:
    """Test cases for BookRecommendation model."""

    def test_book_recommendation_valid(self):
        """Test creating a valid BookRecommendation."""
        rec = BookRecommendation(
            title="1984",
            author="George Orwell",
            year="1949",
            publisher="Secker & Warburg",
            image_url="http://example.com/1984.jpg",
            score=0.85,
            type="hybrid"
        )
        assert rec.title == "1984"
        assert rec.score == 0.85
        assert rec.type == "hybrid"

    def test_book_recommendation_minimal(self):
        """Test creating BookRecommendation with minimal fields."""
        rec = BookRecommendation(
            title="Test Book",
            author="Test Author",
            image_url="http://example.com/test.jpg",
            score=0.5,
            type="content"
        )
        assert rec.year is None
        assert rec.publisher is None

    def test_book_recommendation_types(self):
        """Test different recommendation types."""
        for rec_type in ["collaborative", "content", "hybrid"]:
            rec = BookRecommendation(
                title="Test",
                author="Author",
                image_url="http://example.com/test.jpg",
                score=0.7,
                type=rec_type
            )
            assert rec.type == rec_type


class TestRecommendRequest:
    """Test cases for RecommendRequest model."""

    def test_recommend_request_valid(self):
        """Test creating a valid RecommendRequest."""
        req = RecommendRequest(
            book_title="The Great Gatsby",
            method="hybrid"
        )
        assert req.book_title == "The Great Gatsby"
        assert req.method == "hybrid"

    def test_recommend_request_default_method(self):
        """Test RecommendRequest with default method."""
        req = RecommendRequest(book_title="Test Book")
        assert req.method == "hybrid"

    def test_recommend_request_different_methods(self):
        """Test RecommendRequest with different methods."""
        for method in ["collaborative", "content", "hybrid"]:
            req = RecommendRequest(book_title="Test", method=method)
            assert req.method == method


class TestSearchResult:
    """Test cases for SearchResult model."""

    def test_search_result_valid(self):
        """Test creating a valid SearchResult."""
        result = SearchResult(
            title="Test Book",
            author="Test Author",
            image_url="http://example.com/test.jpg"
        )
        assert result.title == "Test Book"
        assert result.author == "Test Author"
        assert result.image_url == "http://example.com/test.jpg"

    def test_search_result_missing_field(self):
        """Test SearchResult with missing required field."""
        with pytest.raises(ValidationError):
            SearchResult(title="Test", author="Author")


class TestSearchResponse:
    """Test cases for SearchResponse model."""

    def test_search_response_valid(self):
        """Test creating a valid SearchResponse."""
        results = [
            SearchResult(
                title="Book 1",
                author="Author 1",
                image_url="http://example.com/1.jpg"
            ),
            SearchResult(
                title="Book 2",
                author="Author 2",
                image_url="http://example.com/2.jpg"
            )
        ]
        response = SearchResponse(results=results)
        assert len(response.results) == 2
        assert response.results[0].title == "Book 1"

    def test_search_response_empty(self):
        """Test SearchResponse with empty results."""
        response = SearchResponse(results=[])
        assert len(response.results) == 0

    def test_search_response_single_result(self):
        """Test SearchResponse with single result."""
        result = SearchResult(
            title="Single Book",
            author="Author",
            image_url="http://example.com/single.jpg"
        )
        response = SearchResponse(results=[result])
        assert len(response.results) == 1
