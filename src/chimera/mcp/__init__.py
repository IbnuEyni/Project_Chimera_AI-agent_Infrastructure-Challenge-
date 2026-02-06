"""
Model Context Protocol (MCP) Integration Layer for Project Chimera.

This module provides the universal AI interface integration through MCP,
enabling seamless connection to 200+ MCP servers and dynamic capability discovery.

Tenx MCP Sense integration for telemetry and traceability:
    from chimera.mcp.sense import get_sense_logger
"""

from typing import Dict, List, Optional, Any, Callable

from chimera.mcp.sense import MCPSenseLogger, get_sense_logger

__all__ = [
    "MCPIntegrationLayer",
    "MCPServer",
    "MCPServerStatus",
    "MCPCapability",
    "MCPSenseLogger",
    "get_sense_logger",
]
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import json

logger = logging.getLogger(__name__)


class MCPServerStatus(Enum):
    """MCP Server status enumeration."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    INITIALIZING = "initializing"


@dataclass
class MCPCapability:
    """MCP capability definition."""
    name: str
    description: str
    server: str
    parameters: Dict[str, Any]
    version: str


@dataclass
class MCPServer:
    """MCP Server configuration."""
    name: str
    url: str
    capabilities: List[MCPCapability]
    status: MCPServerStatus
    metadata: Dict[str, Any]


class MCPIntegrationLayer:
    """
    Universal AI interface integration through Model Context Protocol.
    
    This class manages connections to multiple MCP servers and provides
    dynamic capability discovery and semantic tool orchestration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.servers: Dict[str, MCPServer] = {}
        self.capabilities: Dict[str, MCPCapability] = {}
        self.active_connections: Dict[str, Any] = {}
        
        logger.info("MCPIntegrationLayer initialized")
    
    async def register_server(self, server_config: Dict[str, Any]) -> None:
        """Register a new MCP server."""
        server = MCPServer(
            name=server_config["name"],
            url=server_config["url"],
            capabilities=[],
            status=MCPServerStatus.INITIALIZING,
            metadata=server_config.get("metadata", {})
        )
        
        self.servers[server.name] = server
        logger.info(f"MCP server '{server.name}' registered")
        
        # Attempt to connect and discover capabilities
        await self._connect_server(server.name)
    
    async def _connect_server(self, server_name: str) -> None:
        """Connect to an MCP server and discover capabilities."""
        server = self.servers.get(server_name)
        if not server:
            logger.error(f"Server '{server_name}' not found")
            return
        
        try:
            # Simulate MCP connection and capability discovery
            await asyncio.sleep(0.1)
            
            # Mock capabilities for demonstration
            mock_capabilities = [
                MCPCapability(
                    name=f"{server_name}_capability_1",
                    description=f"Primary capability for {server_name}",
                    server=server_name,
                    parameters={"timeout": 30, "retries": 3},
                    version="1.0.0"
                ),
                MCPCapability(
                    name=f"{server_name}_capability_2",
                    description=f"Secondary capability for {server_name}",
                    server=server_name,
                    parameters={"batch_size": 100},
                    version="1.0.0"
                )
            ]
            
            server.capabilities = mock_capabilities
            server.status = MCPServerStatus.CONNECTED
            
            # Register capabilities globally
            for capability in mock_capabilities:
                self.capabilities[capability.name] = capability
            
            logger.info(f"Connected to MCP server '{server_name}' with {len(mock_capabilities)} capabilities")
            
        except Exception as e:
            server.status = MCPServerStatus.ERROR
            logger.error(f"Failed to connect to MCP server '{server_name}': {e}")
    
    async def discover_capabilities(self, query: str) -> List[MCPCapability]:
        """Discover capabilities matching a query."""
        matching_capabilities = []
        
        for capability in self.capabilities.values():
            if query.lower() in capability.name.lower() or query.lower() in capability.description.lower():
                matching_capabilities.append(capability)
        
        logger.info(f"Found {len(matching_capabilities)} capabilities matching '{query}'")
        return matching_capabilities
    
    async def execute_capability(self, capability_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a capability through its MCP server."""
        capability = self.capabilities.get(capability_name)
        if not capability:
            raise ValueError(f"Capability '{capability_name}' not found")
        
        server = self.servers.get(capability.server)
        if not server or server.status != MCPServerStatus.CONNECTED:
            raise RuntimeError(f"Server '{capability.server}' not available")
        
        try:
            # Simulate capability execution
            await asyncio.sleep(0.2)
            
            result = {
                "capability": capability_name,
                "server": capability.server,
                "parameters": parameters,
                "result": f"Executed {capability_name} successfully",
                "execution_time": 0.2,
                "success": True
            }
            
            logger.info(f"Executed capability '{capability_name}' on server '{capability.server}'")
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute capability '{capability_name}': {e}")
            raise
    
    async def get_server_status(self, server_name: str) -> Optional[MCPServerStatus]:
        """Get the status of an MCP server."""
        server = self.servers.get(server_name)
        return server.status if server else None
    
    async def list_servers(self) -> List[Dict[str, Any]]:
        """List all registered MCP servers."""
        return [
            {
                "name": server.name,
                "url": server.url,
                "status": server.status.value,
                "capabilities_count": len(server.capabilities),
                "metadata": server.metadata
            }
            for server in self.servers.values()
        ]
    
    async def list_capabilities(self) -> List[Dict[str, Any]]:
        """List all available capabilities."""
        return [
            {
                "name": capability.name,
                "description": capability.description,
                "server": capability.server,
                "version": capability.version,
                "parameters": capability.parameters
            }
            for capability in self.capabilities.values()
        ]
    
    async def semantic_tool_selection(self, task_description: str) -> List[MCPCapability]:
        """
        Intelligently select optimal tools for a task using semantic analysis.
        
        This method analyzes the task description and recommends the most
        suitable capabilities based on semantic matching and historical performance.
        """
        # Simplified semantic matching - in production, this would use
        # advanced NLP and embedding-based similarity
        keywords = task_description.lower().split()
        
        scored_capabilities = []
        for capability in self.capabilities.values():
            score = 0
            capability_text = f"{capability.name} {capability.description}".lower()
            
            for keyword in keywords:
                if keyword in capability_text:
                    score += 1
            
            if score > 0:
                scored_capabilities.append((capability, score))
        
        # Sort by score and return top capabilities
        scored_capabilities.sort(key=lambda x: x[1], reverse=True)
        selected_capabilities = [cap for cap, score in scored_capabilities[:5]]
        
        logger.info(f"Selected {len(selected_capabilities)} capabilities for task: '{task_description}'")
        return selected_capabilities
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all MCP servers."""
        health_status = {
            "total_servers": len(self.servers),
            "connected_servers": 0,
            "total_capabilities": len(self.capabilities),
            "server_details": {}
        }
        
        for server_name, server in self.servers.items():
            if server.status == MCPServerStatus.CONNECTED:
                health_status["connected_servers"] += 1
            
            health_status["server_details"][server_name] = {
                "status": server.status.value,
                "capabilities_count": len(server.capabilities),
                "url": server.url
            }
        
        return health_status