"""
Command-line interface for the Human-AI Interaction Framework.

This module provides a command-line interface for interacting with
the Human-AI Interaction Framework.
"""
import argparse
import os
import sys
import uuid
from typing import Dict, List, Optional

from src.human_ai_framework.core.framework import Role
from src.human_ai_framework.models.interaction import (
    Interaction,
    InteractionSession,
    InteractionStatus,
    InteractionType
)
from src.human_ai_framework.services.framework_service import FrameworkService
from src.human_ai_framework.services.registry import service_registry
from src.human_ai_framework.utils.config import config_manager
from src.human_ai_framework.utils.logging import logging_manager, get_logger


class FrameworkCLI:
    """
    Command-line interface for the Human-AI Interaction Framework.
    
    This class provides a command-line interface for interacting with
    the Human-AI Interaction Framework.
    """
    
    def __init__(self) -> None:
        """Initialize the CLI."""
        self.logger = get_logger(self.__class__.__name__)
        self.current_session: Optional[InteractionSession] = None
        
    def initialize(self, config_dir: Optional[str] = None, env: str = "development") -> None:
        """
        Initialize the CLI.
        
        Args:
            config_dir: Path to the configuration directory (optional)
            env: Environment name (e.g., development, production)
        """
        # Load configuration
        self._load_configuration(config_dir, env)
        
        # Initialize logging
        logging_manager.init_logging()
        
        # Initialize services
        service_registry.initialize_all()
        
        # Create a new session
        self._create_new_session()
        
    def _load_configuration(self, config_dir: Optional[str] = None, env: str = "development") -> None:
        """
        Load configuration.
        
        Args:
            config_dir: Path to the configuration directory (optional)
            env: Environment name (e.g., development, production)
        """
        # Load environment variables
        config_manager.load_from_env()
        
        # Load configuration files
        if config_dir:
            config_manager.load_hierarchical_config(config_dir, env)
            
    def _create_new_session(self) -> None:
        """Create a new interaction session."""
        session_id = str(uuid.uuid4())
        self.current_session = InteractionSession(
            session_id=session_id,
            metadata={"environment": config_manager.get("environment", "development")}
        )
        self.logger.info(f"Created new session: {session_id}")
        
    def run(self) -> None:
        """
        Run the CLI in interactive mode.
        
        This method starts an interactive session where the user can
        input instructions and receive responses.
        """
        if not self.current_session:
            self._create_new_session()
            
        framework_service = service_registry.get_typed("framework", FrameworkService)
        
        print("\nHuman-AI Interaction Framework CLI")
        print("----------------------------------")
        print("Type 'help' for available commands, 'exit' to quit.\n")
        print(f"Session ID: {self.current_session.session_id}")
        print("----------------------------------\n")
        
        # Main interaction loop
        while True:
            try:
                # Get user input
                user_input = input("Human> ").strip()
                
                # Process built-in commands
                if user_input.lower() == "exit":
                    print("Exiting...")
                    break
                elif user_input.lower() == "help":
                    self._print_help()
                    continue
                elif user_input.lower() == "summary":
                    summary = framework_service.generate_framework_summary()
                    print("\nFramework Summary:")
                    print(summary)
                    continue
                elif user_input.lower() == "clear":
                    os.system("cls" if os.name == "nt" else "clear")
                    continue
                elif user_input.lower() == "new session":
                    self._create_new_session()
                    print(f"Created new session: {self.current_session.session_id}")
                    continue
                
                # Create a new interaction for the user input
                interaction_id = str(uuid.uuid4())
                interaction = self.current_session.add_interaction(
                    interaction_id=interaction_id,
                    interaction_type=InteractionType.INSTRUCTION,
                    status=InteractionStatus.IN_PROGRESS
                )
                
                # Add the user message to the interaction
                interaction.add_message(user_input, Role.HUMAN)
                
                # Generate AI response
                ai_response = self._generate_ai_response(user_input)
                
                # Add the AI response to the interaction
                interaction.add_message(ai_response, Role.AI)
                
                # Update interaction status
                interaction.status = InteractionStatus.COMPLETED
                
                # Display AI response
                print(f"AI> {ai_response}")
                print()
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                self.logger.error(f"Error in CLI: {str(e)}")
                print(f"Error: {str(e)}")
    
    def _generate_ai_response(self, user_input: str) -> str:
        """
        Generate an AI response to the user input.
        
        Args:
            user_input: User input string
            
        Returns:
            AI response string
        """
        # In a real implementation, this would use an actual AI system.
        # For now, we'll use a simple rule-based approach.
        
        if "hello" in user_input.lower() or "hi" in user_input.lower():
            return "Hello! How can I assist you with the Human-AI Interaction Framework today?"
        elif "framework" in user_input.lower():
            return "The Human-AI Interaction Framework establishes a robust, ethical, and transparent collaborative framework between human users and AI systems for digital product design and development."
        elif "role" in user_input.lower() or "responsibility" in user_input.lower():
            return "In the framework, humans define vision and strategy, while AI generates insights and technical solutions. Both work together within ethical guidelines."
        elif "ethical" in user_input.lower():
            return "The framework emphasizes transparency, accountability, privacy, and fairness in all interactions between humans and AI."
        elif "communication" in user_input.lower():
            return "Communication in the framework follows structured dialogues, clarification protocols, and consistency standards to ensure effective collaboration."
        elif "feedback" in user_input.lower():
            return "The framework incorporates immediate feedback, scheduled reviews, and issue tracking to continuously improve human-AI collaboration."
        elif "help" in user_input.lower():
            return "You can ask me about the framework, roles and responsibilities, ethical considerations, communication protocols, feedback mechanisms, or type 'help' for available commands."
        else:
            return "I understand your input, but I'm currently operating with limited capabilities. In a production environment, I would provide more meaningful responses based on the framework's principles."
            
    def _print_help(self) -> None:
        """Print help information."""
        print("\nAvailable Commands:")
        print("  help        - Display this help message")
        print("  exit        - Exit the CLI")
        print("  summary     - Display the framework summary")
        print("  clear       - Clear the screen")
        print("  new session - Create a new interaction session")
        print()
        print("You can also ask questions about:")
        print("  - The framework's purpose and principles")
        print("  - Roles and responsibilities")
        print("  - Ethical considerations")
        print("  - Communication protocols")
        print("  - Feedback mechanisms")
        print("  - Improvement processes")
        print("  - Collaborative workflows")
        print()


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Human-AI Interaction Framework CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--config",
        help="Path to the configuration directory",
        type=str,
        default="config"
    )
    
    parser.add_argument(
        "--env",
        help="Environment name (e.g., development, production)",
        type=str,
        default="development"
    )
    
    parser.add_argument(
        "--log-level",
        help="Logging level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        type=str,
        default=None
    )
    
    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Set log level from command-line argument if provided
    if args.log_level:
        os.environ["HAIF_LOG_LEVEL"] = args.log_level
    
    # Create and initialize the CLI
    cli = FrameworkCLI()
    cli.initialize(args.config, args.env)
    
    # Run the CLI
    cli.run()
    
    # Shutdown services
    service_registry.shutdown_all()


if __name__ == "__main__":
    main() 