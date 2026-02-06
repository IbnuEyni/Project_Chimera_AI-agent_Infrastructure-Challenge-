# 🎯 Chimera Agent Skills Catalog

**Version**: 1.0.0  
**Last Updated**: 2026-02-06

---

## Overview

In Project Chimera, a **Skill** is a containerized, atomic capability package with strict Pydantic-validated interfaces. Every skill adheres to the `ChimeraSkill` base class to ensure reliability within the Swarm.

---

## Skill Architecture

### Base Interface Contract

All skills implement the `ChimeraSkill` abstract base class with generic type enforcement:

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Generic, TypeVar

T_In = TypeVar("T_In", bound=BaseModel)
T_Out = TypeVar("T_Out", bound=BaseModel)

class ChimeraSkill(ABC, Generic[T_In, T_Out]):
    """
    Base class for all autonomous skills.
    Forces strict typing and safety validation.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique skill identifier."""
        pass

    @abstractmethod
    async def execute(self, params: T_In) -> T_Out:
        """Core skill logic with MCP tool integration."""
        pass

    def validate_safety(self, params: T_In) -> bool:
        """Pre-execution safety check (Governance Layer)."""
        return True
```

### Directory Structure
```
skills/
├── README.md                # Skill Master Contract (this file)
├── interface.py             # ChimeraSkill base class
├── trend_analyzer/          # Perception Skill (The Oracle)
│   ├── __init__.py
│   ├── contract.py
│   └── README.md
├── asset_factory/           # Creative Skill (The Creator)
│   ├── __init__.py
│   ├── contract.py
│   └── README.md
└── commerce_manager/        # Economic Skill (The Treasurer)
    ├── __init__.py
    ├── contract.py
    └── README.md
```

---

## Critical Skills Registry

### 1. Skill: `trend_analyzer` (The Oracle)
**Agent**: Scout  
**Purpose**: Scans MCP resources to identify high-engagement opportunities

**Input Contract**:
```json
{
  "sources": ["twitter://trends", "news://ethiopia/tech"],
  "relevance_threshold": 0.85,
  "time_window": "4h",
  "keywords": ["AI", "Crypto"],
  "platforms": ["twitter", "tiktok", "google_trends"]
}
```

**Output Contract**:
```json
{
  "signals": [
    {
      "topic": "USDC Stability",
      "alpha_score": 0.92,
      "volume": 15000,
      "sentiment_score": 0.75,
      "rising_velocity": 2.3,
      "context": "Regulatory clarity driving adoption"
    }
  ],
  "recommended_action": "CREATE_POST",
  "execution_time_ms": 1850
}
```

**Performance**: <2000ms  
**Cost**: ~$0.02 per analysis  
**Status**: Ready for Implementation

---

### 2. Skill: `asset_factory` (The Creator)
**Agent**: Artist  
**Purpose**: Generates character-consistent multimodal content using MCP-driven GenAI tools

**Input Contract**:
```json
{
  "persona_id": "chimera-alpha-01",
  "brief_id": "brief-123",
  "script": "Explore the future of AI...",
  "prompt_logic": "Deep-tech aesthetic, neon lighting",
  "visual_prompts": [
    "Futuristic tech lab with neon lights",
    "AI chip glowing with energy"
  ],
  "format": "VIDEO_HD",
  "duration_seconds": 30,
  "resolution": "1080p",
  "character_consistency_id": "lora_v4_face_lock"
}
```

**Output Contract**:
```json
{
  "asset_id": "asset-456",
  "media_url": "s3://chimera-assets/post_01.mp4",
  "thumbnail_url": "s3://chimera-assets/thumb_01.jpg",
  "checksum": "sha256_abc123...",
  "duration_seconds": 30,
  "file_size_bytes": 15728640,
  "production_cost": 11.80,
  "quality_score": 0.92,
  "ai_label_applied": true
}
```

**Performance**: <120s for completion  
**Cost**: ~$2.00 per video  
**Status**: Ready for Implementation

---

### 3. Skill: `commerce_manager` (The Treasurer)
**Agent**: CFO  
**Purpose**: Executes on-chain transactions and manages agent P&L via Coinbase AgentKit

**Input Contract**:
```json
{
  "request_id": "req-789",
  "agent_id": "agent-123",
  "action": "TRANSFER | DEPLOY_TOKEN | APPROVE_SPEND",
  "recipient_address": "0xabcd...1234",
  "amount_usdc": 10.50,
  "priority": "normal",
  "projected_roi": 2.5,
  "justification": "Payment for API credits"
}
```

**Output Contract**:
```json
{
  "request_id": "req-789",
  "approved": true,
  "tx_hash": "0x5678...9abc",
  "new_balance": 145.20,
  "status": "CONFIRMED_ON_BASE",
  "approval_signature": "0x1234...abcd",
  "budget_remaining": {
    "daily": 485.0,
    "weekly": 2340.0,
    "monthly": 8920.0
  },
  "risk_score": 0.25
}
```

**Performance**: <300ms  
**Cost**: $0.00 (internal) + gas fees  
**Status**: Ready for Implementation

---

## Skill Implementation Pattern

### Example: Trend Analyzer Skill

```python
# skills/trend_analyzer/__init__.py
from skills.interface import ChimeraSkill
from .contract import TrendAnalyzerInput, TrendAnalyzerOutput

class TrendAnalyzer(ChimeraSkill[TrendAnalyzerInput, TrendAnalyzerOutput]):
    """The Oracle - Identifies high-engagement opportunities."""
    
    @property
    def name(self) -> str:
        return "trend_analyzer"
    
    async def execute(self, params: TrendAnalyzerInput) -> TrendAnalyzerOutput:
        """Scan MCP resources for trending topics."""
        # 1. Validate safety
        if not self.validate_safety(params):
            raise SecurityError("Safety validation failed")
        
        # 2. Call MCP social-media tools
        signals = await self._scan_platforms(params)
        
        # 3. Calculate alpha scores
        ranked_signals = self._rank_by_engagement(signals)
        
        # 4. Return structured output
        return TrendAnalyzerOutput(
            signals=ranked_signals,
            recommended_action="CREATE_POST",
            execution_time_ms=1850
        )
    
    def validate_safety(self, params: TrendAnalyzerInput) -> bool:
        """Ensure sources are whitelisted."""
        allowed_sources = ["twitter://", "news://", "tiktok://"]
        return all(
            any(src.startswith(allowed) for allowed in allowed_sources)
            for src in params.sources
        )
```

---

## Usage Example

```python
from skills.trend_analyzer import TrendAnalyzer, TrendAnalyzerInput

# Initialize skill
analyzer = TrendAnalyzer()

# Create input
input_data = TrendAnalyzerInput(
    sources=["twitter://trends", "news://ethiopia/tech"],
    relevance_threshold=0.85,
    time_window="4h",
    keywords=["AI", "Crypto"],
    platforms=["twitter", "tiktok"]
)

# Execute skill
try:
    result = await analyzer.execute(input_data)
    
    for signal in result.signals:
        print(f"Topic: {signal.topic}")
        print(f"Alpha Score: {signal.alpha_score}")
        print(f"Action: {result.recommended_action}")
        
except Exception as e:
    logger.error(f"Skill execution failed: {e}")
```

---

## Development Guidelines

### 1. Contract-First Design
- Define Pydantic schemas in `contract.py` before implementation
- Use strict typing with `Generic[T_In, T_Out]`
- Validate all inputs/outputs

### 2. Safety-First Execution
- Implement `validate_safety()` for pre-execution checks
- Whitelist external resources
- Rate limit API calls
- Log all executions

### 3. MCP Integration
- Use MCP tools for external service calls
- Implement retry logic with exponential backoff
- Handle timeouts gracefully
- Cache results when appropriate

### 4. Testing Requirements
- Unit tests with mocked MCP responses
- Integration tests with test credentials
- Performance tests against SLA targets
- Security tests for safety validation
- Minimum 80% code coverage

---

## Performance Targets

| Skill | Target Latency | Success Rate | Cost | Priority |
|-------|---------------|--------------|------|----------|
| trend_analyzer | <2000ms | >95% | $0.02 | Critical |
| asset_factory | <120s | >90% | $2.00 | Critical |
| commerce_manager | <300ms | >99% | $0.00 | Critical |

---

## Adding New Skills

1. Create directory: `skills/skill_name/`
2. Implement `ChimeraSkill` interface
3. Define contracts in `contract.py`
4. Document in `README.md`
5. Write comprehensive tests
6. Update this registry

---

## References

- Base Interface: `skills/interface.py`
- Specifications: `../specs/functional.md`
- Tooling Strategy: `../research/tooling_strategy.md`
