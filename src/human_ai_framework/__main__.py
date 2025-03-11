#!/usr/bin/env python3
"""
Human-AI Interaction Framework for Digital Product Design and Development.

This module serves as the entry point for the Human-AI Interaction Framework.
"""
import os
import sys

# Add the src directory to the path to enable imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.human_ai_framework.cli import main as cli_main
from src.human_ai_framework.services.framework_service import FrameworkService
from src.human_ai_framework.services.registry import service_registry
from src.human_ai_framework.utils.config import config_manager
from src.human_ai_framework.utils.logging import logging_manager, get_logger


def main() -> None:
    """Main entry point for the Human-AI Interaction Framework."""
    # Initialize logging
    logging_manager.init_logging()
    logger = get_logger("main")
    
    logger.info("Starting Human-AI Interaction Framework")
    
    try:
        # Run the CLI
        cli_main()
    except Exception as e:
        logger.error(f"Error running the framework: {str(e)}")
        sys.exit(1)
    finally:
        # Shutdown services
        service_registry.shutdown_all()
        
    logger.info("Human-AI Interaction Framework completed successfully")


if __name__ == "__main__":
    main() 