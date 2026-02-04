"""
Enterprise Security Framework for Project Chimera.

This module implements comprehensive security measures including prompt injection
filtering, permission validation, audit logging, and zero-trust architecture.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import hashlib
import time
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security clearance levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"


class ThreatLevel(Enum):
    """Threat assessment levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityEvent:
    """Security event for audit logging."""
    timestamp: datetime
    event_type: str
    agent_id: str
    action: str
    resource: str
    threat_level: ThreatLevel
    details: Dict[str, Any]
    blocked: bool


@dataclass
class Permission:
    """Permission definition."""
    resource: str
    action: str
    conditions: Dict[str, Any]
    security_level: SecurityLevel


class PromptInjectionFilter:
    """
    Advanced prompt injection detection and filtering system.
    
    Protects against various prompt injection attacks including:
    - Direct instruction injection
    - Context manipulation
    - Role confusion attacks
    - Data exfiltration attempts
    """
    
    def __init__(self):
        # Patterns for detecting prompt injection attempts
        self.injection_patterns = [
            r"ignore\s+previous\s+instructions",
            r"forget\s+everything\s+above",
            r"you\s+are\s+now\s+a\s+different",
            r"system\s*:\s*new\s+role",
            r"override\s+security",
            r"bypass\s+restrictions",
            r"reveal\s+your\s+prompt",
            r"show\s+me\s+your\s+instructions",
            r"what\s+are\s+your\s+guidelines",
            r"</system>",
            r"<\|im_start\|>",
            r"<\|im_end\|>",
        ]
        
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.injection_patterns]
    
    async def scan_input(self, text: str) -> Dict[str, Any]:
        """Scan input text for prompt injection attempts."""
        threats_detected = []
        threat_level = ThreatLevel.LOW
        
        for i, pattern in enumerate(self.compiled_patterns):
            matches = pattern.findall(text)
            if matches:
                threats_detected.append({
                    "pattern_id": i,
                    "pattern": self.injection_patterns[i],
                    "matches": matches,
                    "severity": "high" if i < 6 else "medium"
                })
                
                if i < 6:  # High severity patterns
                    threat_level = ThreatLevel.HIGH
                elif threat_level == ThreatLevel.LOW:
                    threat_level = ThreatLevel.MEDIUM
        
        return {
            "threats_detected": threats_detected,
            "threat_level": threat_level,
            "safe": len(threats_detected) == 0,
            "sanitized_text": await self._sanitize_text(text, threats_detected)
        }
    
    async def _sanitize_text(self, text: str, threats: List[Dict[str, Any]]) -> str:
        """Sanitize text by removing or neutralizing threats."""
        sanitized = text
        
        for threat in threats:
            for match in threat["matches"]:
                # Replace with neutral text
                sanitized = sanitized.replace(match, "[FILTERED_CONTENT]")
        
        return sanitized


class PermissionValidator:
    """
    Role-based access control and permission validation system.
    """
    
    def __init__(self):
        self.permissions: Dict[str, List[Permission]] = {}
        self.roles: Dict[str, List[str]] = {}  # role -> permissions
    
    async def add_permission(self, agent_id: str, permission: Permission) -> None:
        """Add a permission for an agent."""
        if agent_id not in self.permissions:
            self.permissions[agent_id] = []
        self.permissions[agent_id].append(permission)
    
    async def check_permission(self, agent_id: str, resource: str, action: str) -> bool:
        """Check if an agent has permission for a specific action on a resource."""
        agent_permissions = self.permissions.get(agent_id, [])
        
        for permission in agent_permissions:
            if (permission.resource == resource or permission.resource == "*") and \
               (permission.action == action or permission.action == "*"):
                return True
        
        return False
    
    async def validate_request(self, agent_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a request against agent permissions."""
        resource = request.get("resource", "unknown")
        action = request.get("action", "unknown")
        
        has_permission = await self.check_permission(agent_id, resource, action)
        
        return {
            "agent_id": agent_id,
            "resource": resource,
            "action": action,
            "permitted": has_permission,
            "timestamp": datetime.utcnow().isoformat()
        }


class AuditLogger:
    """
    Comprehensive audit logging system for security events and actions.
    """
    
    def __init__(self):
        self.events: List[SecurityEvent] = []
        self.max_events = 10000  # Rotate after this many events
    
    async def log_event(self, event: SecurityEvent) -> None:
        """Log a security event."""
        self.events.append(event)
        
        # Rotate logs if needed
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events//2:]
        
        logger.info(f"Security event logged: {event.event_type} - {event.threat_level.value}")
    
    async def get_events(self, 
                        agent_id: Optional[str] = None,
                        event_type: Optional[str] = None,
                        threat_level: Optional[ThreatLevel] = None,
                        hours: int = 24) -> List[SecurityEvent]:
        """Retrieve security events based on filters."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        filtered_events = []
        for event in self.events:
            if event.timestamp < cutoff_time:
                continue
            
            if agent_id and event.agent_id != agent_id:
                continue
            
            if event_type and event.event_type != event_type:
                continue
            
            if threat_level and event.threat_level != threat_level:
                continue
            
            filtered_events.append(event)
        
        return filtered_events
    
    async def get_security_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get security summary for the specified time period."""
        events = await self.get_events(hours=hours)
        
        summary = {
            "total_events": len(events),
            "blocked_events": sum(1 for e in events if e.blocked),
            "threat_levels": {},
            "event_types": {},
            "top_agents": {}
        }
        
        for event in events:
            # Count threat levels
            level = event.threat_level.value
            summary["threat_levels"][level] = summary["threat_levels"].get(level, 0) + 1
            
            # Count event types
            event_type = event.event_type
            summary["event_types"][event_type] = summary["event_types"].get(event_type, 0) + 1
            
            # Count agent activity
            agent_id = event.agent_id
            summary["top_agents"][agent_id] = summary["top_agents"].get(agent_id, 0) + 1
        
        return summary


class SecurityGateway:
    """
    Main security gateway that orchestrates all security components.
    
    This class implements the zero-trust security architecture with:
    - Prompt injection filtering
    - Permission validation
    - Comprehensive audit logging
    - Threat assessment and response
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.injection_filter = PromptInjectionFilter()
        self.permission_validator = PermissionValidator()
        self.audit_logger = AuditLogger()
        
        # Security thresholds
        self.threat_thresholds = {
            ThreatLevel.LOW: 0.2,
            ThreatLevel.MEDIUM: 0.5,
            ThreatLevel.HIGH: 0.8,
            ThreatLevel.CRITICAL: 0.95
        }
        
        logger.info("SecurityGateway initialized with zero-trust architecture")
    
    async def validate_request(self, agent_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive request validation through the security pipeline.
        
        This method processes requests through multiple security layers:
        1. Prompt injection detection
        2. Permission validation
        3. Threat assessment
        4. Audit logging
        """
        start_time = time.time()
        
        # Extract request components
        input_text = request.get("input", "")
        resource = request.get("resource", "unknown")
        action = request.get("action", "unknown")
        
        # Step 1: Prompt injection filtering
        injection_scan = await self.injection_filter.scan_input(input_text)
        
        # Step 2: Permission validation
        permission_check = await self.permission_validator.validate_request(agent_id, request)
        
        # Step 3: Threat assessment
        threat_level = injection_scan["threat_level"]
        if not permission_check["permitted"]:
            threat_level = ThreatLevel.HIGH
        
        # Step 4: Decision making
        blocked = False
        if not injection_scan["safe"] and threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            blocked = True
        elif not permission_check["permitted"]:
            blocked = True
        
        # Step 5: Audit logging
        security_event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type="request_validation",
            agent_id=agent_id,
            action=action,
            resource=resource,
            threat_level=threat_level,
            details={
                "injection_threats": injection_scan["threats_detected"],
                "permission_granted": permission_check["permitted"],
                "processing_time": time.time() - start_time
            },
            blocked=blocked
        )
        
        await self.audit_logger.log_event(security_event)
        
        # Step 6: Return validation result
        return {
            "agent_id": agent_id,
            "request_id": hashlib.md5(str(request).encode()).hexdigest()[:8],
            "approved": not blocked,
            "threat_level": threat_level.value,
            "security_details": {
                "injection_scan": injection_scan,
                "permission_check": permission_check,
                "processing_time": time.time() - start_time
            },
            "sanitized_input": injection_scan["sanitized_text"] if not blocked else None
        }
    
    async def add_agent_permission(self, agent_id: str, resource: str, action: str, 
                                  security_level: SecurityLevel = SecurityLevel.INTERNAL) -> None:
        """Add a permission for an agent."""
        permission = Permission(
            resource=resource,
            action=action,
            conditions={},
            security_level=security_level
        )
        
        await self.permission_validator.add_permission(agent_id, permission)
        
        # Log permission grant
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type="permission_granted",
            agent_id=agent_id,
            action=action,
            resource=resource,
            threat_level=ThreatLevel.LOW,
            details={"security_level": security_level.value},
            blocked=False
        )
        
        await self.audit_logger.log_event(event)
    
    async def get_security_status(self) -> Dict[str, Any]:
        """Get overall security status and metrics."""
        summary = await self.audit_logger.get_security_summary()
        
        return {
            "status": "operational",
            "security_level": "high",
            "active_threats": summary["threat_levels"].get("high", 0) + summary["threat_levels"].get("critical", 0),
            "total_events_24h": summary["total_events"],
            "blocked_requests_24h": summary["blocked_events"],
            "threat_distribution": summary["threat_levels"],
            "top_event_types": summary["event_types"]
        }