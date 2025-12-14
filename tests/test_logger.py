"""
Tests for pydqa4pm.utils.logger module.
"""

import os
import pytest
import tempfile
from pydqa4pm.utils.logger import Logger


class TestLogger:
    """Test suite for Logger class."""
    
    def test_logger_creation(self):
        """Test that logger can be created."""
        logger = Logger("test_module")
        assert logger is not None
    
    def test_logger_info(self, capsys):
        """Test info level logging."""
        logger = Logger("test_info")
        logger.info("Test message")
        
        captured = capsys.readouterr()
        assert "Info>" in captured.out
        assert "Test message" in captured.out
    
    def test_logger_error(self, capsys):
        """Test error level logging."""
        logger = Logger("test_error")
        logger.error("Error message")
        
        captured = capsys.readouterr()
        assert "Error>" in captured.out
        assert "Error message" in captured.out
    
    def test_logger_debug(self, capsys):
        """Test debug level logging."""
        logger = Logger("test_debug")
        logger.debug("Debug message")
        
        captured = capsys.readouterr()
        assert "Debug>" in captured.out
        assert "Debug message" in captured.out
    
    def test_logger_warning(self, capsys):
        """Test warning level logging."""
        logger = Logger("test_warning")
        logger.warning("Warning message")
        
        captured = capsys.readouterr()
        assert "Warning>" in captured.out
        assert "Warning message" in captured.out
    
    def test_logger_multiple_arguments(self, capsys):
        """Test logging with multiple arguments."""
        logger = Logger("test_multi")
        logger.info("Value:", 42, " items")
        
        captured = capsys.readouterr()
        assert "Value:42 items" in captured.out
    
    def test_logger_builds_message_correctly(self):
        """Test internal message building."""
        logger = Logger("test_build")
        message = logger._build_message(("Part1", " ", "Part2", " ", 123))
        assert message == "Part1 Part2 123"
    
    def test_multiple_loggers_same_name(self):
        """Test that multiple loggers with same name don't add duplicate handlers."""
        logger1 = Logger("same_name")
        handler_count1 = len(logger1._logger.handlers)
        
        logger2 = Logger("same_name")
        handler_count2 = len(logger2._logger.handlers)
        
        # Should not add more handlers
        assert handler_count2 == handler_count1


class TestLoggerAlias:
    """Test backward compatibility alias."""
    
    def test_log_alias_exists(self):
        """Test that log alias exists for backward compatibility."""
        from pydqa4pm.utils.logger import log
        assert log is Logger

