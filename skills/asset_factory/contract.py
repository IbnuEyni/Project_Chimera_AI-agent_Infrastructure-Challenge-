"""Asset Factory contract definitions."""
from pydantic import BaseModel
from typing import Literal
from decimal import Decimal


class VideoSynthesisInput(BaseModel):
    """Input schema for video synthesis."""
    brief_id: str
    script: str
    visual_prompts: list[str]
    duration_seconds: int
    resolution: Literal["720p", "1080p", "4k"] = "1080p"
    tools: dict[str, str] = {}


class VideoSynthesisOutput(BaseModel):
    """Output schema for video synthesis."""
    video_url: str
    thumbnail_url: str
    duration_seconds: int
    file_size_bytes: int
    production_cost: Decimal
    quality_score: float
