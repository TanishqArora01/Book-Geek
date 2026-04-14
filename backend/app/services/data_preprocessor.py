"""Data preprocessing utilities for BookSage-AI."""
import pandas as pd

from app.core.config import Config
from app.core.logger import logger


class DataPreprocessor:
    """Preprocess data for recommendation models."""

    def __init__(
        self,
        books: pd.DataFrame,
        users: pd.DataFrame,
        ratings: pd.DataFrame
    ):
        """
        Initialize preprocessor with raw data.

        Args:
            books: Raw books DataFrame
            users: Raw users DataFrame
            ratings: Raw ratings DataFrame
        """
        self.books = books
        self.users = users
        self.ratings = ratings
        self.ratings_with_books: pd.DataFrame | None = None
        self.final_rating: pd.DataFrame | None = None
        self.books_content: pd.DataFrame | None = None

    def filter_active_users(self) -> "DataPreprocessor":
        """Filter users with more than MIN_USER_RATINGS ratings."""
        user_ratings_count = self.ratings["user_id"].value_counts()
        active_users = user_ratings_count[
            user_ratings_count > Config.MIN_USER_RATINGS
        ].index
        self.ratings = self.ratings[self.ratings["user_id"].isin(active_users)]
        logger.info(f"Filtered to {len(active_users)} active users")
        return self

    def merge_ratings_with_books(self) -> "DataPreprocessor":
        """Merge ratings with books data."""
        self.ratings_with_books = self.ratings.merge(self.books, on="ISBN")
        logger.info(f"Merged data shape: {self.ratings_with_books.shape}")
        return self

    def filter_popular_books(self) -> "DataPreprocessor":
        """Filter books with at least MIN_BOOK_RATINGS ratings."""
        if self.ratings_with_books is None:
            logger.error("Must call merge_ratings_with_books first")
            return self

        book_ratings_count = self.ratings_with_books.groupby(
            "title"
        )["rating"].count().reset_index()
        book_ratings_count.rename(columns={"rating": "num_ratings"}, inplace=True)

        self.final_rating = self.ratings_with_books.merge(
            book_ratings_count, on="title"
        )
        self.final_rating = self.final_rating[
            self.final_rating["num_ratings"] >= Config.MIN_BOOK_RATINGS
        ]
        self.final_rating.drop_duplicates(["user_id", "title"], inplace=True)

        logger.info(f"Final rating data shape: {self.final_rating.shape}")
        return self

    def prepare_content_features(self) -> "DataPreprocessor":
        """Prepare content-based features."""
        if self.final_rating is None:
            logger.error("Must call filter_popular_books first")
            return self

        self.books_content = self.books.drop_duplicates("title")
        self.books_content = self.books_content[
            self.books_content["title"].isin(self.final_rating["title"])
        ]

        self.books_content = self.books_content.copy()
        self.books_content["content_features"] = (
            self.books_content["title"] + " " +
            self.books_content["author"] + " " +
            self.books_content["publisher"].fillna("") + " " +
            self.books_content["year"].astype(str)
        )

        logger.info(f"Books content shape: {self.books_content.shape}")
        return self

    def get_processed_data(self) -> dict:
        """
        Return all processed data.

        Returns:
            Dictionary with processed DataFrames
        """
        return {
            "books": self.books,
            "users": self.users,
            "ratings": self.ratings,
            "final_rating": self.final_rating,
            "books_content": self.books_content
        }
