"""Tests for recommendation engine."""
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from app.services.recommendation_engine import RecommendationEngine


class TestRecommendationEngine:
    """Test cases for RecommendationEngine class."""

    @pytest.fixture
    def engine(self):
        """Create a fresh engine instance."""
        return RecommendationEngine()

    def test_init(self, engine):
        """Test engine initialization."""
        assert engine.cf_model is None
        assert engine.cb_model is None
        assert engine.hybrid_model is None
        assert engine.processed_data is None
        assert engine.is_trained is False

    def test_get_recommendations_not_trained(self, engine):
        """Test getting recommendations when not trained."""
        result = engine.get_recommendations("Test Book")
        assert result == []

    def test_get_recommendations_invalid_method(self, engine):
        """Test getting recommendations with invalid method."""
        engine.is_trained = True
        engine.cf_model = MagicMock()
        engine.cb_model = MagicMock()
        engine.hybrid_model = MagicMock()
        engine.processed_data = {"books_content": MagicMock(), "books": MagicMock()}

        result = engine.get_recommendations("Test Book", method="invalid")
        assert result == []

    def test_get_recommendations_collaborative(self, engine):
        """Test collaborative recommendations."""
        engine.is_trained = True
        engine.cf_model = MagicMock()
        engine.cf_model.get_recommendations.return_value = [{"title": "Book A"}]
        engine.processed_data = {
            "books_content": MagicMock(),
            "books": MagicMock()
        }

        result = engine.get_recommendations("Test Book", method="collaborative")

        assert result == [{"title": "Book A"}]
        engine.cf_model.get_recommendations.assert_called_once()

    def test_get_recommendations_content(self, engine):
        """Test content-based recommendations."""
        engine.is_trained = True
        engine.cb_model = MagicMock()
        engine.cb_model.get_recommendations.return_value = [{"title": "Book B"}]
        engine.processed_data = {"books_content": MagicMock()}

        result = engine.get_recommendations("Test Book", method="content")

        assert result == [{"title": "Book B"}]
        engine.cb_model.get_recommendations.assert_called_once()

    def test_get_recommendations_hybrid(self, engine):
        """Test hybrid recommendations."""
        engine.is_trained = True
        engine.hybrid_model = MagicMock()
        engine.hybrid_model.get_recommendations.return_value = [{"title": "Book C"}]
        engine.processed_data = {
            "books_content": MagicMock(),
            "books": MagicMock()
        }

        result = engine.get_recommendations("Test Book", method="hybrid")

        assert result == [{"title": "Book C"}]
        engine.hybrid_model.get_recommendations.assert_called_once()

    def test_get_available_books_not_trained(self, engine):
        """Test getting available books when not trained."""
        result = engine.get_available_books()
        assert result == []

    def test_get_available_books_with_limit(self, engine, sample_books_content_df):
        """Test getting available books with limit."""
        engine.is_trained = True
        engine.processed_data = {"books_content": sample_books_content_df}

        result = engine.get_available_books(limit=2)

        assert len(result) == 2

    def test_search_books_not_trained(self, engine):
        """Test searching books when not trained."""
        result = engine.search_books("test")
        assert result == []

    def test_search_books_success(self, engine, sample_books_content_df):
        """Test successful book search."""
        engine.is_trained = True
        engine.processed_data = {"books_content": sample_books_content_df}

        result = engine.search_books("gatsby", limit=5)

        assert len(result) >= 0
        for book in result:
            assert "title" in book
            assert "author" in book

    def test_search_books_case_insensitive(self, engine, sample_books_content_df):
        """Test that search is case insensitive."""
        engine.is_trained = True
        engine.processed_data = {"books_content": sample_books_content_df}

        result_lower = engine.search_books("gatsby")
        result_upper = engine.search_books("GATSBY")

        assert len(result_lower) == len(result_upper)

    def test_get_book_info_not_trained(self, engine):
        """Test getting book info when not trained."""
        result = engine.get_book_info("Test Book")
        assert result is None

    def test_get_book_info_not_found(self, engine, sample_books_content_df):
        """Test getting info for non-existent book."""
        engine.is_trained = True
        engine.processed_data = {"books_content": sample_books_content_df}

        result = engine.get_book_info("Nonexistent Book")
        assert result is None

    def test_get_book_info_success(self, engine, sample_books_content_df):
        """Test successful book info retrieval."""
        engine.is_trained = True
        engine.processed_data = {"books_content": sample_books_content_df}

        result = engine.get_book_info("The Great Gatsby")

        assert result is not None
        assert result["title"] == "The Great Gatsby"
        assert "author" in result
        assert "image_url" in result

    def test_get_popular_books_not_trained(self, engine):
        """Test getting popular books when not trained."""
        result = engine.get_popular_books()
        assert result == []

    def test_get_popular_books_success(
        self, engine, sample_books_content_df, sample_final_rating_df, sample_books_df
    ):
        """Test successful popular books retrieval."""
        engine.is_trained = True
        engine.processed_data = {
            "books_content": sample_books_content_df,
            "final_rating": sample_final_rating_df,
            "books": sample_books_df
        }

        result = engine.get_popular_books(limit=5)

        assert isinstance(result, list)
        for book in result:
            assert "title" in book
            assert "author" in book
            assert "image_url" in book

    @patch("app.services.recommendation_engine.ModelManager")
    def test_load_trained_models_not_exist(self, mock_manager_class, engine):
        """Test loading models when they don't exist."""
        mock_manager = MagicMock()
        mock_manager.models_exist.return_value = False
        engine.model_manager = mock_manager

        result = engine.load_trained_models()

        assert result is False
        assert engine.is_trained is False

    @patch("app.services.recommendation_engine.ModelManager")
    def test_load_trained_models_success(self, mock_manager_class, engine):
        """Test successful model loading."""
        mock_manager = MagicMock()
        mock_manager.models_exist.return_value = True
        mock_manager.load_models.return_value = {
            "cf_model": MagicMock(),
            "cb_model": MagicMock(),
            "hybrid_model": MagicMock(),
            "books_content": MagicMock(),
            "final_rating": MagicMock(),
            "books": MagicMock()
        }
        engine.model_manager = mock_manager

        result = engine.load_trained_models()

        assert result is True
        assert engine.is_trained is True

    def test_search_books_with_results(self, engine, sample_books_content_df):
        """Test search that returns matching results."""
        engine.is_trained = True
        df = sample_books_content_df.copy()
        df["img_url"] = "http://example.com/img.jpg"
        engine.processed_data = {"books_content": df}

        result = engine.search_books("Great", limit=5)

        assert len(result) >= 0
        for book in result:
            assert "title" in book
            assert "author" in book
            assert "image_url" in book

    def test_search_books_with_invalid_image(self, engine, sample_books_content_df):
        """Test search with invalid image URL."""
        engine.is_trained = True
        df = sample_books_content_df.copy()
        df["img_url"] = "invalid"
        engine.processed_data = {"books_content": df}

        result = engine.search_books("Gatsby", limit=5)

        # Should use default image for invalid URL
        for book in result:
            if book.get("image_url"):
                assert book["image_url"].startswith("http")

    def test_get_popular_books_fallback_to_books(
        self, engine, sample_books_content_df, sample_final_rating_df
    ):
        """Test popular books when title not in books_content."""
        engine.is_trained = True
        # Create books_content without one title from final_rating
        books_content = pd.DataFrame({
            "title": ["Other Book"],
            "author": ["Other Author"],
            "year": ["2000"],
            "publisher": ["Publisher"],
            "img_url": ["http://example.com/other.jpg"]
        })
        books = sample_books_content_df.copy()
        books["img_url"] = "http://example.com/book.jpg"
        books["year"] = "2000"
        books["publisher"] = "Publisher"

        engine.processed_data = {
            "books_content": books_content,
            "final_rating": sample_final_rating_df,
            "books": books
        }

        result = engine.get_popular_books(limit=5)
        assert isinstance(result, list)

    def test_get_book_info_with_invalid_image(self, engine, sample_books_content_df):
        """Test get_book_info with invalid image URL."""
        engine.is_trained = True
        df = sample_books_content_df.copy()
        df["img_url"] = None
        engine.processed_data = {"books_content": df}

        result = engine.get_book_info("The Great Gatsby")

        if result:
            assert result["image_url"].startswith("http")

    @patch("app.services.recommendation_engine.DataLoader")
    @patch("app.services.recommendation_engine.DataPreprocessor")
    def test_train_models_data_load_failure(
        self, mock_preprocessor, mock_loader, engine
    ):
        """Test train_models when data loading fails."""
        mock_loader.load_books.return_value = None
        mock_loader.load_users.return_value = MagicMock()
        mock_loader.load_ratings.return_value = MagicMock()

        result = engine.train_models()

        assert result is False
        assert engine.is_trained is False

    @patch("app.services.recommendation_engine.DataLoader")
    @patch("app.services.recommendation_engine.DataPreprocessor")
    @patch("app.services.recommendation_engine.CollaborativeFilteringModel")
    @patch("app.services.recommendation_engine.ContentBasedModel")
    @patch("app.services.recommendation_engine.HybridRecommendationModel")
    def test_train_models_success(
        self, mock_hybrid, mock_cb, mock_cf, mock_preprocessor, mock_loader, engine
    ):
        """Test successful model training."""
        # Mock data loading
        mock_loader.load_books.return_value = pd.DataFrame({"title": ["A"]})
        mock_loader.load_users.return_value = pd.DataFrame({"user_id": [1]})
        mock_loader.load_ratings.return_value = pd.DataFrame({"rating": [5]})

        # Mock preprocessor
        mock_prep_instance = MagicMock()
        mock_prep_instance.get_processed_data.return_value = {
            "books": pd.DataFrame(),
            "users": pd.DataFrame(),
            "ratings": pd.DataFrame(),
            "final_rating": pd.DataFrame(),
            "books_content": pd.DataFrame()
        }
        mock_preprocessor.return_value = mock_prep_instance

        # Mock model manager
        engine.model_manager = MagicMock()
        engine.model_manager.save_models.return_value = True

        result = engine.train_models()

        assert result is True
        assert engine.is_trained is True

    @patch("app.services.recommendation_engine.DataLoader")
    @patch("app.services.recommendation_engine.DataPreprocessor")
    @patch("app.services.recommendation_engine.CollaborativeFilteringModel")
    @patch("app.services.recommendation_engine.ContentBasedModel")
    @patch("app.services.recommendation_engine.HybridRecommendationModel")
    def test_train_models_save_failure(
        self, mock_hybrid, mock_cb, mock_cf, mock_preprocessor, mock_loader, engine
    ):
        """Test train_models when saving fails."""
        # Mock data loading
        mock_loader.load_books.return_value = pd.DataFrame({"title": ["A"]})
        mock_loader.load_users.return_value = pd.DataFrame({"user_id": [1]})
        mock_loader.load_ratings.return_value = pd.DataFrame({"rating": [5]})

        # Mock preprocessor
        mock_prep_instance = MagicMock()
        mock_prep_instance.get_processed_data.return_value = {
            "books": pd.DataFrame(),
            "users": pd.DataFrame(),
            "ratings": pd.DataFrame(),
            "final_rating": pd.DataFrame(),
            "books_content": pd.DataFrame()
        }
        mock_preprocessor.return_value = mock_prep_instance

        # Mock model manager to fail save
        engine.model_manager = MagicMock()
        engine.model_manager.save_models.return_value = False

        result = engine.train_models()

        assert result is False

    @patch("app.services.recommendation_engine.ModelManager")
    def test_load_models_returns_none(self, mock_manager_class, engine):
        """Test load when model_manager.load_models returns None."""
        mock_manager = MagicMock()
        mock_manager.models_exist.return_value = True
        mock_manager.load_models.return_value = None
        engine.model_manager = mock_manager

        result = engine.load_trained_models()

        assert result is False
        assert engine.is_trained is False

    def test_get_available_books_no_limit(self, engine, sample_books_content_df):
        """Test get_available_books returns all books when no limit specified."""
        engine.is_trained = True
        engine.processed_data = {"books_content": sample_books_content_df}

        result = engine.get_available_books(limit=None)

        # Should return all unique titles without limit
        assert isinstance(result, list)
        assert len(result) == len(sample_books_content_df["title"].unique())

    def test_get_popular_books_not_in_both_dataframes(self, engine):
        """Test popular books when title not found in both dataframes (continue)."""
        engine.is_trained = True

        # Create a final_rating with a title that doesn't exist in either DataFrame
        final_rating = pd.DataFrame({
            "title": ["Nonexistent Book", "Another Missing Book"],
            "rating": [5, 4]
        })

        # Empty dataframes - book won't be found
        books_content = pd.DataFrame({
            "title": [],
            "author": [],
            "year": [],
            "publisher": [],
            "img_url": []
        })
        books = pd.DataFrame({
            "title": [],
            "author": [],
            "year": [],
            "publisher": [],
            "img_url": []
        })

        engine.processed_data = {
            "books_content": books_content,
            "final_rating": final_rating,
            "books": books
        }

        result = engine.get_popular_books(limit=5)

        # Should return empty list since no books found
        assert result == []

    def test_get_popular_books_invalid_image(self, engine, sample_final_rating_df):
        """Test popular books with invalid image URL uses default."""
        engine.is_trained = True

        books_content = pd.DataFrame({
            "title": ["The Great Gatsby"],
            "author": ["F. Scott Fitzgerald"],
            "year": ["1925"],
            "publisher": ["Scribner"],
            "img_url": [None]  # Invalid image
        })

        engine.processed_data = {
            "books_content": books_content,
            "final_rating": sample_final_rating_df,
            "books": books_content
        }

        result = engine.get_popular_books(limit=5)

        # Should use default image URL for invalid img_url
        for book in result:
            assert book["image_url"].startswith("http")
