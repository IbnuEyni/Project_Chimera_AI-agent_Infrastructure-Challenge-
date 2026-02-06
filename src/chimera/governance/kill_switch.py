"""
Kill-Switch Protocol for Project Chimera

Black Swan Protection:
- Low confidence scores (<0.5)
- Market crash signals
- Budget anomalies
- Security breaches
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SystemState(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    EMERGENCY_HALT = "emergency_halt"


class PanicReason(str, Enum):
    LOW_CONFIDENCE = "low_confidence"
    MARKET_CRASH = "market_crash"
    BUDGET_ANOMALY = "budget_anomaly"
    SECURITY_BREACH = "security_breach"


class PanicException(Exception):
    """Triggers immediate halt of all commerce transactions."""
    
    def __init__(self, reason: PanicReason, details: str, confidence_score: Optional[float] = None):
        self.reason = reason
        self.details = details
        self.confidence_score = confidence_score
        super().__init__(f"PANIC: {reason.value} - {details}")


class SystemPauseFlag(BaseModel):
    is_paused: bool = False
    state: SystemState = SystemState.ACTIVE
    reason: Optional[PanicReason] = None
    details: Optional[str] = None
    paused_at: Optional[datetime] = None


class KillSwitchProtocol:
    def __init__(self, min_confidence: float = 0.5):
        self.min_confidence = min_confidence
        self.pause_flag = SystemPauseFlag()
    
    def check_confidence(self, confidence_score: float) -> None:
        if confidence_score < self.min_confidence:
            raise PanicException(
                PanicReason.LOW_CONFIDENCE,
                f"Confidence {confidence_score} below {self.min_confidence}",
                confidence_score
            )
    
    def check_market_crash(self, volatility: float) -> None:
        if volatility > 50:
            raise PanicException(
                PanicReason.MARKET_CRASH,
                f"Volatility {volatility}% exceeds threshold"
            )
    
    def trigger_halt(self, reason: PanicReason, details: str) -> None:
        self.pause_flag.is_paused = True
        self.pause_flag.state = SystemState.EMERGENCY_HALT
        self.pause_flag.reason = reason
        self.pause_flag.details = details
        self.pause_flag.paused_at = datetime.utcnow()
        raise PanicException(reason, details)
