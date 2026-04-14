"""Data loading utilities for BookSage-AI."""
import pandas as pd

from app.core.config import Config
from app.core.logger import logger


class DataLoader:
    """Load and preprocess data files."""

    @staticmethod
    def load_books() -> pd.DataFrame | None:
        """
        Load and preprocess books data.

        Returns:
            DataFrame with books data or None if loading fails
        """
        try:
            books = pd.read_csv(
                Config.DATA_DIR / Config.BOOKS_FILE,
                sep=";",
                on_bad_lines="skip",
                encoding="latin-1"
            )

            # Select and rename columns
            books = books[[
                "ISBN", "Book-Title", "Book-Author",
                "Year-Of-Publication", "Publisher", "Image-URL-L"
            ]]
            books.rename(columns={
                "Book-Title": "title",
                "Book-Author": "author",
                "Year-Of-Publication": "year",
                "Publisher": "publisher",
                "Image-URL-L": "img_url"
            }, inplace=True)

            logger.info(f"Books data loaded successfully. Shape: {books.shape}")
            return books

        except Exception as e:
            logger.error(f"Error loading books data: {e}")
            return None

    @staticmethod
    def load_users() -> pd.DataFrame | None:
        """
        Load and preprocess users data.

        Returns:
            DataFrame with users data or None if loading fails
        """
        try:
            users = pd.read_csv(
                Config.DATA_DIR / Config.USERS_FILE,
                sep=";",
                on_bad_lines="skip",
                encoding="latin-1"
            )

            users.rename(columns={
                "User-ID": "user_id",
                "Location": "location",
                "Age": "age"
            }, inplace=True)

            logger.info(f"Users data loaded successfully. Shape: {users.shape}")
            return users

        except Exception as e:
            logger.error(f"Error loading users data: {e}")
            return None

    @staticmethod
    def load_ratings() -> pd.DataFrame | None:
        """
        Load and preprocess ratings data.

        Returns:
            DataFrame with ratings data or None if loading fails
        """
        try:
            ratings = pd.read_csv(
                Config.DATA_DIR / Config.RATINGS_FILE,
                sep=";",
                on_bad_lines="skip",
                encoding="latin-1"
            )

            ratings.rename(columns={
                "User-ID": "user_id",
                "Book-Rating": "rating"
            }, inplace=True)

            logger.info(f"Ratings data loaded successfully. Shape: {ratings.shape}")
            return ratings

        except Exception as e:
            logger.error(f"Error loading ratings data: {e}")
            return None
