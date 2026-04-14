"""Tests for configuration module."""
from pathlib import Path

import pytest

from app.core.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_base_dir_is_path(self):
        """Test that BASE_DIR is a Path object."""
        assert isinstance(Config.BASE_DIR, Path)

    def test_data_dir_is_path(self):
        """Test that DATA_DIR is a Path object."""
        assert isinstance(Config.DATA_DIR, Path)
        assert Config.DATA_DIR == Config.BASE_DIR / "data"

    def test_models_dir_is_path(self):
        """Test that MODELS_DIR is a Path object."""
        assert isinstance(Config.MODELS_DIR, Path)
        assert Config.MODELS_DIR == Config.BASE_DIR / "models"

    def test_logs_dir_is_path(self):
        """Test that LOGS_DIR is a Path object."""
        assert isinstance(Config.LOGS_DIR, Path)
        assert Config.LOGS_DIR == Config.BASE_DIR / "logs"

    def test_data_files_are_strings(self):
        """Test that data file names are strings."""
        assert isinstance(Config.BOOKS_FILE, str)
        assert isinstance(Config.USERS_FILE, str)
        assert isinstance(Config.RATINGS_FILE, str)

    def test_model_parameters(self):
        """Test model parameter values."""
        assert Config.MIN_USER_RATINGS > 0
        assert Config.MIN_BOOK_RATINGS > 0
        assert Config.TFIDF_MAX_FEATURES > 0

    def test_recommendation_parameters(self):
        """Test recommendation parameter values."""
        assert Config.DEFAULT_TOP_N > 0
        assert 0 <= Config.HYBRID_CF_WEIGHT <= 1
        assert 0 <= Config.HYBRID_CB_WEIGHT <= 1
        assert Config.HYBRID_CF_WEIGHT + Config.HYBRID_CB_WEIGHT == pytest.approx(1.0)

    def test_server_settings(self):
        """Test server configuration values."""
        assert Config.HOST == "0.0.0.0"
        assert Config.PORT == 8000
        assert isinstance(Config.DEBUG, bool)

    def test_default_image_url(self):
        """Test default image URL is valid."""
        assert Config.DEFAULT_IMAGE_URL.startswith("http")

    def test_ensure_directories(self, tmp_path, monkeypatch):
        """Test ensure_directories creates required directories."""
        # Temporarily change directories to tmp_path
        test_logs_dir = tmp_path / "logs"
        test_models_dir = tmp_path / "models"

        monkeypatch.setattr(Config, "LOGS_DIR", test_logs_dir)
        monkeypatch.setattr(Config, "MODELS_DIR", test_models_dir)

        # Ensure directories don't exist
        assert not test_logs_dir.exists()
        assert not test_models_dir.exists()

        # Call ensure_directories
        Config.ensure_directories()

        # Check directories were created
        assert test_logs_dir.exists()
        assert test_models_dir.exists()
