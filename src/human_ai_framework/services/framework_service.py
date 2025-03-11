"""
Framework service implementation for the Human-AI Interaction Framework.

This module provides a service implementation for managing
the Human-AI Interaction Framework.
"""
from typing import Any, Dict, Optional

from src.human_ai_framework.core.factory import HumanAIFrameworkFactory
from src.human_ai_framework.core.framework import HumanAIFramework
from src.human_ai_framework.services.base import BaseService
from src.human_ai_framework.utils.config import config_manager


class FrameworkService(BaseService):
    """
    Service for managing the Human-AI Interaction Framework.
    
    This service provides methods for creating, configuring, and
    using the Human-AI Interaction Framework.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the framework service.
        
        Args:
            config: Service configuration dictionary (optional)
        """
        super().__init__(config)
        self.framework: Optional[HumanAIFramework] = None
        
    def initialize(self) -> None:
        """
        Initialize the framework service.
        
        This method creates and configures the framework based on
        the service configuration.
        """
        if self.initialized:
            self.logger.debug("Framework service already initialized")
            return
            
        self.logger.info("Initializing framework service")
        
        # Get framework configuration
        if not self.config:
            # Use configuration from config manager
            framework_config = config_manager.get("framework", {})
        else:
            # Use provided configuration
            framework_config = self.config.get("framework", self.config)
        
        # Create framework instance
        if framework_config:
            self.logger.debug("Creating framework from configuration")
            try:
                self.framework = HumanAIFrameworkFactory.create_framework_from_config(framework_config)
            except ValueError as e:
                self.logger.error(f"Failed to create framework from configuration: {str(e)}")
                self.logger.info("Falling back to default framework")
                self.framework = HumanAIFrameworkFactory.create_default_framework()
        else:
            self.logger.debug("Creating default framework")
            self.framework = HumanAIFrameworkFactory.create_default_framework()
            
        self.initialized = True
        self.logger.info("Framework service initialized")
        
    def shutdown(self) -> None:
        """
        Shutdown the framework service.
        
        This method performs any necessary cleanup tasks.
        """
        self.logger.info("Shutting down framework service")
        self.framework = None
        self.initialized = False
        
    def get_framework(self) -> HumanAIFramework:
        """
        Get the current framework instance.
        
        Returns:
            The current framework instance
            
        Raises:
            RuntimeError: If the service is not initialized
        """
        if not self.initialized or self.framework is None:
            raise RuntimeError("Framework service not initialized")
            
        return self.framework
    
    def generate_framework_summary(self) -> str:
        """
        Generate a formatted summary of the current framework.
        
        Returns:
            A string containing the formatted framework summary
            
        Raises:
            RuntimeError: If the service is not initialized
        """
        framework = self.get_framework()
        return framework.generate_framework_summary() 