"""
Integration tests for the complete Human-AI Interaction Framework workflow.

These tests verify the full functionality of the framework
from initialization to processing interactions and feedback.
"""
import pytest
from unittest.mock import patch, MagicMock

from src.human_ai_framework.core.framework import HumanAIFramework, Role
from src.human_ai_framework.core.factory import HumanAIFrameworkFactory
from src.human_ai_framework.services.registry import ServiceRegistry
from src.human_ai_framework.services.framework_service import FrameworkService
from src.human_ai_framework.models.interaction import (
    InteractionSession,
    Interaction,
    InteractionType,
    InteractionStatus,
    Message
)
from src.human_ai_framework.utils.config import ConfigurationManager


class TestFullWorkflow:
    """Tests for the complete Human-AI Interaction Framework workflow."""

    @pytest.fixture
    def config_manager(self):
        """Create a configuration manager for testing."""
        with patch('src.human_ai_framework.utils.config.ConfigurationManager.load_from_file') as mock_load:
            # Mock configuration for testing
            mock_load.return_value = {
                "framework": {
                    "name": "Test Framework",
                    "version": "0.1.0",
                    "ethical_principles": ["TRANSPARENCY", "PRIVACY", "FAIRNESS"],
                    "communication_protocols": ["CLARIFICATION", "STRUCTURED_DIALOGUE"],
                    "feedback_mechanisms": ["IMMEDIATE", "SCHEDULED"],
                    "improvement_processes": ["CONTINUOUS_LEARNING", "RETROSPECTIVE_ANALYSIS"]
                },
                "roles": {
                    "human": [
                        "Provide clear requirements",
                        "Offer feedback on AI suggestions",
                        "Make final decisions on designs"
                    ],
                    "ai": [
                        "Generate design alternatives",
                        "Explain design rationale",
                        "Adapt to user preferences"
                    ]
                }
            }

            config_manager = ConfigurationManager("HAIF_")
            return config_manager

    @pytest.fixture
    def framework_factory(self):
        """Create a framework factory for testing."""
        return HumanAIFrameworkFactory()

    @pytest.fixture
    def framework(self, framework_factory):
        """Create a framework instance for testing."""
        return framework_factory.create_default_framework()

    @pytest.fixture
    def service_registry(self):
        """Create a service registry for testing."""
        return ServiceRegistry()

    @pytest.fixture
    def framework_service(self, framework, service_registry):
        """Create a framework service for testing."""
        service = FrameworkService(framework)
        service_registry.register_service("framework_service", service)
        return service

    def test_end_to_end_workflow(self, framework, framework_service):
        """Test the end-to-end workflow of the framework."""
        # 1. Create a new interaction session
        session = InteractionSession(session_id="test-e2e-session")

        # 2. Start a new design interaction
        interaction = session.add_interaction(
            interaction_id="test-e2e-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )

        # 3. Add initial human instruction
        interaction.add_message(
            "I need a design for a new mobile app that helps users track their daily water intake.",
            Role.HUMAN
        )

        # 4. Mock the service processing with detailed responses
        with patch.object(framework_service, 'process_interaction') as mock_process:
            # First AI response
            mock_process.return_value = """
            Thank you for your request. I'll help design a mobile app for tracking water intake.

            Here are some initial questions to clarify requirements:
            1. What visual style do you prefer (minimalist, colorful, etc.)?
            2. Are there specific features you need beyond basic tracking?
            3. Do you have any reference apps you like?
            """

            # Process the interaction
            ai_response = framework_service.process_interaction(interaction)

            # Add AI response to the interaction
            interaction.add_message(ai_response, Role.AI)

            # Verify first response follows framework guidelines
            assert "clarify requirements" in ai_response
            assert ai_response.count("\n") > 3  # Structured format with multiple lines

            # 5. Add human response with more details
            interaction.add_message(
                """
                I prefer a minimalist design with blue tones. Features needed:
                - Daily goal setting
                - Reminders throughout the day
                - Weekly progress reports
                I like the simplicity of "Daily Water" and "Hydro Coach" apps.
                """,
                Role.HUMAN
            )

            # Update mock response for the second round
            mock_process.return_value = """
            Based on your preferences, I've designed a minimalist water tracking app with blue tones.

            Key components:
            1. Home screen with circular progress indicator
            2. Goal setting screen with customizable targets
            3. Notification system with customizable intervals
            4. Weekly report screen with charts

            Would you like to see wireframes for any specific screens?
            """

            # Process the interaction again
            second_response = framework_service.process_interaction(interaction)

            # Add second AI response
            interaction.add_message(second_response, Role.AI)

            # Verify second response incorporates human feedback
            assert "minimalist" in second_response
            assert "blue tones" in second_response
            assert "Goal setting" in second_response
            assert "Notification" in second_response
            assert "Weekly report" in second_response

            # 6. Add human feedback
            interaction.add_message(
                "This looks good! Can you show me the home screen wireframe and explain how users add water intake?",
                Role.HUMAN
            )

            # Update mock for detailed design explanation
            mock_process.return_value = """
            # Home Screen Wireframe

            [Wireframe description: Circular progress indicator in center showing 65% filled,
            with "1.3L / 2L" text inside. Plus (+) button at bottom right to add water.]

            ## How Users Add Water Intake:

            1. Tap the (+) button on home screen
            2. Choose from preset amounts (200ml, 330ml, 500ml) or enter custom amount
            3. Confirm addition, which updates the progress indicator immediately
            4. Optional: add a timestamp if different from current time

            This approach makes tracking quick and simple, reducing friction for regular use.
            """

            # Process final interaction
            final_response = framework_service.process_interaction(interaction)

            # Add final AI response
            interaction.add_message(final_response, Role.AI)

            # Verify final response provides detailed explanation
            assert "Home Screen" in final_response
            assert "Wireframe" in final_response
            assert "How Users Add" in final_response
            assert "approach makes tracking quick" in final_response  # Explanation of design rationale

    def test_configuration_driven_framework(self, config_manager):
        """Test that the framework is properly configured based on configuration."""
        # Mock a simpler config for easy testing
        with patch.object(config_manager, 'load_from_file') as mock_load:
            mock_load.return_value = {
                "framework": {
                    "name": "Test Framework",
                    "version": "0.1.0"
                },
                "roles": {
                    "human": [
                        "Provide clear requirements",
                        "Offer feedback on AI suggestions",
                        "Make final decisions on designs"
                    ],
                    "ai": [
                        "Generate design alternatives",
                        "Explain design rationale",
                        "Adapt to user preferences"
                    ]
                }
            }

            # Create a framework with desired responsibilities
            framework = HumanAIFramework()

            # Add responsibilities from config
            for resp in ["Provide clear requirements", "Offer feedback on AI suggestions", "Make final decisions on designs"]:
                framework.add_responsibility(Role.HUMAN, resp)

            for resp in ["Generate design alternatives", "Explain design rationale", "Adapt to user preferences"]:
                framework.add_responsibility(Role.AI, resp)

            # Verify responsibilities
            # Verify human responsibilities
            human_responsibilities = framework.get_responsibilities_by_role(Role.HUMAN)
            human_resp_descriptions = [resp.description for resp in human_responsibilities]
            assert "Provide clear requirements" in human_resp_descriptions
            assert "Offer feedback on AI suggestions" in human_resp_descriptions
            assert "Make final decisions on designs" in human_resp_descriptions

            # Verify AI responsibilities
            ai_responsibilities = framework.get_responsibilities_by_role(Role.AI)
            ai_resp_descriptions = [resp.description for resp in ai_responsibilities]
            assert "Generate design alternatives" in ai_resp_descriptions
            assert "Explain design rationale" in ai_resp_descriptions
            assert "Adapt to user preferences" in ai_resp_descriptions

    def test_service_lifecycle(self, service_registry, framework_service):
        """Test the lifecycle of services in the registry."""
        # Verify service is registered and started
        assert service_registry.is_service_registered("framework_service")

        # Start all services
        service_registry.start_all_services()

        # Verify service is running
        assert framework_service.is_running

        # Stop all services
        service_registry.stop_all_services()

        # Verify service is stopped
        assert not framework_service.is_running

        # Restart services
        service_registry.start_all_services()

        # Verify service is running again
        assert framework_service.is_running
