"""
Unit tests for the models module.
"""
import pytest
from datetime import datetime
from unittest.mock import patch

from src.human_ai_framework.models.interaction import (
    Message,
    Interaction,
    InteractionSession,
    InteractionType,
    InteractionStatus
)
from src.human_ai_framework.core.framework import Role


class TestMessage:
    """Tests for the Message class."""
    
    def test_init(self):
        """Test initialization of Message."""
        content = "Test message"
        role = Role.HUMAN
        metadata = {"key": "value"}
        
        message = Message(content=content, role=role, metadata=metadata)
        
        assert message.content == content
        assert message.role == role
        assert message.metadata == metadata
        assert isinstance(message.timestamp, datetime)
    
    def test_str_representation_human(self):
        """Test string representation of a human message."""
        message = Message(content="Hello", role=Role.HUMAN)
        str_repr = str(message)
        
        assert "Human: Hello" in str_repr
        assert message.timestamp.strftime('%Y-%m-%d') in str_repr
    
    def test_str_representation_ai(self):
        """Test string representation of an AI message."""
        message = Message(content="Hello", role=Role.AI)
        str_repr = str(message)
        
        assert "AI: Hello" in str_repr
        assert message.timestamp.strftime('%Y-%m-%d') in str_repr


class TestInteraction:
    """Tests for the Interaction class."""
    
    def test_init(self):
        """Test initialization of Interaction."""
        interaction_id = "test-interaction-1"
        interaction_type = InteractionType.INSTRUCTION
        status = InteractionStatus.PENDING
        metadata = {"session": "test-session"}
        
        interaction = Interaction(
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            status=status,
            metadata=metadata
        )
        
        assert interaction.interaction_id == interaction_id
        assert interaction.interaction_type == interaction_type
        assert interaction.status == status
        assert interaction.metadata == metadata
        assert isinstance(interaction.created_at, datetime)
        assert isinstance(interaction.updated_at, datetime)
        assert interaction.messages == []
    
    def test_add_message(self):
        """Test adding a message to an interaction."""
        interaction = Interaction(
            interaction_id="test-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )
        
        # Test initial state
        assert len(interaction.messages) == 0
        
        # Add a message
        content = "Test message"
        role = Role.HUMAN
        metadata = {"key": "value"}
        
        old_updated_at = interaction.updated_at
        
        # Small delay to ensure timestamp difference
        with patch('src.human_ai_framework.models.interaction.datetime') as mock_datetime:
            mock_now = datetime.now()
            mock_datetime.now.return_value = mock_now
            
            message = interaction.add_message(content, role, metadata)
            
            assert mock_datetime.now.called
            assert interaction.updated_at == mock_now
        
        # Check the message was added
        assert len(interaction.messages) == 1
        assert interaction.messages[0] == message
        assert message.content == content
        assert message.role == role
        assert message.metadata == metadata
    
    def test_get_last_message_empty(self):
        """Test getting the last message from an empty interaction."""
        interaction = Interaction(
            interaction_id="test-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )
        
        assert interaction.get_last_message() is None
    
    def test_get_last_message(self):
        """Test getting the last message from an interaction."""
        interaction = Interaction(
            interaction_id="test-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )
        
        # Add messages
        message1 = interaction.add_message("First message", Role.HUMAN)
        message2 = interaction.add_message("Second message", Role.AI)
        
        # Check the last message
        assert interaction.get_last_message() == message2
    
    def test_get_messages_by_role(self):
        """Test getting messages by role."""
        interaction = Interaction(
            interaction_id="test-interaction",
            interaction_type=InteractionType.INSTRUCTION,
            status=InteractionStatus.PENDING
        )
        
        # Add messages with different roles
        human_message1 = interaction.add_message("Human message 1", Role.HUMAN)
        ai_message = interaction.add_message("AI message", Role.AI)
        human_message2 = interaction.add_message("Human message 2", Role.HUMAN)
        
        # Get messages by role
        human_messages = interaction.get_messages_by_role(Role.HUMAN)
        ai_messages = interaction.get_messages_by_role(Role.AI)
        
        # Check the results
        assert len(human_messages) == 2
        assert human_message1 in human_messages
        assert human_message2 in human_messages
        
        assert len(ai_messages) == 1
        assert ai_message in ai_messages


class TestInteractionSession:
    """Tests for the InteractionSession class."""
    
    def test_init(self):
        """Test initialization of InteractionSession."""
        session_id = "test-session-1"
        metadata = {"user": "test-user"}
        
        session = InteractionSession(
            session_id=session_id,
            metadata=metadata
        )
        
        assert session.session_id == session_id
        assert session.metadata == metadata
        assert isinstance(session.created_at, datetime)
        assert isinstance(session.updated_at, datetime)
        assert session.interactions == []
    
    def test_add_interaction(self):
        """Test adding an interaction to a session."""
        session = InteractionSession(session_id="test-session")
        
        # Test initial state
        assert len(session.interactions) == 0
        
        # Add an interaction
        interaction_id = "test-interaction"
        interaction_type = InteractionType.INSTRUCTION
        status = InteractionStatus.PENDING
        metadata = {"key": "value"}
        
        old_updated_at = session.updated_at
        
        # Small delay to ensure timestamp difference
        with patch('src.human_ai_framework.models.interaction.datetime') as mock_datetime:
            mock_now = datetime.now()
            mock_datetime.now.return_value = mock_now
            
            interaction = session.add_interaction(
                interaction_id=interaction_id,
                interaction_type=interaction_type,
                status=status,
                metadata=metadata
            )
            
            assert mock_datetime.now.called
            assert session.updated_at == mock_now
        
        # Check the interaction was added
        assert len(session.interactions) == 1
        assert session.interactions[0] == interaction
        assert interaction.interaction_id == interaction_id
        assert interaction.interaction_type == interaction_type
        assert interaction.status == status
        assert interaction.metadata == metadata
    
    def test_get_interaction(self):
        """Test getting an interaction by ID."""
        session = InteractionSession(session_id="test-session")
        
        # Add interactions
        interaction1 = session.add_interaction(
            interaction_id="interaction-1",
            interaction_type=InteractionType.INSTRUCTION
        )
        interaction2 = session.add_interaction(
            interaction_id="interaction-2",
            interaction_type=InteractionType.RESPONSE
        )
        
        # Get interaction by ID
        found_interaction = session.get_interaction("interaction-1")
        assert found_interaction == interaction1
        
        # Get non-existent interaction
        not_found = session.get_interaction("non-existent")
        assert not_found is None
    
    def test_get_latest_interaction_empty(self):
        """Test getting the latest interaction from an empty session."""
        session = InteractionSession(session_id="test-session")
        assert session.get_latest_interaction() is None
    
    def test_get_latest_interaction(self):
        """Test getting the latest interaction from a session."""
        session = InteractionSession(session_id="test-session")
        
        # Add interactions
        interaction1 = session.add_interaction(
            interaction_id="interaction-1",
            interaction_type=InteractionType.INSTRUCTION
        )
        interaction2 = session.add_interaction(
            interaction_id="interaction-2",
            interaction_type=InteractionType.RESPONSE
        )
        
        # Check the latest interaction
        assert session.get_latest_interaction() == interaction2 