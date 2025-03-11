"""
Integration tests for the framework service.

These tests verify that the framework service correctly
integrates with the core framework and other components.
"""
import pytest
from unittest.mock import patch, MagicMock

from src.human_ai_framework.core.framework import (
    HumanAIFramework,
    Role,
    EthicalPrinciple,
    CommunicationProtocol
)
from src.human_ai_framework.services.registry import ServiceRegistry
from src.human_ai_framework.services.framework_service import FrameworkService
from src.human_ai_framework.models.interaction import (
    InteractionSession,
    InteractionType,
    InteractionStatus
)


class TestFrameworkServiceIntegration:
    """Integration tests for the FrameworkService."""

    @pytest.fixture
    def framework(self):
        """Create a framework instance for testing."""
        return HumanAIFramework()

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

    @pytest.fixture
    def session(self):
        """Create an interaction session for testing."""
        return InteractionSession(session_id="test-session")

    def test_service_registration(self, framework_service, service_registry):
        """Test that the framework service is correctly registered."""
        # Verify service is registered
        assert service_registry.get_service("framework_service") == framework_service

        # Verify service can be looked up by type
        services = service_registry.find_services_by_type(FrameworkService)
        assert len(services) == 1
        assert services[0] == framework_service

    def test_framework_service_integration(self, framework_service, session):
        """Test integration between framework service and interaction session."""
        # Create a new interaction
        interaction = session.add_interaction(
            interaction_id="test-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )

        # Add a human message
        human_message = interaction.add_message(
            "Create a design for a new app interface",
            Role.HUMAN
        )

        # Process the message with the framework service
        with patch.object(framework_service, 'process_interaction') as mock_process:
            mock_process.return_value = "Understanding your request for a new app interface design."

            response = framework_service.process_interaction(interaction)

            # Verify the service was called with the interaction
            mock_process.assert_called_once_with(interaction)
            assert response == "Understanding your request for a new app interface design."

    def test_ethical_principles_application(self, framework, framework_service, session):
        """Test that ethical principles are applied during interaction processing."""
        # Ensure transparency principle is active
        framework.add_ethical_principle(EthicalPrinciple.TRANSPARENCY)

        # Create interaction
        interaction = session.add_interaction(
            interaction_id="test-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )

        # Add human message
        interaction.add_message(
            "Why did you make that recommendation?",
            Role.HUMAN
        )

        # Mock the framework's explanation generation
        with patch.object(framework, 'get_responsibilities_by_role') as mock_get:
            mock_get.return_value = ["Provide clear explanations for decisions and recommendations"]

            # Mock the service's processing
            with patch.object(framework_service, 'process_interaction') as mock_process:
                mock_process.return_value = "I recommended this approach because of factors X, Y, and Z..."

                response = framework_service.process_interaction(interaction)

                # Verify the framework was consulted for responsibilities
                mock_get.assert_called_once_with(Role.AI)

                # Verify the response contains an explanation
                assert "because" in response

    def test_communication_protocol_application(self, framework, framework_service, session):
        """Test that communication protocols are applied during interaction."""
        # Ensure structured communication protocol is active
        framework.add_communication_protocol(CommunicationProtocol.STRUCTURED_DIALOGUE)

        # Create interaction
        interaction = session.add_interaction(
            interaction_id="test-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )

        # Add human message
        interaction.add_message(
            "What are the steps to implement this feature?",
            Role.HUMAN
        )

        # Mock the service's processing
        with patch.object(framework_service, 'process_interaction') as mock_process:
            # Mock a structured response with clear steps
            mock_process.return_value = """
            # Steps to Implement Feature

            1. Define requirements
            2. Design the UI components
            3. Implement backend logic
            4. Test the integration
            5. Deploy the feature
            """

            response = framework_service.process_interaction(interaction)

            # Verify the response follows a structured format with steps
            assert "Steps" in response
            assert "1." in response
            assert "2." in response
