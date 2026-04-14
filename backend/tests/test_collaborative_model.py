"""Tests for collaborative filtering model."""
import numpy as np
import pandas as pd
import pytest

from app.services.collaborative_model import CollaborativeFilteringModel


class TestCollaborativeFilteringModel:
    """Test cases for CollaborativeFilteringModel class."""

    @pytest.fixture
    def cf_model(self):
        """Create a fresh CF model instance."""
        return CollaborativeFilteringModel()

    @pytest.fixture
    def trained_cf_model(self, sample_final_rating_df):
        """Create a trained CF model."""
        model = CollaborativeFilteringModel()
        model.train(sample_final_rating_df)
        return model

    def test_init(self, cf_model):
        """Test model initialization."""
        assert cf_model.model is None
        assert cf_model.book_pivot is None
        assert cf_model.is_trained is False

    def test_train_success(self, cf_model, sample_final_rating_df):
        """Test successful model training."""
        result = cf_model.train(sample_final_rating_df)

        assert result is True
        assert cf_model.is_trained is True
        assert cf_model.model is not None
        assert cf_model.book_pivot is not None

    def test_train_creates_pivot_table(self, cf_model, sample_final_rating_df):
        """Test that training creates correct pivot table."""
        cf_model.train(sample_final_rating_df)

        assert isinstance(cf_model.book_pivot, pd.DataFrame)
        assert cf_model.book_pivot.index.name == "title"

    def test_get_recommendations_not_trained(self, cf_model, sample_books_content_df):
        """Test getting recommendations when model is not trained."""
        result = cf_model.get_recommendations(
            "The Great Gatsby",
            sample_books_content_df,
            sample_books_content_df
        )

        assert result == []

    def test_get_recommendations_book_not_found(
        self, trained_cf_model, sample_books_content_df
    ):
        """Test getting recommendations for non-existent book."""
        result = trained_cf_model.get_recommendations(
            "Nonexistent Book",
            sample_books_content_df,
            sample_books_content_df
        )

        assert result == []

    def test_get_recommendations_success(
        self, trained_cf_model, sample_books_content_df, sample_books_df
    ):
        """Test successful recommendation generation."""
        if trained_cf_model.book_pivot is not None:
            available_titles = trained_cf_model.book_pivot.index.tolist()
            if available_titles:
                result = trained_cf_model.get_recommendations(
                    available_titles[0],
                    sample_books_content_df,
                    sample_books_df,
                    top_n=3
                )

                assert isinstance(result, list)
                for rec in result:
                    assert "title" in rec
                    assert "author" in rec
                    assert "score" in rec
                    assert "type" in rec
                    assert rec["type"] == "collaborative"

    def test_validate_image_url_valid(self, cf_model):
        """Test image URL validation with valid URL."""
        result = cf_model._validate_image_url("http://example.com/image.jpg")
        assert result == "http://example.com/image.jpg"

    def test_validate_image_url_https(self, cf_model):
        """Test image URL validation with HTTPS URL."""
        result = cf_model._validate_image_url("https://example.com/image.jpg")
        assert result == "https://example.com/image.jpg"

    def test_validate_image_url_invalid(self, cf_model):
        """Test image URL validation with invalid URL."""
        from app.core.config import Config

        result = cf_model._validate_image_url("invalid_url")
        assert result == Config.DEFAULT_IMAGE_URL

    def test_validate_image_url_none(self, cf_model):
        """Test image URL validation with None."""
        from app.core.config import Config

        result = cf_model._validate_image_url(None)
        assert result == Config.DEFAULT_IMAGE_URL

    def test_validate_image_url_nan(self, cf_model):
        """Test image URL validation with NaN."""
        from app.core.config import Config

        result = cf_model._validate_image_url(np.nan)
        assert result == Config.DEFAULT_IMAGE_URL

    def test_train_failure_with_invalid_data(self, cf_model):
        """Test training failure with invalid data."""
        invalid_df = pd.DataFrame({"wrong_column": [1, 2, 3]})
        result = cf_model.train(invalid_df)
        assert result is False
        assert cf_model.is_trained is False

    def test_get_recommendations_fallback_to_books(
        self, trained_cf_model, sample_books_df
    ):
        """Test recommendations when title not in books_content."""
        if trained_cf_model.book_pivot is not None:
            available_titles = trained_cf_model.book_pivot.index.tolist()
            if available_titles:
                empty_content = pd.DataFrame({
                    "title": ["Not in pivot"],
                    "author": ["Unknown"],
                    "year": ["2000"],
                    "publisher": ["Unknown"],
                    "img_url": ["http://example.com/img.jpg"]
                })
                result = trained_cf_model.get_recommendations(
                    available_titles[0],
                    empty_content,
                    sample_books_df,
                    top_n=3
                )
                assert isinstance(result, list)

    def test_get_recommendations_exception_handling(self, trained_cf_model):
        """Test that exceptions are handled gracefully."""
        if trained_cf_model.book_pivot is not None:
            available_titles = trained_cf_model.book_pivot.index.tolist()
            if available_titles:
                result = trained_cf_model.get_recommendations(
                    available_titles[0],
                    None,
                    None,
                    top_n=3
                )
                assert result == []

    def test_get_recommendations_book_not_in_both_dataframes(
        self, cf_model, sample_final_rating_df
    ):
        """Test recommendations when book not found in both dataframes (continue)."""
        from unittest.mock import patch

        import numpy as np

        # First train the model
        cf_model.train(sample_final_rating_df)

        if cf_model.book_pivot is not None and len(cf_model.book_pivot.index) > 0:

            # Mock the pivot index to include a fake book title that won't be in DataFrames
            original_index = cf_model.book_pivot.index.tolist()

            # Create a custom Index with a non-existent book at indices returned
            fake_index = pd.Index([
                "Nonexistent Book 1",
                "Nonexistent Book 2",
                "Nonexistent Book 3",
                "Nonexistent Book 4",
                "Nonexistent Book 5"
            ] + original_index, name="title")

            # Mock kneighbors to return indices pointing to non-existent books
            with patch.object(cf_model.model, 'kneighbors') as mock_kneighbors:
                mock_kneighbors.return_value = (
                    np.array([[0.1, 0.2, 0.3]]),  # distances
                    np.array([[0, 1, 2]])  # indices - points to fake books
                )

                # Create a modified pivot with fake book at index 0
                original_pivot = cf_model.book_pivot
                cf_model.book_pivot = pd.DataFrame(
                    index=fake_index[:len(original_pivot) + 3],
                    columns=original_pivot.columns
                ).fillna(0)

                # DataFrames without the fake books
                books_content = pd.DataFrame({
                    "title": ["Real Book"],
                    "author": ["Real Author"],
                    "year": ["2020"],
                    "publisher": ["Publisher"],
                    "img_url": ["http://example.com/real.jpg"]
                })
                books = pd.DataFrame({
                    "title": ["Another Real Book"],
                    "author": ["Another Author"],
                    "year": ["2021"],
                    "publisher": ["Publisher2"],
                    "img_url": ["http://example.com/real2.jpg"]
                })

                result = cf_model.get_recommendations(
                    fake_index[0],  # Use the fake book title
                    books_content,
                    books,
                    top_n=3
                )

                # Restore original pivot
                cf_model.book_pivot = original_pivot

            # Should return empty or partial since fake books aren't in DataFrames
            assert isinstance(result, list)
