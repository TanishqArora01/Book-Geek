"""Tests for data loader module."""
import pandas as pd

from app.services.data_loader import DataLoader


class TestDataLoader:
    """Test cases for DataLoader class."""

    def test_load_books_success(self, sample_books_df, tmp_path, monkeypatch):
        """Test successful loading of books data."""
        # Create temp CSV file
        csv_path = tmp_path / "BX-Books.csv"
        sample_books_df.rename(columns={
            "title": "Book-Title",
            "author": "Book-Author",
            "year": "Year-Of-Publication",
            "publisher": "Publisher",
            "img_url": "Image-URL-L"
        }).to_csv(csv_path, sep=";", index=False)

        # Patch Config
        from app.core.config import Config
        monkeypatch.setattr(Config, "DATA_DIR", tmp_path)
        monkeypatch.setattr(Config, "BOOKS_FILE", "BX-Books.csv")

        result = DataLoader.load_books()

        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert "title" in result.columns
        assert "author" in result.columns

    def test_load_books_file_not_found(self, tmp_path, monkeypatch):
        """Test loading books when file doesn't exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "DATA_DIR", tmp_path)
        monkeypatch.setattr(Config, "BOOKS_FILE", "nonexistent.csv")

        result = DataLoader.load_books()
        assert result is None

    def test_load_users_success(self, sample_users_df, tmp_path, monkeypatch):
        """Test successful loading of users data."""
        # Create temp CSV file
        csv_path = tmp_path / "BX-Users.csv"
        sample_users_df.rename(columns={
            "user_id": "User-ID",
            "location": "Location",
            "age": "Age"
        }).to_csv(csv_path, sep=";", index=False)

        from app.core.config import Config
        monkeypatch.setattr(Config, "DATA_DIR", tmp_path)
        monkeypatch.setattr(Config, "USERS_FILE", "BX-Users.csv")

        result = DataLoader.load_users()

        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert "user_id" in result.columns

    def test_load_users_file_not_found(self, tmp_path, monkeypatch):
        """Test loading users when file doesn't exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "DATA_DIR", tmp_path)
        monkeypatch.setattr(Config, "USERS_FILE", "nonexistent.csv")

        result = DataLoader.load_users()
        assert result is None

    def test_load_ratings_success(self, sample_ratings_df, tmp_path, monkeypatch):
        """Test successful loading of ratings data."""
        # Create temp CSV file
        csv_path = tmp_path / "BX-Book-Ratings.csv"
        sample_ratings_df.rename(columns={
            "user_id": "User-ID",
            "rating": "Book-Rating"
        }).to_csv(csv_path, sep=";", index=False)

        from app.core.config import Config
        monkeypatch.setattr(Config, "DATA_DIR", tmp_path)
        monkeypatch.setattr(Config, "RATINGS_FILE", "BX-Book-Ratings.csv")

        result = DataLoader.load_ratings()

        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert "user_id" in result.columns
        assert "rating" in result.columns

    def test_load_ratings_file_not_found(self, tmp_path, monkeypatch):
        """Test loading ratings when file doesn't exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "DATA_DIR", tmp_path)
        monkeypatch.setattr(Config, "RATINGS_FILE", "nonexistent.csv")

        result = DataLoader.load_ratings()
        assert result is None
