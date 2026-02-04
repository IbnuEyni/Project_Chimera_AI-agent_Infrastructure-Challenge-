"""
Agent system for Project Chimera.

This module defines the base agent classes and agent pool management
for the swarm intelligence system.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class AgentCapability:
    """Agent capability definition."""
    name: str
    description: str
    parameters: Dict[str, Any]
    confidence: float


class Agent(ABC):
    """
    Base agent class for all agents in the Chimera system.
    
    All agents inherit from this base class and implement the execute method
    for their specific functionality.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        self.id = agent_id or str(uuid.uuid4())
        self.name = name or f"Agent-{self.id[:8]}"
        self.status = AgentStatus.IDLE
        self.capabilities: List[AgentCapability] = []
        self.metadata: Dict[str, Any] = {}
        
        logger.info(f"Agent {self.name} ({self.id}) initialized")
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task and return the result."""
        pass
    
    async def get_capabilities(self) -> List[AgentCapability]:
        """Get agent capabilities."""
        return self.capabilities
    
    async def update_status(self, status: AgentStatus) -> None:
        """Update agent status."""
        self.status = status
        logger.debug(f"Agent {self.name} status updated to {status.value}")


class PlannerAgent(Agent):
    """Agent specialized in task planning and decomposition."""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id, f"Planner-{agent_id[:8] if agent_id else 'unknown'}")
        self.capabilities = [
            AgentCapability(
                name="task_decomposition",
                description="Break down complex tasks into subtasks",
                parameters={"max_depth": 5, "min_complexity": 0.1},
                confidence=0.9
            )
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Plan and decompose a task."""
        await self.update_status(AgentStatus.BUSY)
        
        try:
            # Simulate planning logic
            await asyncio.sleep(0.1)
            
            result = {
                "subtasks": [
                    {"id": str(uuid.uuid4()), "description": f"Subtask 1 for {task.get('description', 'unknown')}"},
                    {"id": str(uuid.uuid4()), "description": f"Subtask 2 for {task.get('description', 'unknown')}"}
                ],
                "execution_order": "parallel",
                "estimated_duration": 300
            }
            
            await self.update_status(AgentStatus.IDLE)
            return result
            
        except Exception as e:
            await self.update_status(AgentStatus.ERROR)
            logger.error(f"Planner agent {self.name} failed: {e}")
            raise


class WorkerAgent(Agent):
    """Agent specialized in task execution."""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id, f"Worker-{agent_id[:8] if agent_id else 'unknown'}")
        self.capabilities = [
            AgentCapability(
                name="task_execution",
                description="Execute assigned tasks",
                parameters={"max_concurrent": 3, "timeout": 600},
                confidence=0.85
            )
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task."""
        await self.update_status(AgentStatus.BUSY)
        
        try:
            # Simulate work execution
            await asyncio.sleep(0.2)
            
            result = {
                "output": f"Completed: {task.get('description', 'unknown task')}",
                "execution_time": 0.2,
                "success": True
            }
            
            await self.update_status(AgentStatus.IDLE)
            return result
            
        except Exception as e:
            await self.update_status(AgentStatus.ERROR)
            logger.error(f"Worker agent {self.name} failed: {e}")
            raise


class JudgeAgent(Agent):
    """Agent specialized in quality assurance and validation."""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id, f"Judge-{agent_id[:8] if agent_id else 'unknown'}")
        self.capabilities = [
            AgentCapability(
                name="quality_assessment",
                description="Assess quality of task results",
                parameters={"quality_threshold": 0.8, "criteria": ["accuracy", "completeness"]},
                confidence=0.95
            )
        ]
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Judge the quality of a task result."""
        await self.update_status(AgentStatus.BUSY)
        
        try:
            # Simulate quality assessment
            await asyncio.sleep(0.1)
            
            result = {
                "quality_score": 0.92,
                "passed": True,
                "feedback": "Task completed successfully with high quality",
                "recommendations": []
            }
            
            await self.update_status(AgentStatus.IDLE)
            return result
            
        except Exception as e:
            await self.update_status(AgentStatus.ERROR)
            logger.error(f"Judge agent {self.name} failed: {e}")
            raise


class AgentPool:
    """
    Agent pool management for efficient agent allocation and load balancing.
    """
    
    def __init__(self, pool_type: str, capacity: int = 10):
        self.pool_type = pool_type
        self.capacity = capacity
        self.agents: List[Agent] = []
        self.active_tasks: Dict[str, str] = {}  # task_id -> agent_id
        
        logger.info(f"AgentPool '{pool_type}' initialized with capacity {capacity}")
    
    async def add_agent(self, agent: Agent) -> None:
        """Add an agent to the pool."""
        if len(self.agents) < self.capacity:
            self.agents.append(agent)
            logger.info(f"Agent {agent.name} added to pool '{self.pool_type}'")
        else:
            raise ValueError(f"Pool '{self.pool_type}' is at capacity")
    
    async def get_available_agent(self) -> Optional[Agent]:
        """Get an available agent from the pool."""
        for agent in self.agents:
            if agent.status == AgentStatus.IDLE:
                return agent
        return None
    
    async def assign_task(self, task_id: str, agent: Agent) -> None:
        """Assign a task to an agent."""
        self.active_tasks[task_id] = agent.id
        await agent.update_status(AgentStatus.BUSY)
    
    async def complete_task(self, task_id: str) -> None:
        """Mark a task as completed and free the agent."""
        if task_id in self.active_tasks:
            agent_id = self.active_tasks.pop(task_id)
            agent = next((a for a in self.agents if a.id == agent_id), None)
            if agent:
                await agent.update_status(AgentStatus.IDLE)
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get pool status information."""
        status_counts = {}
        for agent in self.agents:
            status = agent.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "pool_type": self.pool_type,
            "total_agents": len(self.agents),
            "capacity": self.capacity,
            "active_tasks": len(self.active_tasks),
            "status_distribution": status_counts
        }