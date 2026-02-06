# Skill: Trend Analysis

**Agent**: Scout  
**Version**: 1.0.0  
**Status**: Ready for Implementation

---

## Purpose

Analyze social media trends from multiple platforms (Twitter, TikTok, Google Trends) to identify rising topics for content strategy.

---

## Input Contract

```python
from pydantic import BaseModel, Field
from typing import Literal

class TrendAnalysisInput(BaseModel):
    """Input schema for trend analysis."""
    
    keywords: list[str] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="Search keywords"
    )
    
    platforms: list[Literal["twitter", "tiktok", "google_trends"]] = Field(
        ...,
        min_items=1,
        description="Platforms to analyze"
    )
    
    timeframe: str = Field(
        ...,
        pattern=r"^\d+[hdwm]$",
        description="ISO8601 duration (e.g., '24h', '7d')"
    )
    
    min_velocity: float = Field(
        default=0.5,
        ge=0.0,
        le=10.0,
        description="Minimum rising velocity threshold"
    )
```

---

## Output Contract

```python
from decimal import Decimal

class TrendReport(BaseModel):
    """Individual trend report."""
    
    trend_id: str
    topic: str
    volume: int = Field(ge=0)
    sentiment_score: float = Field(ge=-1.0, le=1.0)
    rising_velocity: float = Field(ge=0.0)
    platforms: list[str]
    metadata: dict

class TrendAnalysisOutput(BaseModel):
    """Output schema for trend analysis."""
    
    trends: list[TrendReport] = Field(
        ...,
        min_items=1,
        max_items=20,
        description="Detected trends"
    )
    
    execution_time_ms: int = Field(
        ...,
        ge=0,
        description="Execution time in milliseconds"
    )
```

---

## Performance Requirements

- **Latency**: <2000ms (P95)
- **Success Rate**: >95%
- **Cost**: ~$0.02 per execution
- **Deduplication**: >90% noise removal
- **Sentiment Accuracy**: >85%

---

## Error Handling

```python
class TrendAnalysisError(Exception):
    """Base exception for trend analysis."""
    pass

class InvalidTimeframeError(TrendAnalysisError):
    """Raised when timeframe format is invalid."""
    pass

class PlatformUnavailableError(TrendAnalysisError):
    """Raised when platform API is unavailable."""
    pass

class RateLimitExceededError(TrendAnalysisError):
    """Raised when API rate limit is hit."""
    pass
```

---

## Usage Example

```python
from skills.skill_trend_analysis import execute, TrendAnalysisInput

# Create input
input_data = TrendAnalysisInput(
    keywords=["AI", "Crypto"],
    platforms=["twitter", "tiktok"],
    timeframe="24h",
    min_velocity=0.5
)

# Execute skill
try:
    result = await execute(input_data)
    
    for trend in result.trends:
        print(f"Topic: {trend.topic}")
        print(f"Volume: {trend.volume}")
        print(f"Sentiment: {trend.sentiment_score}")
        
except TrendAnalysisError as e:
    logger.error(f"Trend analysis failed: {e}")
```

---

## Implementation Notes

1. Use MCP social-media-mcp server for API access
2. Implement semantic deduplication using embeddings
3. Calculate sentiment using pre-trained models
4. Cache results for 15 minutes to reduce API costs
5. Implement exponential backoff for rate limits

---

## Testing Strategy

- Unit tests with mocked API responses
- Integration tests with test API keys
- Performance tests to validate <2s latency
- Load tests with 100 concurrent requests

---

## Dependencies

- `httpx`: Async HTTP client
- `pydantic`: Schema validation
- `transformers`: Sentiment analysis
- `redis`: Result caching

---

## References

- Functional Spec: `../../specs/functional.md` (Section 1)
- Technical Spec: `../../specs/technical.md` (Trend Analysis Interface)
