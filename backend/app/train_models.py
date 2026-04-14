#!/usr/bin/env python3
"""
Training script for BookSage-AI models.

This script trains all recommendation models using the proper module paths
so that pickled models can be loaded correctly by the FastAPI application.

Usage:
    python train_models.py
"""
import sys
from pathlib import Path

# Ensure the project root is in the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.logger import logger  # noqa: E402
from app.services.recommendation_engine import RecommendationEngine  # noqa: E402


def main():
    """Train all recommendation models."""
    logger.info("=" * 60)
    logger.info("BookSage-AI Model Training Script")
    logger.info("=" * 60)

    engine = RecommendationEngine()

    # Train the models
    logger.info("Starting model training...")
    if engine.train_models():
        logger.info("=" * 60)
        logger.info("SUCCESS: All models trained and saved!")
        logger.info("You can now run the application with:")
        logger.info("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        logger.info("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("FAILED: Model training failed!")
        logger.error("Please check the logs above for details.")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
