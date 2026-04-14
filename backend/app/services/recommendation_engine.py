"""Recommendation engine for BookSage-AI."""
from collections import OrderedDict
from typing import Any

from app.core.config import Config
from app.core.logger import logger
from app.services.collaborative_model import CollaborativeFilteringModel
from app.services.content_model import ContentBasedModel
from app.services.data_loader import DataLoader
from app.services.data_preprocessor import DataPreprocessor
from app.services.hybrid_model import HybridRecommendationModel
from app.services.model_manager import ModelManager


class RecommendationEngine:
    """Main recommendation engine combining all models."""

    def __init__(self):
        """Initialize the recommendation engine."""
        self.cf_model: CollaborativeFilteringModel | None = None
        self.cb_model: ContentBasedModel | None = None
        self.hybrid_model: HybridRecommendationModel | None = None
        self.processed_data: dict | None = None
        self.model_manager = ModelManager()
        self.is_trained: bool = False
        self._recommendation_cache: OrderedDict[tuple[str, str, int], list[dict[str, Any]]] = OrderedDict()
        self._cache_max_size: int = 200

    def _normalize_title(self, title: str) -> str:
        """Normalize title to improve cache hit rates."""
        return " ".join(title.strip().lower().split())

    def _normalize_text_value(self, value: Any) -> str | None:
        """Convert pandas/numpy values to clean optional strings."""
        if value is None:
            return None

        try:
            if pd.isna(value):
                return None
        except Exception:
            pass

        text = str(value).strip()
        return text or None

    def _build_book_payload(self, book: pd.Series | dict[str, Any]) -> dict[str, Any]:
        """Create a response-safe book dictionary."""
        img_url = book.get("img_url") if isinstance(book, dict) else book["img_url"]
        normalized_img_url = self._normalize_text_value(img_url)
        if not normalized_img_url or not normalized_img_url.startswith("http"):
            normalized_img_url = Config.DEFAULT_IMAGE_URL

        return {
            "title": self._normalize_text_value(book["title"]),
            "author": self._normalize_text_value(book["author"]),
            "year": self._normalize_text_value(book.get("year") if isinstance(book, dict) else book["year"]),
            "publisher": self._normalize_text_value(book.get("publisher") if isinstance(book, dict) else book["publisher"]),
            "image_url": normalized_img_url,
        }

    def _cache_get(
        self,
        method: str,
        title: str,
        top_n: int,
    ) -> list[dict[str, Any]] | None:
        """Get cached recommendations if available."""
        key = (method, self._normalize_title(title), top_n)
        cached = self._recommendation_cache.get(key)
        if cached is None:
            return None

        # Keep hot entries near the end.
        self._recommendation_cache.move_to_end(key)
        return cached

    def _cache_set(
        self,
        method: str,
        title: str,
        top_n: int,
        recommendations: list[dict[str, Any]],
    ) -> None:
        """Store recommendations in a bounded in-memory LRU cache."""
        key = (method, self._normalize_title(title), top_n)
        self._recommendation_cache[key] = recommendations
        self._recommendation_cache.move_to_end(key)

        if len(self._recommendation_cache) > self._cache_max_size:
            self._recommendation_cache.popitem(last=False)

    def train_models(self) -> bool:
        """
        Train all recommendation models.

        Returns:
            True if training successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("Starting model training...")
        logger.info("=" * 60)

        # Load data
        logger.info("1. Loading data...")
        books = DataLoader.load_books()
        users = DataLoader.load_users()
        ratings = DataLoader.load_ratings()

        if any(data is None for data in [books, users, ratings]):
            logger.error("Failed to load data")
            return False

        # Preprocess data
        logger.info("2. Preprocessing data...")
        preprocessor = DataPreprocessor(books, users, ratings)
        preprocessor.filter_active_users()
        preprocessor.merge_ratings_with_books()
        preprocessor.filter_popular_books()
        preprocessor.prepare_content_features()

        self.processed_data = preprocessor.get_processed_data()

        # Train collaborative filtering model
        logger.info("3. Training collaborative filtering model...")
        self.cf_model = CollaborativeFilteringModel()
        self.cf_model.train(self.processed_data["final_rating"])

        # Train content-based model
        logger.info("4. Training content-based model...")
        self.cb_model = ContentBasedModel()
        self.cb_model.train(self.processed_data["books_content"])

        # Create hybrid model
        logger.info("5. Creating hybrid model...")
        self.hybrid_model = HybridRecommendationModel(
            self.cf_model, self.cb_model
        )

        # Save models
        logger.info("6. Saving models...")
        if self.model_manager.save_models(
            self.cf_model, self.cb_model, self.processed_data
        ):
            self.is_trained = True
            self._recommendation_cache.clear()
            logger.info("=" * 60)
            logger.info("Model training completed successfully!")
            logger.info("=" * 60)
            return True
        else:
            logger.error("Failed to save models")
            return False

    def load_trained_models(self) -> bool:
        """
        Load pre-trained models.

        Returns:
            True if loading successful, False otherwise
        """
        logger.info("Checking for existing trained models...")

        if not self.model_manager.models_exist():
            logger.warning("No trained models found")
            return False

        loaded_data = self.model_manager.load_models()

        if loaded_data:
            self.cf_model = loaded_data["cf_model"]
            self.cb_model = loaded_data["cb_model"]
            self.hybrid_model = loaded_data["hybrid_model"]
            self.processed_data = {
                "books_content": loaded_data["books_content"],
                "final_rating": loaded_data["final_rating"],
                "books": loaded_data["books"]
            }
            self.is_trained = True
            self._recommendation_cache.clear()
            logger.info("Models loaded successfully!")
            return True

        logger.error("Failed to load models")
        return False

    def get_recommendations(
        self,
        book_title: str,
        method: str = "hybrid",
        top_n: int = Config.DEFAULT_TOP_N
    ) -> list[dict[str, Any]]:
        """
        Get recommendations using specified method.

        Args:
            book_title: Title of book to get recommendations for
            method: Recommendation method ('collaborative', 'content', 'hybrid')
            top_n: Number of recommendations to return

        Returns:
            List of recommendation dictionaries
        """
        if not self.is_trained:
            logger.warning("Models not trained or loaded")
            return []

        cached = self._cache_get(method=method, title=book_title, top_n=top_n)
        if cached is not None:
            return cached

        recommendations: list[dict[str, Any]]
        if method == "collaborative":
            recommendations = self.cf_model.get_recommendations(
                book_title,
                self.processed_data["books_content"],
                self.processed_data["books"],
                top_n
            )
        elif method == "content":
            recommendations = self.cb_model.get_recommendations(
                book_title,
                self.processed_data["books_content"],
                top_n
            )
        elif method == "hybrid":
            recommendations = self.hybrid_model.get_recommendations(
                book_title,
                self.processed_data["books_content"],
                self.processed_data["books"],
                top_n=top_n
            )
        else:
            logger.warning(
                "Invalid method. Use 'collaborative', 'content', or 'hybrid'"
            )
            return []

        self._cache_set(
            method=method,
            title=book_title,
            top_n=top_n,
            recommendations=recommendations,
        )
        return recommendations

    def get_available_books(self, limit: int | None = None) -> list[str]:
        """
        Get list of all available books for recommendations.

        Args:
            limit: Maximum number of books to return

        Returns:
            List of book titles
        """
        if not self.is_trained:
            logger.warning("Models not trained or loaded")
            return []

        books = self.processed_data["books_content"]["title"].unique().tolist()
        if limit:
            return books[:limit]
        return books

    def search_books(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """
        Search for books by title.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching book dictionaries
        """
        if not self.is_trained:
            logger.warning("Models not trained or loaded")
            return []

        books = self.processed_data["books_content"]
        matching_books = books[
            books["title"].str.contains(query, case=False, na=False)
        ]

        results = []
        for _, book in matching_books.head(limit).iterrows():
            payload = self._build_book_payload(book)
            results.append(payload)

        return results

    def get_book_info(self, book_title: str) -> dict[str, Any] | None:
        """
        Get detailed information about a specific book.

        Args:
            book_title: Title of the book

        Returns:
            Book info dictionary or None if not found
        """
        if not self.is_trained:
            return None

        book_info = self.processed_data["books_content"][
            self.processed_data["books_content"]["title"] == book_title
        ]

        if book_info.empty:
            return None

        book = book_info.iloc[0]
        return self._build_book_payload(book)

    def get_popular_books(self, limit: int = 12) -> list[dict[str, Any]]:
        """
        Get popular books based on rating count.

        Args:
            limit: Number of popular books to return

        Returns:
            List of popular book dictionaries
        """
        if not self.is_trained:
            return []

        popular_titles = (
            self.processed_data["final_rating"]
            .groupby("title")["rating"]
            .count()
            .sort_values(ascending=False)
            .head(limit)
            .index.tolist()
        )

        books_data = []
        for title in popular_titles:
            book_info = self.processed_data["books_content"][
                self.processed_data["books_content"]["title"] == title
            ]
            if book_info.empty:
                book_info = self.processed_data["books"][
                    self.processed_data["books"]["title"] == title
                ]
                if book_info.empty:
                    continue

            book = book_info.iloc[0]
            books_data.append(self._build_book_payload(book))

        return books_data
