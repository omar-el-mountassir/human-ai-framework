"""
Logging module for the Human-AI Interaction Framework.

This module provides logging utilities for the framework,
including configurable loggers and formatters.
"""
import os
import sys
import logging
from pathlib import Path
from typing import Dict, Optional, Union

from src.human_ai_framework.utils.config import config_manager


class LoggingManager:
    """
    Logging manager for the Human-AI Interaction Framework.
    
    This class provides methods for configuring and managing loggers
    for the framework.
    """
    
    def __init__(self) -> None:
        """Initialize the logging manager."""
        self.loggers: Dict[str, logging.Logger] = {}
        self.initialized = False
        
    def init_logging(self, config: Optional[Dict] = None) -> None:
        """
        Initialize logging with the given configuration.
        
        Args:
            config: Logging configuration dictionary (optional)
        """
        if self.initialized:
            return
            
        # Use provided config or load from config manager
        if config is None:
            # Ensure config is loaded
            if not config_manager.config:
                config_manager.load_from_env()
                
            config = config_manager.config.get("logging", {})
            
        # Get logging configuration
        log_level = self._get_log_level(config.get("level", "INFO"))
        log_format = config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        log_to_file = config.get("log_to_file", False)
        log_file = config.get("log_file", "logs/human_ai_framework.log")
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(console_handler)
        
        # Create file handler if enabled
        if log_to_file and log_file:
            # Create log directory if it doesn't exist
            log_file_path = Path(log_file)
            log_dir = log_file_path.parent
            os.makedirs(log_dir, exist_ok=True)
            
            # Create and add file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(logging.Formatter(log_format))
            root_logger.addHandler(file_handler)
            
        self.initialized = True
        
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a named logger.
        
        Args:
            name: Logger name
            
        Returns:
            Configured logger instance
        """
        if not self.initialized:
            self.init_logging()
            
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
            
        return self.loggers[name]
    
    @staticmethod
    def _get_log_level(level: Union[str, int]) -> int:
        """
        Convert a log level string to a logging level constant.
        
        Args:
            level: Log level string or integer
            
        Returns:
            Logging level constant
        """
        if isinstance(level, int):
            return level
            
        level_upper = level.upper()
        if level_upper == "DEBUG":
            return logging.DEBUG
        elif level_upper == "INFO":
            return logging.INFO
        elif level_upper == "WARNING":
            return logging.WARNING
        elif level_upper == "ERROR":
            return logging.ERROR
        elif level_upper == "CRITICAL":
            return logging.CRITICAL
        else:
            return logging.INFO


# Create a singleton instance of the logging manager
logging_manager = LoggingManager()


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    return logging_manager.get_logger(name) 