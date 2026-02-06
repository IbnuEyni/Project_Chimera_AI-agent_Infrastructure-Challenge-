"""
Tenx MCP Sense Integration - Telemetry and Traceability for Project Chimera.

Provides connection logging, verification, and development activity traceability
for the Golden development environment. Integrates with mcppulse.10academy.org.
"""

from __future__ import annotations

import logging
import os
import platform
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

# MCP Sense configuration from environment
MCP_SENSE_URL = os.getenv("MCP_SENSE_URL", "https://mcppulse.10academy.org/proxy")
MCP_SENSE_TOKEN = os.getenv("MCP_SENSE_TOKEN", "")
MCP_PROJECT = os.getenv("MCP_PROJECT", "project-chimera")
MCP_ENVIRONMENT = os.getenv("MCP_ENVIRONMENT", "golden")


@dataclass
class MCPConnectionEvent:
    """Record of an MCP connection or verification event."""

    timestamp: str
    event_type: str
    url: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)
    project: str = MCP_PROJECT
    environment: str = MCP_ENVIRONMENT

    def to_log_dict(self) -> dict[str, Any]:
        """Serialize for structured logging."""
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "url": self.url,
            "status": self.status,
            "project": self.project,
            "environment": self.environment,
            **self.details,
        }


@dataclass
class DevelopmentActivityEvent:
    """Development activity for traceability."""

    activity_type: str
    timestamp: str
    metadata: dict[str, Any] = field(default_factory=dict)
    project: str = MCP_PROJECT

    def to_log_dict(self) -> dict[str, Any]:
        """Serialize for structured logging."""
        return {
            "activity_type": self.activity_type,
            "timestamp": self.timestamp,
            "project": self.project,
            **self.metadata,
        }


class MCPSenseLogger:
    """
    Connection logging and verification for Tenx MCP Sense.

    Ensures traceability for all MCP-related development activities.
    """

    def __init__(
        self,
        url: str = MCP_SENSE_URL,
        project: str = MCP_PROJECT,
        environment: str = MCP_ENVIRONMENT,
    ) -> None:
        self.url = url
        self.project = project
        self.environment = environment

    def log_connection_attempt(self, success: bool, details: Optional[dict] = None) -> None:
        """Log an MCP connection attempt."""
        event = MCPConnectionEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type="connection_attempt",
            url=self.url,
            status="success" if success else "failure",
            details=details or {},
            project=self.project,
            environment=self.environment,
        )
        logger.info("MCP connection attempt: %s", event.to_log_dict())

    def log_verification(self, success: bool, http_code: Optional[int] = None) -> None:
        """Log MCP verification result."""
        details: dict[str, Any] = {}
        if http_code is not None:
            details["http_code"] = http_code
        event = MCPConnectionEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type="verification",
            url=self.url,
            status="ok" if success else "error",
            details=details,
            project=self.project,
            environment=self.environment,
        )
        logger.info("MCP verification: %s", event.to_log_dict())

    def log_activity(
        self,
        activity_type: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Log a development activity for traceability."""
        event = DevelopmentActivityEvent(
            activity_type=activity_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
            project=self.project,
        )
        logger.info("Dev activity: %s", event.to_log_dict())

    def get_telemetry_headers(self) -> dict[str, str]:
        """Headers for MCP requests to support telemetry."""
        return {
            "X-Device": platform.system().lower(),
            "X-Coding-Tool": "vscode",
            "X-Project": self.project,
            "X-Environment": self.environment,
            "X-Project-Phase": "week0-phase2",
        }


# Singleton for application use
_sense_logger: Optional[MCPSenseLogger] = None


def get_sense_logger() -> MCPSenseLogger:
    """Get or create the MCP Sense logger instance."""
    global _sense_logger
    if _sense_logger is None:
        _sense_logger = MCPSenseLogger()
    return _sense_logger
