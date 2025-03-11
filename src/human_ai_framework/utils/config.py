"""
Configuration management module for the Human-AI Interaction Framework.

This module provides utilities for loading, parsing, and validating
configuration from various sources, including environment variables
and configuration files.
"""
import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union


class ConfigurationManager:
    """
    Configuration manager for the Human-AI Interaction Framework.
    
    This class provides methods for loading, parsing, and validating
    configuration from various sources, including environment variables
    and configuration files.
    """
    
    def __init__(self, env_prefix: str = "HAIF_") -> None:
        """
        Initialize the configuration manager.
        
        Args:
            env_prefix: Prefix for environment variables (default: "HAIF_")
        """
        self.env_prefix = env_prefix
        self.config: Dict[str, Any] = {}
        
    def load_from_env(self) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        Returns:
            Dictionary containing configuration loaded from environment variables
        """
        env_config = {}
        
        # Get all environment variables with the specified prefix
        for key, value in os.environ.items():
            if key.startswith(self.env_prefix):
                # Remove prefix and convert to lowercase for consistency
                config_key = key[len(self.env_prefix):].lower()
                
                # Convert string representations to appropriate types
                if value.lower() in ("true", "yes", "1", "on"):
                    env_config[config_key] = True
                elif value.lower() in ("false", "no", "0", "off"):
                    env_config[config_key] = False
                elif value.isdigit():
                    env_config[config_key] = int(value)
                elif value.replace(".", "", 1).isdigit() and value.count(".") == 1:
                    env_config[config_key] = float(value)
                else:
                    env_config[config_key] = value
        
        # Update the configuration with environment variables
        self.config.update(env_config)
        return env_config
    
    def load_from_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load configuration from a file (JSON or YAML).
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Dictionary containing configuration loaded from the file
            
        Raises:
            FileNotFoundError: If the configuration file does not exist
            ValueError: If the file format is not supported or invalid
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        # Load the configuration based on the file extension
        try:
            with open(file_path, "r") as file:
                if file_path.suffix.lower() in (".yaml", ".yml"):
                    file_config = yaml.safe_load(file)
                elif file_path.suffix.lower() == ".json":
                    file_config = json.load(file)
                else:
                    raise ValueError(f"Unsupported configuration file format: {file_path.suffix}")
        except Exception as e:
            raise ValueError(f"Failed to load configuration file: {str(e)}")
        
        # Update the configuration with file settings
        if file_config is not None:
            self.config.update(file_config)
            return file_config
        
        return {}
    
    def load_hierarchical_config(self, base_dir: Union[str, Path], env: str) -> Dict[str, Any]:
        """
        Load hierarchical configuration for a specific environment.
        
        Args:
            base_dir: Base directory containing configuration files
            env: Environment name (e.g., development, testing, production)
            
        Returns:
            Dictionary containing merged configuration from all loaded files
            
        Example directory structure:
            config/
                default.yaml
                development.yaml
                production.yaml
        """
        base_dir = Path(base_dir)
        
        # Define the configuration files to load in order
        config_files = [
            base_dir / "default.yaml",
            base_dir / f"{env}.yaml"
        ]
        
        # Load each configuration file in order
        for file_path in config_files:
            if file_path.exists():
                self.load_from_file(file_path)
        
        return self.config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key
            default: Default value if the key is not found
            
        Returns:
            Configuration value or default value if not found
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value


# Create a singleton instance of the configuration manager
config_manager = ConfigurationManager() 