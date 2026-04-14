"""Model management utilities for BookSage-AI."""
import pickle
from typing import Any

from app.core.config import Config
from app.core.logger import logger
from app.services.collaborative_model import CollaborativeFilteringModel
from app.services.content_model import ContentBasedModel
from app.services.hybrid_model import HybridRecommendationModel


class ModelManager:
    """Manage model saving and loading operations."""

    def __init__(self):
        """Initialize model manager and ensure directories exist."""
        Config.MODELS_DIR.mkdir(exist_ok=True)

    def save_models(
        self,
        cf_model: CollaborativeFilteringModel,
        cb_model: ContentBasedModel,
        processed_data: dict
    ) -> bool:
        """
        Save all models and processed data.

        Args:
            cf_model: Trained collaborative filtering model
            cb_model: Trained content-based model
            processed_data: Dictionary with processed DataFrames

        Returns:
            True if saving successful, False otherwise
        """
        try:
            logger.info("Saving models and processed data...")

            model_files = {
                "cf_model.pkl": cf_model,
                "cb_model.pkl": cb_model,
                "book_pivot.pkl": cf_model.book_pivot,
                "tfidf_vectorizer.pkl": cb_model.tfidf,
                "content_sim_matrix.pkl": cb_model.content_sim_matrix,
                "title_to_idx.pkl": cb_model.title_to_idx,
                "books_content.pkl": processed_data["books_content"],
                "final_rating.pkl": processed_data["final_rating"],
                "books_data.pkl": processed_data["books"]
            }

            for filename, data in model_files.items():
                with open(Config.MODELS_DIR / filename, "wb") as f:
                    pickle.dump(data, f)
                logger.debug(f"Saved: {filename}")

            logger.info(f"All models saved to: {Config.MODELS_DIR}")
            return True

        except Exception as e:
            logger.error(f"Error saving models: {e}")
            return False

    def load_models(self) -> dict[str, Any] | None:
        """
        Load all models and data.

        Returns:
            Dictionary with loaded models or None if loading fails
        """
        try:
            logger.info("Loading models and processed data...")

            # Check if all required files exist
            required_files = [
                "cf_model.pkl", "cb_model.pkl", "books_content.pkl",
                "final_rating.pkl", "books_data.pkl"
            ]

            for filename in required_files:
                if not (Config.MODELS_DIR / filename).exists():
                    logger.error(f"Required file not found: {filename}")
                    return None

            # Load models
            with open(Config.MODELS_DIR / "cf_model.pkl", "rb") as f:
                cf_model = pickle.load(f)

            with open(Config.MODELS_DIR / "cb_model.pkl", "rb") as f:
                cb_model = pickle.load(f)

            # Load processed data
            with open(Config.MODELS_DIR / "books_content.pkl", "rb") as f:
                books_content = pickle.load(f)

            with open(Config.MODELS_DIR / "final_rating.pkl", "rb") as f:
                final_rating = pickle.load(f)

            with open(Config.MODELS_DIR / "books_data.pkl", "rb") as f:
                books = pickle.load(f)

            # Create hybrid model
            hybrid_model = HybridRecommendationModel(cf_model, cb_model)

            logger.info(f"All models loaded from: {Config.MODELS_DIR}")

            return {
                "cf_model": cf_model,
                "cb_model": cb_model,
                "hybrid_model": hybrid_model,
                "books_content": books_content,
                "final_rating": final_rating,
                "books": books
            }

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return None

    def models_exist(self) -> bool:
        """
        Check if trained models exist.

        Returns:
            True if all required model files exist
        """
        required_files = [
            "cf_model.pkl", "cb_model.pkl", "books_content.pkl",
            "final_rating.pkl", "books_data.pkl"
        ]

        return all(
            (Config.MODELS_DIR / filename).exists()
            for filename in required_files
        )
