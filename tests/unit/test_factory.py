"""
Unit tests for the factory module.
"""
import pytest
from unittest.mock import MagicMock, patch

from src.human_ai_framework.core.factory import HumanAIFrameworkFactory
from src.human_ai_framework.core.framework import (
    HumanAIFramework,
    Role,
    EthicalPrinciple,
    CommunicationProtocol,
    FeedbackMechanism,
    ImprovementProcess,
    CollaborationWorkflow
)


class TestHumanAIFrameworkFactory:
    """Tests for the HumanAIFrameworkFactory class."""
    
    def test_create_default_framework(self):
        """Test creating a default framework."""
        framework = HumanAIFrameworkFactory.create_default_framework()
        
        # Test that the framework is an instance of HumanAIFramework
        assert isinstance(framework, HumanAIFramework)
        
        # Test that the framework has default responsibilities
        assert len(framework.responsibilities[Role.HUMAN]) > 0
        assert len(framework.responsibilities[Role.AI]) > 0
        
        # Test that the framework has default principles
        assert len(framework.active_principles) > 0
        
    def test_create_custom_framework(self):
        """Test creating a custom framework."""
        # Define custom settings
        human_responsibilities = ["Custom human responsibility"]
        ai_responsibilities = ["Custom AI responsibility"]
        ethical_principles = [EthicalPrinciple.TRANSPARENCY]
        communication_protocols = [CommunicationProtocol.STRUCTURED_DIALOGUE]
        feedback_mechanisms = [FeedbackMechanism.IMMEDIATE]
        improvement_processes = [ImprovementProcess.CONTINUOUS_LEARNING]
        collaboration_workflows = [CollaborationWorkflow.TASK_DISTRIBUTION]
        
        # Create custom framework
        framework = HumanAIFrameworkFactory.create_custom_framework(
            human_responsibilities=human_responsibilities,
            ai_responsibilities=ai_responsibilities,
            ethical_principles=ethical_principles,
            communication_protocols=communication_protocols,
            feedback_mechanisms=feedback_mechanisms,
            improvement_processes=improvement_processes,
            collaboration_workflows=collaboration_workflows
        )
        
        # Test that the framework is an instance of HumanAIFramework
        assert isinstance(framework, HumanAIFramework)
        
        # Test that the framework has custom responsibilities
        assert len(framework.responsibilities[Role.HUMAN]) == 1
        assert len(framework.responsibilities[Role.AI]) == 1
        assert framework.responsibilities[Role.HUMAN][0].description == human_responsibilities[0]
        assert framework.responsibilities[Role.AI][0].description == ai_responsibilities[0]
        
        # Test that the framework has custom principles
        assert len(framework.active_principles) == 1
        assert EthicalPrinciple.TRANSPARENCY in framework.active_principles
        
        # Test that the framework has custom protocols
        assert len(framework.active_protocols) == 1
        assert CommunicationProtocol.STRUCTURED_DIALOGUE in framework.active_protocols
        
        # Test that the framework has custom mechanisms
        assert len(framework.active_feedback_mechanisms) == 1
        assert FeedbackMechanism.IMMEDIATE in framework.active_feedback_mechanisms
        
        # Test that the framework has custom processes
        assert len(framework.active_improvement_processes) == 1
        assert ImprovementProcess.CONTINUOUS_LEARNING in framework.active_improvement_processes
        
        # Test that the framework has custom workflows
        assert len(framework.active_workflows) == 1
        assert CollaborationWorkflow.TASK_DISTRIBUTION in framework.active_workflows
        
    def test_create_framework_from_config(self):
        """Test creating a framework from a configuration dictionary."""
        # Define configuration
        config = {
            "human_responsibilities": ["Custom human responsibility"],
            "ai_responsibilities": ["Custom AI responsibility"],
            "ethical_principles": ["TRANSPARENCY"],
            "communication_protocols": ["STRUCTURED_DIALOGUE"],
            "feedback_mechanisms": ["IMMEDIATE"],
            "improvement_processes": ["CONTINUOUS_LEARNING"],
            "collaboration_workflows": ["TASK_DISTRIBUTION"]
        }
        
        # Create framework from configuration
        framework = HumanAIFrameworkFactory.create_framework_from_config(config)
        
        # Test that the framework is an instance of HumanAIFramework
        assert isinstance(framework, HumanAIFramework)
        
        # Test that the framework has custom responsibilities
        assert len(framework.responsibilities[Role.HUMAN]) == 1
        assert len(framework.responsibilities[Role.AI]) == 1
        assert framework.responsibilities[Role.HUMAN][0].description == config["human_responsibilities"][0]
        assert framework.responsibilities[Role.AI][0].description == config["ai_responsibilities"][0]
        
        # Test that the framework has custom principles
        assert len(framework.active_principles) == 1
        assert EthicalPrinciple.TRANSPARENCY in framework.active_principles
        
        # Test that the framework has custom protocols
        assert len(framework.active_protocols) == 1
        assert CommunicationProtocol.STRUCTURED_DIALOGUE in framework.active_protocols
        
        # Test that the framework has custom mechanisms
        assert len(framework.active_feedback_mechanisms) == 1
        assert FeedbackMechanism.IMMEDIATE in framework.active_feedback_mechanisms
        
        # Test that the framework has custom processes
        assert len(framework.active_improvement_processes) == 1
        assert ImprovementProcess.CONTINUOUS_LEARNING in framework.active_improvement_processes
        
        # Test that the framework has custom workflows
        assert len(framework.active_workflows) == 1
        assert CollaborationWorkflow.TASK_DISTRIBUTION in framework.active_workflows
        
    def test_create_framework_from_config_invalid(self):
        """Test creating a framework from an invalid configuration dictionary."""
        # Define invalid configuration
        config = {
            "ethical_principles": ["INVALID_PRINCIPLE"]
        }
        
        # Test that creating a framework from an invalid configuration raises a ValueError
        with pytest.raises(ValueError):
            HumanAIFrameworkFactory.create_framework_from_config(config)
 