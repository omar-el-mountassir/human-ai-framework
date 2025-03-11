"""
Human-AI Interaction Framework package.

A robust, ethical, and transparent collaborative framework between
human users and AI systems for digital product design and development.
"""

__version__ = "0.1.0"
__author__ = "Omar El-Mountassir"
__email__ = "omar.mountassir@gmail.com"

from src.human_ai_framework.core.framework import (
    HumanAIFramework,
    Role,
    EthicalPrinciple,
    CommunicationProtocol,
    FeedbackMechanism,
    ImprovementProcess,
    CollaborationWorkflow,
    RoleResponsibility
)
from src.human_ai_framework.core.factory import HumanAIFrameworkFactory

__all__ = [
    "HumanAIFramework",
    "HumanAIFrameworkFactory",
    "Role",
    "EthicalPrinciple",
    "CommunicationProtocol", 
    "FeedbackMechanism",
    "ImprovementProcess",
    "CollaborationWorkflow",
    "RoleResponsibility"
]
