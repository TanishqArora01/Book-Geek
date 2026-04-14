"""Tests for model manager module."""
import pickle
from pathlib import Path

import pandas as pd
import pytest

from app.services.model_manager import ModelManager


class TestModelManager:
    """Test cases for ModelManager class."""

    @pytest.fixture
    def model_manager(self, tmp_path, monkeypatch):
        """Create ModelManager with temp directory."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)
        return ModelManager()

    @pytest.fixture
    def real_cf_model(self):
        """Create a real CF model for testing."""
        from app.services.collaborative_model import CollaborativeFilteringModel
        model = CollaborativeFilteringModel()
        # Set minimal attributes for pickling
        model.book_pivot = pd.DataFrame({"col": [1, 2, 3]})
        model.model = None
        return model

    @pytest.fixture
    def real_cb_model(self):
        """Create a real CB model for testing."""
        from app.services.content_model import ContentBasedModel
        model = ContentBasedModel()
        model.tfidf = None
        model.content_sim_matrix = [[1.0, 0.5], [0.5, 1.0]]
        model.title_to_idx = pd.Series({"Book A": 0, "Book B": 1})
        return model

    @pytest.fixture
    def mock_processed_data(self):
        """Create mock processed data."""
        return {
            "books_content": pd.DataFrame({
                "title": ["Book A", "Book B"],
                "author": ["Author A", "Author B"]
            }),
            "final_rating": pd.DataFrame({
                "title": ["Book A", "Book B"],
                "rating": [4.5, 4.0]
            }),
            "books": pd.DataFrame({
                "ISBN": ["001", "002"],
                "title": ["Book A", "Book B"]
            })
        }

    def test_init_creates_directory(self, tmp_path, monkeypatch):
        """Test ModelManager creates models directory."""
        from app.core.config import Config
        models_dir = tmp_path / "test_models"
        monkeypatch.setattr(Config, "MODELS_DIR", models_dir)

        assert not models_dir.exists()
        ModelManager()
        assert models_dir.exists()

    def test_save_models_success(
        self, model_manager, real_cf_model, real_cb_model, mock_processed_data,
        tmp_path, monkeypatch
    ):
        """Test successful model saving."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        result = model_manager.save_models(
            real_cf_model,
            real_cb_model,
            mock_processed_data
        )

        assert result is True
        assert (tmp_path / "cf_model.pkl").exists()
        assert (tmp_path / "cb_model.pkl").exists()
        assert (tmp_path / "books_content.pkl").exists()

    def test_save_models_failure(
        self, model_manager, real_cf_model, real_cb_model, monkeypatch
    ):
        """Test model saving failure with invalid path."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", Path("/invalid/path/that/does/not/exist"))

        result = model_manager.save_models(
            real_cf_model,
            real_cb_model,
            {"books_content": None, "final_rating": None, "books": None}
        )

        assert result is False

    def test_load_models_success(
        self, model_manager, real_cf_model, real_cb_model, mock_processed_data,
        tmp_path, monkeypatch
    ):
        """Test successful model loading."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        # Save models first
        save_result = model_manager.save_models(
            real_cf_model, real_cb_model, mock_processed_data
        )
        assert save_result is True

        # Load models
        result = model_manager.load_models()

        assert result is not None
        assert "cf_model" in result
        assert "cb_model" in result
        assert "hybrid_model" in result
        assert "books_content" in result

    def test_load_models_missing_file(self, model_manager, tmp_path, monkeypatch):
        """Test model loading when files don't exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        result = model_manager.load_models()

        assert result is None

    def test_load_models_partial_files(
        self, model_manager, tmp_path, monkeypatch
    ):
        """Test model loading when some files exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        # Create only one file with valid pickle
        with open(tmp_path / "cf_model.pkl", "wb") as f:
            pickle.dump({"test": "data"}, f)

        result = model_manager.load_models()
        assert result is None

    def test_load_models_corrupt_file(
        self, model_manager, tmp_path, monkeypatch
    ):
        """Test model loading with corrupt file."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        # Create all required files but make one corrupt
        required_files = [
            "cf_model.pkl", "cb_model.pkl", "books_content.pkl",
            "final_rating.pkl", "books_data.pkl"
        ]
        for filename in required_files:
            with open(tmp_path / filename, "wb") as f:
                f.write(b"corrupt data")

        result = model_manager.load_models()
        assert result is None

    def test_models_exist_true(
        self, model_manager, real_cf_model, real_cb_model, mock_processed_data,
        tmp_path, monkeypatch
    ):
        """Test models_exist returns True when all files exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        model_manager.save_models(real_cf_model, real_cb_model, mock_processed_data)

        result = model_manager.models_exist()
        assert result is True

    def test_models_exist_false(self, model_manager, tmp_path, monkeypatch):
        """Test models_exist returns False when files don't exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        result = model_manager.models_exist()
        assert result is False

    def test_models_exist_partial(self, model_manager, tmp_path, monkeypatch):
        """Test models_exist returns False when only some files exist."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "MODELS_DIR", tmp_path)

        # Create only some files
        with open(tmp_path / "cf_model.pkl", "wb") as f:
            pickle.dump({}, f)

        result = model_manager.models_exist()
        assert result is False
