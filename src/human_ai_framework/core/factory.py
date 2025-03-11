"""
Factory module for creating instances of the Human-AI Interaction Framework.

This module provides factory methods for creating and configuring
instances of the framework with various settings and configurations.
"""
from typing import Dict, List, Optional, Any

from src.human_ai_framework.core.framework import (
    HumanAIFramework,
    Role,
    EthicalPrinciple,
    CommunicationProtocol,
    FeedbackMechanism,
    ImprovementProcess,
    CollaborationWorkflow
)


class HumanAIFrameworkFactory:
    """
    Factory class for creating instances of the Human-AI Framework.
    
    This class provides methods for creating and configuring instances
    of the framework with various settings and configurations.
    """
    
    @staticmethod
    def create_default_framework() -> HumanAIFramework:
        """
        Create a default instance of the Human-AI Framework.
        
        Returns:
            A default-configured HumanAIFramework instance
        """
        return HumanAIFramework()
    
    @staticmethod
    def create_custom_framework(
        human_responsibilities: Optional[List[str]] = None,
        ai_responsibilities: Optional[List[str]] = None,
        ethical_principles: Optional[List[EthicalPrinciple]] = None,
        communication_protocols: Optional[List[CommunicationProtocol]] = None,
        feedback_mechanisms: Optional[List[FeedbackMechanism]] = None,
        improvement_processes: Optional[List[ImprovementProcess]] = None,
        collaboration_workflows: Optional[List[CollaborationWorkflow]] = None
    ) -> HumanAIFramework:
        """
        Create a custom-configured instance of the Human-AI Framework.
        
        Args:
            human_responsibilities: List of human responsibility descriptions
            ai_responsibilities: List of AI responsibility descriptions
            ethical_principles: List of ethical principles to include
            communication_protocols: List of communication protocols to include
            feedback_mechanisms: List of feedback mechanisms to include
            improvement_processes: List of improvement processes to include
            collaboration_workflows: List of collaboration workflows to include
            
        Returns:
            A custom-configured HumanAIFramework instance
        """
        framework = HumanAIFramework()
        
        # Clear all default settings
        framework.responsibilities = {
            Role.HUMAN: [],
            Role.AI: []
        }
        framework.active_principles.clear()
        framework.active_protocols.clear()
        framework.active_feedback_mechanisms.clear()
        framework.active_improvement_processes.clear()
        framework.active_workflows.clear()
        
        # Add custom human responsibilities
        if human_responsibilities:
            for responsibility in human_responsibilities:
                framework.add_responsibility(Role.HUMAN, responsibility)
                
        # Add custom AI responsibilities
        if ai_responsibilities:
            for responsibility in ai_responsibilities:
                framework.add_responsibility(Role.AI, responsibility)
                
        # Add custom ethical principles
        if ethical_principles:
            for principle in ethical_principles:
                framework.add_ethical_principle(principle)
                
        # Add custom communication protocols
        if communication_protocols:
            for protocol in communication_protocols:
                framework.add_communication_protocol(protocol)
                
        # Add custom feedback mechanisms
        if feedback_mechanisms:
            for mechanism in feedback_mechanisms:
                framework.add_feedback_mechanism(mechanism)
                
        # Add custom improvement processes
        if improvement_processes:
            for process in improvement_processes:
                framework.add_improvement_process(process)
                
        # Add custom collaboration workflows
        if collaboration_workflows:
            for workflow in collaboration_workflows:
                framework.add_collaboration_workflow(workflow)
                
        return framework
    
    @staticmethod
    def create_framework_from_config(config: Dict[str, Any]) -> HumanAIFramework:
        """
        Create a framework instance from a configuration dictionary.
        
        Args:
            config: Configuration dictionary containing framework settings
            
        Returns:
            A configured HumanAIFramework instance based on the provided config
            
        Raises:
            ValueError: If the configuration format is invalid
        """
        try:
            # Extract configuration values
            human_responsibilities = config.get("human_responsibilities", [])
            ai_responsibilities = config.get("ai_responsibilities", [])
            
            # Process ethical principles
            principles_config = config.get("ethical_principles", [])
            ethical_principles = [
                EthicalPrinciple[name] for name in principles_config
                if name in EthicalPrinciple.__members__
            ]
            
            # Process communication protocols
            protocols_config = config.get("communication_protocols", [])
            communication_protocols = [
                CommunicationProtocol[name] for name in protocols_config
                if name in CommunicationProtocol.__members__
            ]
            
            # Process feedback mechanisms
            mechanisms_config = config.get("feedback_mechanisms", [])
            feedback_mechanisms = [
                FeedbackMechanism[name] for name in mechanisms_config
                if name in FeedbackMechanism.__members__
            ]
            
            # Process improvement processes
            processes_config = config.get("improvement_processes", [])
            improvement_processes = [
                ImprovementProcess[name] for name in processes_config
                if name in ImprovementProcess.__members__
            ]
            
            # Process collaboration workflows
            workflows_config = config.get("collaboration_workflows", [])
            collaboration_workflows = [
                CollaborationWorkflow[name] for name in workflows_config
                if name in CollaborationWorkflow.__members__
            ]
            
            # Create and return the framework
            return HumanAIFrameworkFactory.create_custom_framework(
                human_responsibilities=human_responsibilities,
                ai_responsibilities=ai_responsibilities,
                ethical_principles=ethical_principles,
                communication_protocols=communication_protocols,
                feedback_mechanisms=feedback_mechanisms,
                improvement_processes=improvement_processes,
                collaboration_workflows=collaboration_workflows
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid configuration format: {str(e)}") 