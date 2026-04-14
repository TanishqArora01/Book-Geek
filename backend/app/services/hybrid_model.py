"""Hybrid recommendation model for BookSage-AI."""
from typing import Any

import pandas as pd

from app.core.config import Config
from app.core.logger import logger
from app.services.collaborative_model import CollaborativeFilteringModel
from app.services.content_model import ContentBasedModel


class HybridRecommendationModel:
    """Hybrid recommendation model combining CF and CB approaches."""

    def __init__(
        self,
        cf_model: CollaborativeFilteringModel,
        cb_model: ContentBasedModel
    ):
        """
        Initialize hybrid model with CF and CB models.

        Args:
            cf_model: Trained collaborative filtering model
            cb_model: Trained content-based model
        """
        self.cf_model = cf_model
        self.cb_model = cb_model

    def get_recommendations(
        self,
        book_title: str,
        books_content: pd.DataFrame,
        books: pd.DataFrame,
        cf_weight: float = Config.HYBRID_CF_WEIGHT,
        cb_weight: float = Config.HYBRID_CB_WEIGHT,
        top_n: int = Config.DEFAULT_TOP_N
    ) -> list[dict[str, Any]]:
        """
        Generate hybrid recommendations.

        Args:
            book_title: Title of the book to get recommendations for
            books_content: DataFrame with book content
            books: DataFrame with all books
            cf_weight: Weight for collaborative filtering scores
            cb_weight: Weight for content-based scores
            top_n: Number of recommendations to return

        Returns:
            List of recommendation dictionaries
        """
        try:
            logger.debug(f"Generating hybrid recommendations for: {book_title}")

            cf_recs = self.cf_model.get_recommendations(
                book_title, books_content, books, top_n * 2
            )
            cb_recs = self.cb_model.get_recommendations(
                book_title, books_content, top_n * 2
            )

            if not cf_recs and not cb_recs:
                logger.warning("No recommendations found from either model")
                return []

            combined_scores: dict[str, dict] = {}

            # Add collaborative filtering scores
            for rec in cf_recs:
                combined_scores[rec["title"]] = {
                    "data": rec,
                    "score": rec["score"] * cf_weight
                }

            # Add content-based scores
            for rec in cb_recs:
                if rec["title"] in combined_scores:
                    combined_scores[rec["title"]]["score"] += (
                        rec["score"] * cb_weight
                    )
                else:
                    combined_scores[rec["title"]] = {
                        "data": rec,
                        "score": rec["score"] * cb_weight
                    }

            # Sort by combined score
            sorted_recs = sorted(
                combined_scores.values(),
                key=lambda x: x["score"],
                reverse=True
            )

            # Prepare final recommendations
            final_recommendations = []
            for rec in sorted_recs[:top_n]:
                final_rec = rec["data"].copy()
                final_rec["score"] = float(rec["score"])
                final_rec["type"] = "hybrid"
                final_recommendations.append(final_rec)

            logger.debug(
                f"Generated {len(final_recommendations)} hybrid recommendations"
            )
            return final_recommendations

        except Exception as e:
            logger.error(f"Error in hybrid recommendations: {e}")
            return []
