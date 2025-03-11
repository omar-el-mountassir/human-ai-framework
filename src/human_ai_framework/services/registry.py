"""
Service registry module for the Human-AI Interaction Framework.

This module provides a registry for managing services in the framework.
"""
from typing import Any, Dict, Optional, Type, TypeVar, cast

from src.human_ai_framework.services.base import BaseService
from src.human_ai_framework.services.framework_service import FrameworkService
from src.human_ai_framework.utils.logging import get_logger

# Type variable for service classes
T = TypeVar('T', bound=BaseService)


class ServiceRegistry:
    """
    Registry for managing services in the framework.
    
    This class provides methods for registering, retrieving, and
    managing services in the framework.
    """
    
    def __init__(self) -> None:
        """Initialize the service registry."""
        self.services: Dict[str, BaseService] = {}
        self.logger = get_logger(self.__class__.__name__)
        
    def register(self, service_name: str, service: BaseService) -> None:
        """
        Register a service with the registry.
        
        Args:
            service_name: Name of the service
            service: Service instance
            
        Raises:
            ValueError: If a service with the same name is already registered
        """
        if service_name in self.services:
            raise ValueError(f"Service '{service_name}' is already registered")
            
        self.services[service_name] = service
        self.logger.debug(f"Registered service: {service_name}")
        
    def unregister(self, service_name: str) -> None:
        """
        Unregister a service from the registry.
        
        Args:
            service_name: Name of the service
            
        Raises:
            KeyError: If the service is not registered
        """
        if service_name not in self.services:
            raise KeyError(f"Service '{service_name}' is not registered")
            
        service = self.services[service_name]
        
        # Shutdown the service if it's initialized
        if service.is_initialized():
            service.shutdown()
            
        # Remove the service from the registry
        del self.services[service_name]
        self.logger.debug(f"Unregistered service: {service_name}")
        
    def get(self, service_name: str, initialize: bool = True) -> BaseService:
        """
        Get a registered service.
        
        Args:
            service_name: Name of the service
            initialize: Whether to initialize the service if not already initialized
            
        Returns:
            The registered service
            
        Raises:
            KeyError: If the service is not registered
        """
        if service_name not in self.services:
            raise KeyError(f"Service '{service_name}' is not registered")
            
        service = self.services[service_name]
        
        # Initialize the service if requested and not already initialized
        if initialize and not service.is_initialized():
            service.initialize()
            
        return service
    
    def get_typed(self, service_name: str, service_type: Type[T], initialize: bool = True) -> T:
        """
        Get a registered service with type checking.
        
        Args:
            service_name: Name of the service
            service_type: Expected service type
            initialize: Whether to initialize the service if not already initialized
            
        Returns:
            The registered service
            
        Raises:
            KeyError: If the service is not registered
            TypeError: If the service is not of the expected type
        """
        service = self.get(service_name, initialize)
        
        if not isinstance(service, service_type):
            raise TypeError(f"Service '{service_name}' is not of type {service_type.__name__}")
            
        return cast(T, service)
    
    def initialize_all(self) -> None:
        """
        Initialize all registered services.
        
        This method initializes all registered services that are not
        already initialized.
        """
        self.logger.info("Initializing all services")
        
        for service_name, service in self.services.items():
            if not service.is_initialized():
                self.logger.debug(f"Initializing service: {service_name}")
                service.initialize()
                
    def shutdown_all(self) -> None:
        """
        Shutdown all registered services.
        
        This method shuts down all registered services that are
        currently initialized.
        """
        self.logger.info("Shutting down all services")
        
        for service_name, service in self.services.items():
            if service.is_initialized():
                self.logger.debug(f"Shutting down service: {service_name}")
                service.shutdown()
                
    def __contains__(self, service_name: str) -> bool:
        """
        Check if a service is registered.
        
        Args:
            service_name: Name of the service
            
        Returns:
            True if the service is registered, False otherwise
        """
        return service_name in self.services


# Create a singleton instance of the service registry
service_registry = ServiceRegistry()

# Register built-in services
service_registry.register("framework", FrameworkService()) 