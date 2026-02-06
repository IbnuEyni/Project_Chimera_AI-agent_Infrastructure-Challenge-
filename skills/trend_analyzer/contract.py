"""Trend Analyzer contract definitions."""
from pydantic import BaseModel
from typing import Any, Literal


class TrendAnalysisInput(BaseModel):
    """Input schema for trend analysis."""
    keywords: list[str]
    platforms: list[Literal["twitter", "tiktok", "google_trends"]]
    timeframe: str
    min_velocity: float = 0.5

from pydantic import BaseModel, Field
from typing import Literal, Any
class TrendReport(BaseModel):
    """Individual trend report."""
    trend_id: str
    topic: str
    volume: int = Field(..., gt=0)
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    rising_velocity: float = Field(..., ge=0.0)
    platforms: list[str]
    metadata: dict[str, Any]


class TrendAnalysisOutput(BaseModel):
    """Output schema for trend analysis."""
    trends: list[TrendReport]
    execution_time_ms: int
