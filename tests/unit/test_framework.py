"""
Unit tests for the core framework module.
"""
import pytest
from unittest.mock import MagicMock, patch

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


class TestHumanAIFramework:
    """Tests for the HumanAIFramework class."""
    
    def test_init(self):
        """Test initialization of HumanAIFramework."""
        framework = HumanAIFramework()
        
        # Test that the responsibilities dictionary is initialized
        assert Role.HUMAN in framework.responsibilities
        assert Role.AI in framework.responsibilities
        
        # Test that default responsibilities are added
        assert len(framework.responsibilities[Role.HUMAN]) > 0
        assert len(framework.responsibilities[Role.AI]) > 0
        
        # Test that default principles are added
        assert len(framework.active_principles) > 0
        for principle in EthicalPrinciple:
            assert principle in framework.active_principles
            
        # Test that default protocols are added
        assert len(framework.active_protocols) > 0
        for protocol in CommunicationProtocol:
            assert protocol in framework.active_protocols
            
        # Test that default feedback mechanisms are added
        assert len(framework.active_feedback_mechanisms) > 0
        for mechanism in FeedbackMechanism:
            assert mechanism in framework.active_feedback_mechanisms
            
        # Test that default improvement processes are added
        assert len(framework.active_improvement_processes) > 0
        for process in ImprovementProcess:
            assert process in framework.active_improvement_processes
            
        # Test that default collaboration workflows are added
        assert len(framework.active_workflows) > 0
        for workflow in CollaborationWorkflow:
            assert workflow in framework.active_workflows
            
    def test_add_responsibility(self):
        """Test adding responsibilities to the framework."""
        framework = HumanAIFramework()
        
        # Clear existing responsibilities
        framework.responsibilities = {
            Role.HUMAN: [],
            Role.AI: []
        }
        
        # Add a responsibility for each role
        human_responsibility = "Test human responsibility"
        ai_responsibility = "Test AI responsibility"
        
        framework.add_responsibility(Role.HUMAN, human_responsibility)
        framework.add_responsibility(Role.AI, ai_responsibility)
        
        # Test that the responsibilities were added
        assert len(framework.responsibilities[Role.HUMAN]) == 1
        assert len(framework.responsibilities[Role.AI]) == 1
        
        assert framework.responsibilities[Role.HUMAN][0].description == human_responsibility
        assert framework.responsibilities[Role.AI][0].description == ai_responsibility
        
        assert framework.responsibilities[Role.HUMAN][0].role == Role.HUMAN
        assert framework.responsibilities[Role.AI][0].role == Role.AI
        
    def test_add_ethical_principle(self):
        """Test adding ethical principles to the framework."""
        framework = HumanAIFramework()
        
        # Clear existing principles
        framework.active_principles.clear()
        
        # Add a principle
        framework.add_ethical_principle(EthicalPrinciple.TRANSPARENCY)
        
        # Test that the principle was added
        assert len(framework.active_principles) == 1
        assert EthicalPrinciple.TRANSPARENCY in framework.active_principles
        
    def test_add_communication_protocol(self):
        """Test adding communication protocols to the framework."""
        framework = HumanAIFramework()
        
        # Clear existing protocols
        framework.active_protocols.clear()
        
        # Add a protocol
        framework.add_communication_protocol(CommunicationProtocol.STRUCTURED_DIALOGUE)
        
        # Test that the protocol was added
        assert len(framework.active_protocols) == 1
        assert CommunicationProtocol.STRUCTURED_DIALOGUE in framework.active_protocols
        
    def test_add_feedback_mechanism(self):
        """Test adding feedback mechanisms to the framework."""
        framework = HumanAIFramework()
        
        # Clear existing mechanisms
        framework.active_feedback_mechanisms.clear()
        
        # Add a mechanism
        framework.add_feedback_mechanism(FeedbackMechanism.IMMEDIATE)
        
        # Test that the mechanism was added
        assert len(framework.active_feedback_mechanisms) == 1
        assert FeedbackMechanism.IMMEDIATE in framework.active_feedback_mechanisms
        
    def test_add_improvement_process(self):
        """Test adding improvement processes to the framework."""
        framework = HumanAIFramework()
        
        # Clear existing processes
        framework.active_improvement_processes.clear()
        
        # Add a process
        framework.add_improvement_process(ImprovementProcess.CONTINUOUS_LEARNING)
        
        # Test that the process was added
        assert len(framework.active_improvement_processes) == 1
        assert ImprovementProcess.CONTINUOUS_LEARNING in framework.active_improvement_processes
        
    def test_add_collaboration_workflow(self):
        """Test adding collaboration workflows to the framework."""
        framework = HumanAIFramework()
        
        # Clear existing workflows
        framework.active_workflows.clear()
        
        # Add a workflow
        framework.add_collaboration_workflow(CollaborationWorkflow.TASK_DISTRIBUTION)
        
        # Test that the workflow was added
        assert len(framework.active_workflows) == 1
        assert CollaborationWorkflow.TASK_DISTRIBUTION in framework.active_workflows
        
    def test_get_responsibilities_by_role(self):
        """Test getting responsibilities by role."""
        framework = HumanAIFramework()
        
        # Clear existing responsibilities
        framework.responsibilities = {
            Role.HUMAN: [],
            Role.AI: []
        }
        
        # Add responsibilities
        human_responsibility = "Test human responsibility"
        ai_responsibility = "Test AI responsibility"
        
        framework.add_responsibility(Role.HUMAN, human_responsibility)
        framework.add_responsibility(Role.AI, ai_responsibility)
        
        # Test getting responsibilities by role
        human_responsibilities = framework.get_responsibilities_by_role(Role.HUMAN)
        ai_responsibilities = framework.get_responsibilities_by_role(Role.AI)
        
        assert len(human_responsibilities) == 1
        assert len(ai_responsibilities) == 1
        
        assert human_responsibilities[0].description == human_responsibility
        assert ai_responsibilities[0].description == ai_responsibility
        
    def test_generate_framework_summary(self):
        """Test generating a framework summary."""
        framework = HumanAIFramework()
        
        # Generate the summary
        summary = framework.generate_framework_summary()
        
        # Test that the summary is a non-empty string
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        # Test that key sections are included in the summary
        assert "Roles and Responsibilities" in summary
        assert "Ethical Considerations" in summary
        assert "Communication Protocols" in summary
        assert "Feedback Mechanisms" in summary
        assert "Iterative Improvement Processes" in summary
        assert "Collaborative Workflow" in summary