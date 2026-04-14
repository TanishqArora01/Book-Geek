"""Collaborative filtering model for BookSage-AI."""
from typing import Any

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from app.core.config import Config
from app.core.logger import logger


class CollaborativeFilteringModel:
    """Collaborative filtering recommendation model using KNN."""

    def __init__(self):
        """Initialize the collaborative filtering model."""
        self.model: NearestNeighbors | None = None
        self.book_pivot: pd.DataFrame | None = None
        self.is_trained: bool = False

    def _normalize_text_value(self, value: Any) -> str | None:
        """Convert values into response-safe strings."""
        if value is None:
            return None

        try:
            if pd.isna(value):
                return None
        except Exception:
            pass

        text = str(value).strip()
        return text or None

    def train(self, final_rating: pd.DataFrame) -> bool:
        """
        Train the collaborative filtering model.

        Args:
            final_rating: DataFrame with user ratings

        Returns:
            True if training successful, False otherwise
        """
        try:
            logger.info("Training collaborative filtering model...")

            # Create user-item matrix
            self.book_pivot = final_rating.pivot_table(
                index="title",
                columns="user_id",
                values="rating"
            ).fillna(0)

            book_sparse = csr_matrix(self.book_pivot.values)

            # Build KNN model
            self.model = NearestNeighbors(metric="cosine", algorithm="brute")
            self.model.fit(book_sparse)

            self.is_trained = True
            logger.info("Collaborative filtering model trained successfully")
            return True

        except Exception as e:
            logger.error(f"Error training collaborative filtering model: {e}")
            self.is_trained = False
            return False

    def get_recommendations(
        self,
        book_title: str,
        books_content: pd.DataFrame,
        books: pd.DataFrame,
        top_n: int = Config.DEFAULT_TOP_N
    ) -> list[dict[str, Any]]:
        """
        Generate collaborative filtering recommendations.

        Args:
            book_title: Title of the book to get recommendations for
            books_content: DataFrame with book content
            books: DataFrame with all books
            top_n: Number of recommendations to return

        Returns:
            List of recommendation dictionaries
        """
        if not self.is_trained or self.model is None or self.book_pivot is None:
            logger.warning("Model not trained yet")
            return []

        try:
            if book_title not in self.book_pivot.index:
                logger.warning(
                    f"Book '{book_title}' not found in collaborative filtering data"
                )
                return []

            book_idx = np.where(self.book_pivot.index == book_title)[0][0]
            distances, indices = self.model.kneighbors(
                self.book_pivot.iloc[book_idx, :].values.reshape(1, -1),
                n_neighbors=top_n + 1
            )

            recommendations = []
            for i in range(1, len(indices.flatten())):
                title = self.book_pivot.index[indices.flatten()[i]]
                book_info = books_content[books_content["title"] == title]

                if book_info.empty:
                    book_info = books[books["title"] == title]
                    if book_info.empty:
                        continue  # pragma: no cover

                book_info = book_info.iloc[0]
                img_url = self._validate_image_url(book_info["img_url"])

                recommendations.append({
                    "title": title,
                    "author": self._normalize_text_value(book_info["author"]),
                    "year": self._normalize_text_value(book_info["year"]),
                    "publisher": self._normalize_text_value(book_info["publisher"]),
                    "image_url": img_url,
                    "score": float(1 - distances.flatten()[i]),
                    "type": "collaborative"
                })

            return recommendations[:top_n]

        except Exception as e:
            logger.error(f"Error in collaborative recommendations: {e}")
            return []

    def _validate_image_url(self, img_url: Any) -> str:
        """
        Validate and return proper image URL.

        Args:
            img_url: Image URL to validate

        Returns:
            Valid image URL or default placeholder
        """
        if not isinstance(img_url, str) or not img_url.startswith("http"):
            return Config.DEFAULT_IMAGE_URL
        return img_url
