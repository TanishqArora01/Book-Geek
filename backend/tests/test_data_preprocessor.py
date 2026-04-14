"""Tests for data preprocessor module."""
from app.services.data_preprocessor import DataPreprocessor


class TestDataPreprocessor:
    """Test cases for DataPreprocessor class."""

    def test_init(self, sample_books_df, sample_users_df, sample_ratings_df):
        """Test preprocessor initialization."""
        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )

        assert preprocessor.books is not None
        assert preprocessor.users is not None
        assert preprocessor.ratings is not None
        assert preprocessor.ratings_with_books is None
        assert preprocessor.final_rating is None
        assert preprocessor.books_content is None

    def test_filter_active_users(
        self, sample_books_df, sample_users_df, sample_ratings_df, monkeypatch
    ):
        """Test filtering active users."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MIN_USER_RATINGS", 1)

        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )

        result = preprocessor.filter_active_users()

        assert result is preprocessor  # Check method chaining
        assert len(preprocessor.ratings) > 0

    def test_merge_ratings_with_books(
        self, sample_books_df, sample_users_df, sample_ratings_df
    ):
        """Test merging ratings with books."""
        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )

        result = preprocessor.merge_ratings_with_books()

        assert result is preprocessor
        assert preprocessor.ratings_with_books is not None
        assert "title" in preprocessor.ratings_with_books.columns
        assert "rating" in preprocessor.ratings_with_books.columns

    def test_filter_popular_books(
        self, sample_books_df, sample_users_df, sample_ratings_df, monkeypatch
    ):
        """Test filtering popular books."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MIN_BOOK_RATINGS", 1)

        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )
        preprocessor.merge_ratings_with_books()

        result = preprocessor.filter_popular_books()

        assert result is preprocessor
        assert preprocessor.final_rating is not None

    def test_filter_popular_books_without_merge(
        self, sample_books_df, sample_users_df, sample_ratings_df
    ):
        """Test filter_popular_books without calling merge first."""
        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )

        result = preprocessor.filter_popular_books()

        assert result is preprocessor
        assert preprocessor.final_rating is None

    def test_prepare_content_features(
        self, sample_books_df, sample_users_df, sample_ratings_df, monkeypatch
    ):
        """Test preparing content features."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MIN_BOOK_RATINGS", 1)

        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )
        preprocessor.merge_ratings_with_books()
        preprocessor.filter_popular_books()

        result = preprocessor.prepare_content_features()

        assert result is preprocessor
        assert preprocessor.books_content is not None
        assert "content_features" in preprocessor.books_content.columns

    def test_prepare_content_features_without_filter(
        self, sample_books_df, sample_users_df, sample_ratings_df
    ):
        """Test prepare_content_features without calling filter first."""
        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )

        result = preprocessor.prepare_content_features()

        assert result is preprocessor
        assert preprocessor.books_content is None

    def test_get_processed_data(
        self, sample_books_df, sample_users_df, sample_ratings_df, monkeypatch
    ):
        """Test getting all processed data."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MIN_BOOK_RATINGS", 1)

        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )
        preprocessor.merge_ratings_with_books()
        preprocessor.filter_popular_books()
        preprocessor.prepare_content_features()

        result = preprocessor.get_processed_data()

        assert isinstance(result, dict)
        assert "books" in result
        assert "users" in result
        assert "ratings" in result
        assert "final_rating" in result
        assert "books_content" in result

    def test_method_chaining(
        self, sample_books_df, sample_users_df, sample_ratings_df, monkeypatch
    ):
        """Test that methods can be chained."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MIN_USER_RATINGS", 1)
        monkeypatch.setattr(Config, "MIN_BOOK_RATINGS", 1)

        preprocessor = DataPreprocessor(
            sample_books_df,
            sample_users_df,
            sample_ratings_df
        )

        result = (
            preprocessor
            .filter_active_users()
            .merge_ratings_with_books()
            .filter_popular_books()
            .prepare_content_features()
        )

        assert result is preprocessor
        assert preprocessor.books_content is not None
