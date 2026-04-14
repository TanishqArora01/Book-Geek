"""Tests for hybrid recommendation model."""
from unittest.mock import MagicMock

import pytest

from app.services.hybrid_model import HybridRecommendationModel


class TestHybridRecommendationModel:
    """Test cases for HybridRecommendationModel class."""

    @pytest.fixture
    def mock_cf_model(self):
        """Create mock collaborative filtering model."""
        model = MagicMock()
        model.get_recommendations.return_value = [
            {
                "title": "Book A",
                "author": "Author A",
                "year": "2020",
                "publisher": "Publisher A",
                "image_url": "http://example.com/a.jpg",
                "score": 0.9,
                "type": "collaborative"
            },
            {
                "title": "Book B",
                "author": "Author B",
                "year": "2021",
                "publisher": "Publisher B",
                "image_url": "http://example.com/b.jpg",
                "score": 0.8,
                "type": "collaborative"
            }
        ]
        return model

    @pytest.fixture
    def mock_cb_model(self):
        """Create mock content-based model."""
        model = MagicMock()
        model.get_recommendations.return_value = [
            {
                "title": "Book A",
                "author": "Author A",
                "year": "2020",
                "publisher": "Publisher A",
                "image_url": "http://example.com/a.jpg",
                "score": 0.85,
                "type": "content"
            },
            {
                "title": "Book C",
                "author": "Author C",
                "year": "2019",
                "publisher": "Publisher C",
                "image_url": "http://example.com/c.jpg",
                "score": 0.7,
                "type": "content"
            }
        ]
        return model

    @pytest.fixture
    def hybrid_model(self, mock_cf_model, mock_cb_model):
        """Create hybrid model with mocked submodels."""
        return HybridRecommendationModel(mock_cf_model, mock_cb_model)

    def test_init(self, hybrid_model, mock_cf_model, mock_cb_model):
        """Test hybrid model initialization."""
        assert hybrid_model.cf_model is mock_cf_model
        assert hybrid_model.cb_model is mock_cb_model

    def test_get_recommendations_success(
        self, hybrid_model, sample_books_content_df, sample_books_df
    ):
        """Test successful hybrid recommendation generation."""
        result = hybrid_model.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df,
            top_n=3
        )

        assert isinstance(result, list)
        assert len(result) <= 3
        for rec in result:
            assert "title" in rec
            assert "score" in rec
            assert rec["type"] == "hybrid"

    def test_get_recommendations_combines_scores(
        self, hybrid_model, sample_books_content_df, sample_books_df
    ):
        """Test that hybrid model combines scores from both models."""
        result = hybrid_model.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df,
            cf_weight=0.6,
            cb_weight=0.4,
            top_n=5
        )

        book_a = next((r for r in result if r["title"] == "Book A"), None)
        if book_a:
            assert book_a["score"] == pytest.approx(0.88, rel=0.01)

    def test_get_recommendations_no_results(
        self, sample_books_content_df, sample_books_df
    ):
        """Test hybrid model when neither model returns results."""
        mock_cf = MagicMock()
        mock_cf.get_recommendations.return_value = []

        mock_cb = MagicMock()
        mock_cb.get_recommendations.return_value = []

        hybrid = HybridRecommendationModel(mock_cf, mock_cb)

        result = hybrid.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df
        )

        assert result == []

    def test_get_recommendations_only_cf_results(
        self, mock_cf_model, sample_books_content_df, sample_books_df
    ):
        """Test hybrid model when only CF returns results."""
        mock_cb = MagicMock()
        mock_cb.get_recommendations.return_value = []

        hybrid = HybridRecommendationModel(mock_cf_model, mock_cb)

        result = hybrid.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df
        )

        assert len(result) > 0
        for rec in result:
            assert rec["type"] == "hybrid"

    def test_get_recommendations_only_cb_results(
        self, mock_cb_model, sample_books_content_df, sample_books_df
    ):
        """Test hybrid model when only CB returns results."""
        mock_cf = MagicMock()
        mock_cf.get_recommendations.return_value = []

        hybrid = HybridRecommendationModel(mock_cf, mock_cb_model)

        result = hybrid.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df
        )

        assert len(result) > 0
        for rec in result:
            assert rec["type"] == "hybrid"

    def test_get_recommendations_sorted_by_score(
        self, hybrid_model, sample_books_content_df, sample_books_df
    ):
        """Test that recommendations are sorted by score descending."""
        result = hybrid_model.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df,
            top_n=5
        )

        if len(result) > 1:
            scores = [r["score"] for r in result]
            assert scores == sorted(scores, reverse=True)

    def test_custom_weights(
        self, hybrid_model, sample_books_content_df, sample_books_df
    ):
        """Test hybrid model with custom weights."""
        result = hybrid_model.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df,
            cf_weight=0.3,
            cb_weight=0.7,
            top_n=5
        )

        assert isinstance(result, list)

    def test_get_recommendations_exception_handling(
        self, sample_books_content_df, sample_books_df
    ):
        """Test that hybrid model handles exceptions gracefully."""
        mock_cf = MagicMock()
        mock_cf.get_recommendations.side_effect = Exception("Test error")

        mock_cb = MagicMock()
        mock_cb.get_recommendations.return_value = []

        hybrid = HybridRecommendationModel(mock_cf, mock_cb)

        result = hybrid.get_recommendations(
            "Test Book",
            sample_books_content_df,
            sample_books_df
        )

        assert result == []
