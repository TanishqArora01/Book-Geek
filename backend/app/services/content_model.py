"""Content-based model for BookSage-AI."""
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import Config
from app.core.logger import logger


class ContentBasedModel:
    """Content-based recommendation model using TF-IDF."""

    def __init__(self):
        """Initialize the content-based model."""
        self.tfidf: TfidfVectorizer | None = None
        self.content_sim_matrix: Any = None
        self.title_to_idx: pd.Series | None = None
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

    def train(self, books_content: pd.DataFrame) -> bool:
        """
        Train the content-based model.

        Args:
            books_content: DataFrame with book content features

        Returns:
            True if training successful, False otherwise
        """
        try:
            logger.info("Training content-based model...")

            # TF-IDF Vectorizer
            self.tfidf = TfidfVectorizer(
                stop_words="english",
                max_features=Config.TFIDF_MAX_FEATURES
            )

            tfidf_matrix = self.tfidf.fit_transform(
                books_content["content_features"]
            )
            self.content_sim_matrix = cosine_similarity(tfidf_matrix)

            # Create title to index mapping
            self.title_to_idx = pd.Series(
                books_content.index,
                index=books_content["title"]
            )
            self.title_to_idx = self.title_to_idx[
                ~self.title_to_idx.index.duplicated(keep="first")
            ]

            self.is_trained = True
            logger.info("Content-based model trained successfully")
            return True

        except Exception as e:
            logger.error(f"Error training content-based model: {e}")
            self.is_trained = False
            return False

    def get_recommendations(
        self,
        book_title: str,
        books_content: pd.DataFrame,
        top_n: int = Config.DEFAULT_TOP_N
    ) -> list[dict[str, Any]]:
        """
        Generate content-based recommendations.

        Args:
            book_title: Title of the book to get recommendations for
            books_content: DataFrame with book content
            top_n: Number of recommendations to return

        Returns:
            List of recommendation dictionaries
        """
        if not self.is_trained or self.title_to_idx is None:
            logger.warning("Model not trained yet")
            return []

        try:
            if book_title not in self.title_to_idx:
                logger.warning(
                    f"Book '{book_title}' not found in content-based data"
                )
                return []

            cb_idx = self.title_to_idx[book_title]
            sim_scores = list(enumerate(self.content_sim_matrix[cb_idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:top_n + 1]

            recommendations = []
            for i, score in sim_scores:
                title = books_content["title"].iloc[i]
                book_info = books_content[
                    books_content["title"] == title
                ].iloc[0]

                img_url = self._validate_image_url(book_info["img_url"])

                recommendations.append({
                    "title": title,
                    "author": self._normalize_text_value(book_info["author"]),
                    "year": self._normalize_text_value(book_info["year"]),
                    "publisher": self._normalize_text_value(book_info["publisher"]),
                    "image_url": img_url,
                    "score": float(score),
                    "type": "content"
                })

            return recommendations[:top_n]

        except Exception as e:
            logger.error(f"Error in content recommendations: {e}")
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
