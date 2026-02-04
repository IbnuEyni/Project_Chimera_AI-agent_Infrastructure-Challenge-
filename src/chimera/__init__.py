"""
Project Chimera - Advanced AI Agent Swarm System

An enterprise-grade platform for autonomous digital intelligence with economic
capabilities and social interaction features.
"""

__version__ = "0.1.0"
__author__ = "10Academy"
__email__ = "chimera@10academy.org"

from .core import ChimeraSwarm
from .agents import Agent, AgentPool
from .mcp import MCPIntegrationLayer
from .security import SecurityGateway
from .commerce import AgenticCommerce

__all__ = [
    "ChimeraSwarm",
    "Agent",
    "AgentPool", 
    "MCPIntegrationLayer",
    "SecurityGateway",
    "AgenticCommerce",
]