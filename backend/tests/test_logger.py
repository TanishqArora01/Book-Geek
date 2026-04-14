"""Tests for logger module."""
import logging

from app.core.logger import setup_logging


class TestLogger:
    """Test cases for logger module."""

    def test_setup_logging_returns_logger(self, tmp_path, monkeypatch):
        """Test setup_logging returns a logger instance."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "LOGS_DIR", tmp_path)

        logger = setup_logging("test_logger")

        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_setup_logging_default_name(self, tmp_path, monkeypatch):
        """Test setup_logging with default name."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "LOGS_DIR", tmp_path)

        logger = setup_logging()

        assert logger.name == "booksage"

    def test_setup_logging_creates_handlers(self, tmp_path, monkeypatch):
        """Test setup_logging creates file and console handlers."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "LOGS_DIR", tmp_path)

        logger = setup_logging("test_handlers")

        # Check handlers were added
        assert len(logger.handlers) >= 2

    def test_setup_logging_creates_log_file(self, tmp_path, monkeypatch):
        """Test setup_logging creates log file."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "LOGS_DIR", tmp_path)

        logger = setup_logging("test_file")
        logger.info("Test message")

        log_file = tmp_path / "app.log"
        assert log_file.exists()

    def test_setup_logging_level(self, tmp_path, monkeypatch):
        """Test setup_logging sets correct level."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "LOGS_DIR", tmp_path)

        logger = setup_logging("test_level")

        assert logger.level == logging.DEBUG

    def test_logger_writes_to_file(self, tmp_path, monkeypatch):
        """Test logger writes messages to file."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "LOGS_DIR", tmp_path)

        logger = setup_logging("test_write")
        test_message = "Test log message for verification"
        logger.info(test_message)

        log_file = tmp_path / "app.log"
        content = log_file.read_text()
        assert test_message in content

    def test_logger_format(self, tmp_path, monkeypatch):
        """Test logger uses correct format."""
        from app.core.config import Config
        monkeypatch.setattr(Config, "LOGS_DIR", tmp_path)

        logger = setup_logging("test_format")
        logger.info("Format test")

        log_file = tmp_path / "app.log"
        content = log_file.read_text()

        # Check format contains expected parts
        assert "test_format" in content
        assert "INFO" in content
