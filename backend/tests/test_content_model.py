"""Tests for content-based model."""
import pandas as pd
import pytest

from app.services.content_model import ContentBasedModel


class TestContentBasedModel:
    """Test cases for ContentBasedModel class."""

    @pytest.fixture
    def cb_model(self):
        """Create a fresh CB model instance."""
        return ContentBasedModel()

    @pytest.fixture
    def trained_cb_model(self, sample_books_content_df):
        """Create a trained CB model."""
        model = ContentBasedModel()
        model.train(sample_books_content_df)
        return model

    def test_init(self, cb_model):
        """Test model initialization."""
        assert cb_model.tfidf is None
        assert cb_model.content_sim_matrix is None
        assert cb_model.title_to_idx is None
        assert cb_model.is_trained is False

    def test_train_success(self, cb_model, sample_books_content_df):
        """Test successful model training."""
        result = cb_model.train(sample_books_content_df)

        assert result is True
        assert cb_model.is_trained is True
        assert cb_model.tfidf is not None
        assert cb_model.content_sim_matrix is not None
        assert cb_model.title_to_idx is not None

    def test_train_creates_similarity_matrix(self, cb_model, sample_books_content_df):
        """Test that training creates similarity matrix."""
        cb_model.train(sample_books_content_df)

        assert cb_model.content_sim_matrix is not None
        assert len(cb_model.content_sim_matrix) == len(sample_books_content_df)

    def test_train_creates_title_index(self, cb_model, sample_books_content_df):
        """Test that training creates title to index mapping."""
        cb_model.train(sample_books_content_df)

        assert cb_model.title_to_idx is not None
        assert isinstance(cb_model.title_to_idx, pd.Series)

    def test_get_recommendations_not_trained(self, cb_model, sample_books_content_df):
        """Test getting recommendations when model is not trained."""
        result = cb_model.get_recommendations(
            "The Great Gatsby",
            sample_books_content_df
        )

        assert result == []

    def test_get_recommendations_book_not_found(
        self, trained_cb_model, sample_books_content_df
    ):
        """Test getting recommendations for non-existent book."""
        result = trained_cb_model.get_recommendations(
            "Nonexistent Book",
            sample_books_content_df
        )

        assert result == []

    def test_get_recommendations_success(
        self, trained_cb_model, sample_books_content_df
    ):
        """Test successful recommendation generation."""
        result = trained_cb_model.get_recommendations(
            "The Great Gatsby",
            sample_books_content_df,
            top_n=3
        )

        assert isinstance(result, list)
        for rec in result:
            assert "title" in rec
            assert "author" in rec
            assert "score" in rec
            assert "type" in rec
            assert rec["type"] == "content"

    def test_recommendations_have_valid_scores(
        self, trained_cb_model, sample_books_content_df
    ):
        """Test that recommendations have valid similarity scores."""
        result = trained_cb_model.get_recommendations(
            "The Great Gatsby",
            sample_books_content_df,
            top_n=3
        )

        for rec in result:
            assert 0 <= rec["score"] <= 1

    def test_validate_image_url_valid(self, cb_model):
        """Test image URL validation with valid URL."""
        result = cb_model._validate_image_url("http://example.com/image.jpg")
        assert result == "http://example.com/image.jpg"

    def test_validate_image_url_invalid(self, cb_model):
        """Test image URL validation with invalid URL."""
        from app.core.config import Config

        result = cb_model._validate_image_url("invalid_url")
        assert result == Config.DEFAULT_IMAGE_URL

    def test_validate_image_url_none(self, cb_model):
        """Test image URL validation with None."""
        from app.core.config import Config

        result = cb_model._validate_image_url(None)
        assert result == Config.DEFAULT_IMAGE_URL

    def test_train_failure_with_invalid_data(self, cb_model):
        """Test training failure with invalid data."""
        invalid_df = pd.DataFrame({"wrong_column": [1, 2, 3]})
        result = cb_model.train(invalid_df)
        assert result is False
        assert cb_model.is_trained is False

    def test_get_recommendations_exception_handling(self, trained_cb_model):
        """Test that exceptions are handled gracefully."""
        result = trained_cb_model.get_recommendations(
            "The Great Gatsby",
            None,
            top_n=3
        )
        assert result == []
