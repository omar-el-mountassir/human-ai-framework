"""
Interaction models for the Human-AI Interaction Framework.

This module provides data models for representing interactions
between human users and AI systems.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional

from src.human_ai_framework.core.framework import Role


class InteractionType(Enum):
    """Enumeration of interaction types between humans and AI."""
    
    INSTRUCTION = auto()  # Human instructs AI
    RESPONSE = auto()  # AI responds to human
    CLARIFICATION = auto()  # AI asks for clarification
    FEEDBACK = auto()  # Human provides feedback
    SUGGESTION = auto()  # AI provides suggestion
    DECISION = auto()  # Human makes decision
    STATUS = auto()  # AI provides status update


class InteractionStatus(Enum):
    """Enumeration of interaction statuses."""
    
    PENDING = auto()  # Waiting for processing
    IN_PROGRESS = auto()  # Currently being processed
    COMPLETED = auto()  # Successfully completed
    FAILED = auto()  # Failed to complete
    CANCELLED = auto()  # Cancelled by user


@dataclass
class Message:
    """Data model for a message in an interaction."""
    
    content: str
    role: Role
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def __str__(self) -> str:
        """
        Return string representation of the message.
        
        Returns:
            String representation of the message
        """
        role_name = "Human" if self.role == Role.HUMAN else "AI"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {role_name}: {self.content}"


@dataclass
class Interaction:
    """Data model for an interaction between a human and AI."""
    
    interaction_id: str
    interaction_type: InteractionType
    status: InteractionStatus
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def add_message(self, content: str, role: Role, metadata: Optional[Dict] = None) -> Message:
        """
        Add a message to the interaction.
        
        Args:
            content: Message content
            role: Role of the message sender
            metadata: Optional metadata for the message
            
        Returns:
            The created message
        """
        message = Message(
            content=content,
            role=role,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def get_last_message(self) -> Optional[Message]:
        """
        Get the last message in the interaction.
        
        Returns:
            The last message or None if there are no messages
        """
        if not self.messages:
            return None
        return self.messages[-1]
    
    def get_messages_by_role(self, role: Role) -> List[Message]:
        """
        Get all messages from a specific role.
        
        Args:
            role: Role to filter by
            
        Returns:
            List of messages from the specified role
        """
        return [message for message in self.messages if message.role == role]


@dataclass
class InteractionSession:
    """Data model for a session of interactions."""
    
    session_id: str
    interactions: List[Interaction] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def add_interaction(
        self,
        interaction_id: str,
        interaction_type: InteractionType,
        status: InteractionStatus = InteractionStatus.PENDING,
        metadata: Optional[Dict] = None
    ) -> Interaction:
        """
        Add an interaction to the session.
        
        Args:
            interaction_id: Unique identifier for the interaction
            interaction_type: Type of interaction
            status: Initial status of the interaction
            metadata: Optional metadata for the interaction
            
        Returns:
            The created interaction
        """
        interaction = Interaction(
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            status=status,
            metadata=metadata or {}
        )
        self.interactions.append(interaction)
        self.updated_at = datetime.now()
        return interaction
    
    def get_interaction(self, interaction_id: str) -> Optional[Interaction]:
        """
        Get an interaction by ID.
        
        Args:
            interaction_id: Interaction ID to find
            
        Returns:
            The interaction or None if not found
        """
        for interaction in self.interactions:
            if interaction.interaction_id == interaction_id:
                return interaction
        return None
    
    def get_latest_interaction(self) -> Optional[Interaction]:
        """
        Get the most recent interaction in the session.
        
        Returns:
            The most recent interaction or None if there are no interactions
        """
        if not self.interactions:
            return None
        return self.interactions[-1] 