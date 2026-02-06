# Skill: Video Synthesis

**Agent**: Artist  
**Version**: 1.0.0  
**Status**: Ready for Implementation

---

## Purpose

Generate high-quality video content from scripts and visual prompts using AI tools (Runway Gen-2, Pika, ElevenLabs).

---

## Input Contract

```python
from pydantic import BaseModel, Field
from typing import Literal

class VideoSynthesisInput(BaseModel):
    """Input schema for video synthesis."""
    
    brief_id: str = Field(
        ...,
        description="Content brief UUID"
    )
    
    script: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Video script"
    )
    
    visual_prompts: list[str] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="Visual generation prompts"
    )
    
    duration_seconds: int = Field(
        ...,
        ge=5,
        le=600,
        description="Target video duration (5-600 seconds)"
    )
    
    resolution: Literal["720p", "1080p", "4k"] = Field(
        default="1080p",
        description="Video resolution"
    )
    
    tools: dict[str, str] = Field(
        default={"video": "runway-gen2", "audio": "elevenlabs"},
        description="AI tools to use"
    )
```

---

## Output Contract

```python
from decimal import Decimal

class VideoSynthesisOutput(BaseModel):
    """Output schema for video synthesis."""
    
    asset_id: str = Field(
        ...,
        description="Generated asset UUID"
    )
    
    video_url: str = Field(
        ...,
        description="S3/CDN URL to video file"
    )
    
    thumbnail_url: str = Field(
        ...,
        description="S3/CDN URL to thumbnail"
    )
    
    duration_seconds: int = Field(
        ...,
        ge=0,
        description="Actual video duration"
    )
    
    file_size_bytes: int = Field(
        ...,
        ge=0,
        le=100_000_000,  # 100MB max
        description="Video file size"
    )
    
    production_cost: Decimal = Field(
        ...,
        ge=0,
        description="Total production cost in USD"
    )
    
    quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Quality assessment score"
    )
```

---

## Performance Requirements

- **Task Acceptance**: <100ms (acknowledges request)
- **Image Generation**: <30s per image
- **Video Generation**: <120s total completion
- **Quality Score**: >0.8
- **Success Rate**: >90%
- **Cost**: ~$2.00 per video

---

## Error Handling

```python
class VideoSynthesisError(Exception):
    """Base exception for video synthesis."""
    pass

class ToolUnavailableError(VideoSynthesisError):
    """Raised when AI tool is unavailable."""
    pass

class QualityThresholdError(VideoSynthesisError):
    """Raised when quality score < 0.8."""
    pass

class FileSizeExceededError(VideoSynthesisError):
    """Raised when file size > 100MB."""
    pass

class GenerationTimeoutError(VideoSynthesisError):
    """Raised when generation exceeds 120s."""
    pass
```

---

## Usage Example

```python
from skills.skill_video_synthesis import execute, VideoSynthesisInput

# Create input
input_data = VideoSynthesisInput(
    brief_id="brief-123",
    script="Explore the future of AI...",
    visual_prompts=[
        "Futuristic tech lab with neon lights",
        "AI chip glowing with energy"
    ],
    duration_seconds=30,
    resolution="1080p"
)

# Execute skill (async operation)
try:
    result = await execute(input_data)
    
    print(f"Video URL: {result.video_url}")
    print(f"Quality: {result.quality_score}")
    print(f"Cost: ${result.production_cost}")
    
except VideoSynthesisError as e:
    logger.error(f"Video synthesis failed: {e}")
```

---

## Implementation Notes

1. **Asynchronous Processing**: Task acceptance is immediate (<100ms), generation runs async
2. **Tool Selection**: Fallback from Runway → Pika if primary fails
3. **Quality Validation**: Use CLIP score for visual-text alignment
4. **Cost Tracking**: Log all API calls to ledger table
5. **File Management**: Upload to S3, generate signed URLs
6. **Retry Logic**: 3 attempts with exponential backoff

---

## Workflow

```
1. Accept task (<100ms)
   ↓
2. Generate images from visual_prompts (30s)
   ↓
3. Generate video from images (60s)
   ↓
4. Generate audio from script (20s)
   ↓
5. Combine video + audio (10s)
   ↓
6. Validate quality (CLIP score)
   ↓
7. Upload to S3
   ↓
8. Return result
```

---

## Testing Strategy

- Unit tests with mocked AI tool responses
- Integration tests with test API keys
- Performance tests to validate <120s completion
- Quality tests to ensure score >0.8
- Cost tracking validation

---

## Dependencies

- `httpx`: Async HTTP client
- `pydantic`: Schema validation
- `boto3`: S3 upload
- `ffmpeg-python`: Video processing
- `torch`: CLIP model for quality scoring

---

## References

- Functional Spec: `../../specs/functional.md` (Section 3)
- Technical Spec: `../../specs/technical.md` (Asset Production)
