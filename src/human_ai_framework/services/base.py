"""
Base service module for the Human-AI Interaction Framework.

This module provides base classes and interfaces for services
in the framework.
"""
import abc
from typing import Any, Dict, Optional

from src.human_ai_framework.utils.logging import get_logger


class BaseService(abc.ABC):
    """
    Abstract base class for all services in the framework.
    
    This class defines the interface and common functionality
    for services in the framework.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the service.
        
        Args:
            config: Service configuration dictionary (optional)
        """
        self.config = config or {}
        self.logger = get_logger(self.__class__.__name__)
        self.initialized = False
        
    @abc.abstractmethod
    def initialize(self) -> None:
        """
        Initialize the service.
        
        This method should be implemented by subclasses to perform
        any necessary initialization steps.
        
        Raises:
            NotImplementedError: If not implemented by subclasses
        """
        pass
    
    @abc.abstractmethod
    def shutdown(self) -> None:
        """
        Shutdown the service.
        
        This method should be implemented by subclasses to perform
        any necessary cleanup steps.
        
        Raises:
            NotImplementedError: If not implemented by subclasses
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the service is initialized.
        
        Returns:
            True if the service is initialized, False otherwise
        """
        return self.initialized
    
    def __enter__(self) -> 'BaseService':
        """
        Enter the context manager.
        
        Returns:
            The service instance
        """
        self.initialize()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit the context manager.
        
        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        self.shutdown() 