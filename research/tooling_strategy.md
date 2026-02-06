# 🛠️ Project Chimera - Tooling & Skills Strategy

**Version**: 1.0.0  
**Last Updated**: 2026-02-06  
**Status**: Active Development

---

## Overview

This document defines the tooling ecosystem for Project Chimera, divided into two categories:
1. **Developer Tools (MCP)**: Tools that assist developers during development
2. **Agent Skills (Runtime)**: Capabilities that Chimera agents use during production

---

## Part A: Developer Tools (MCP Servers)

### The "Orchestrator's Workbench" - Strategic MCP Stack

To maintain high-velocity, spec-driven development, we utilize the Model Context Protocol (MCP) to bridge the IDE and system state. Each tool serves a strategic purpose in the development workflow.

---

### Core MCP Servers

#### 1. **sequential-thinking** - Architecture Planning
**Strategic Utility**: Prevents "LLM Tunnel Vision" by forcing iterative architecture thinking before coding

**Configuration**:
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

**Use Cases**:
- Plan complex features before implementation
- Break down architectural decisions
- Document reasoning for ADRs
- Prevent premature optimization

**Workflow Integration**: Required before any major code changes

---

#### 2. **filesystem** - Spec-Driven Development
**Strategic Utility**: Direct access to specifications and codebase for spec-code alignment

**Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    }
  }
}
```

**Use Cases**:
- Read specifications from `specs/` before coding
- Validate implementation against contracts
- Update documentation in sync with code
- Maintain traceability

**Prime Directive**: NEVER code without reading relevant spec first

---

#### 3. **github/git** - Agentic GitOps
**Strategic Utility**: Enables automated branch management, PR creation, and CI/CD integration

**Configuration**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    }
  }
}
```

**Use Cases**:
- Create feature branches automatically
- Manage pull requests
- Check CI/CD status
- Enforce commit message standards

**Capabilities**:
- `git_status`, `git_diff`, `git_commit`, `git_log`
- `create_issue`, `list_pull_requests`, `get_workflow_runs`

---

#### 4. **postgres** - Real-Time State Observability
**Strategic Utility**: Direct inspection of Influencer State and Content Ledger for debugging

**Configuration**:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost:5432/chimera"]
    }
  }
}
```

**Use Cases**:
- Validate schema against `specs/technical.md`
- Debug agent state issues
- Verify financial ledger integrity
- Monitor budget tracking in real-time

**Capabilities**:
- `query`: Execute SQL queries
- `list_tables`: View database schema
- `describe_table`: Get table structure

---

### Verification Loop: Spec-Code-Verify Cycle

Every developer action follows this mandatory workflow:

```
1. SPEC
   ↓ (filesystem-mcp)
   Read relevant specs/ documentation
   
2. THINK
   ↓ (sequential-thinking)
   Plan architecture and edge cases
   
3. CODE
   ↓ (filesystem-mcp)
   Implement with spec alignment
   
4. VERIFY
   ↓ (git-mcp + postgres-mcp)
   Run tests, validate state, commit
   
5. INTEGRATE
   ↓ (github-mcp)
   Create PR, check CI status
```

---

### MCP Server Priority Matrix

| Server | Strategic Role | Priority | Status | Use Frequency |
|--------|----------------|----------|--------|---------------|
| sequential-thinking | Architecture Planning | Critical | Active | Before major changes |
| filesystem | Spec-Driven Development | Critical | Active | Continuous |
| git/github | Agentic GitOps | Critical | Active | Daily |
| postgres | State Observability | High | Active | Debug/Validation |

---

### Tooling Governance

**Centralized Configuration**: All MCP servers configured via `mcp-config.json` to ensure environment parity across the engineering swarm.

**Configuration File**: `.cursor/mcp.json`
```json
{
  "mcpServers": {
    "sequential-thinking": { ... },
    "filesystem": { ... },
    "github": { ... },
    "git": { ... },
    "postgres": { ... }
  }
}
```

**Enforcement**:
- Version controlled in repository
- Validated in CI/CD pipeline
- Required for all developers
- Documented in onboarding

---

## Part B: Agent Skills (Runtime Capabilities)

### Skills Architecture

**Definition**: A "Skill" is a self-contained capability package with defined Input/Output contracts that agents can invoke at runtime.

**Structure**:
```
skills/
├── README.md                    # Skills catalog
├── skill_trend_analysis/        # Skill 1
│   ├── __init__.py
│   ├── contract.py              # I/O schemas
│   └── README.md                # Documentation
├── skill_video_synthesis/       # Skill 2
│   ├── __init__.py
│   ├── contract.py
│   └── README.md
└── skill_financial_approval/    # Skill 3
    ├── __init__.py
    ├── contract.py
    └── README.md
```

---

### Critical Skills Catalog

#### Skill 1: Trend Analysis
**Agent**: Scout  
**Purpose**: Analyze social media trends from multiple platforms

**Input Contract**:
```python
class TrendAnalysisInput(BaseModel):
    keywords: list[str]
    platforms: list[Literal["twitter", "tiktok", "google_trends"]]
    timeframe: str  # ISO8601 duration
    min_velocity: float = 0.5
```

**Output Contract**:
```python
class TrendAnalysisOutput(BaseModel):
    trends: list[TrendReport]
    execution_time_ms: int
    
class TrendReport(BaseModel):
    trend_id: str
    topic: str
    volume: int
    sentiment_score: float  # -1.0 to 1.0
    rising_velocity: float
    platforms: list[str]
    metadata: dict
```

**Performance**: <2000ms (P95)

---

#### Skill 2: Video Synthesis
**Agent**: Artist  
**Purpose**: Generate video content from scripts and visual prompts

**Input Contract**:
```python
class VideoSynthesisInput(BaseModel):
    brief_id: str
    script: str
    visual_prompts: list[str]
    duration_seconds: int
    resolution: Literal["720p", "1080p", "4k"] = "1080p"
    tools: dict[str, str]  # {"video": "runway-gen2", "audio": "elevenlabs"}
```

**Output Contract**:
```python
class VideoSynthesisOutput(BaseModel):
    asset_id: str
    video_url: str
    thumbnail_url: str
    duration_seconds: int
    file_size_bytes: int
    production_cost: Decimal
    quality_score: float  # 0.0 to 1.0
```

**Performance**: <120000ms (120s) for completion

---

#### Skill 3: Financial Approval
**Agent**: CFO  
**Purpose**: Approve or reject resource requests based on budget and ROI

**Input Contract**:
```python
class FinancialApprovalInput(BaseModel):
    request_id: str
    agent_id: str
    request_type: Literal["api_call", "compute", "storage", "blockchain"]
    request_cost: Decimal
    projected_roi: float
    justification: str
```

**Output Contract**:
```python
class FinancialApprovalOutput(BaseModel):
    request_id: str
    approved: bool
    reason: str
    risk_score: float  # 0.0 to 1.0
    approval_signature: str
    budget_remaining: dict[str, Decimal]  # {"daily": 485.0, "weekly": 2340.0}
    conditions: list[str]
```

**Performance**: <300ms (P95)

---

### Additional Skills (Planned)

#### Skill 4: Content Strategy
**Agent**: Director  
**Purpose**: Convert trends into content briefs

**Status**: Planned  
**Priority**: High

---

#### Skill 5: Safety Validation
**Agent**: Judge  
**Purpose**: Validate content against safety guidelines

**Status**: Planned  
**Priority**: Critical

---

#### Skill 6: Platform Publishing
**Agent**: Publisher  
**Purpose**: Publish content to social media platforms

**Status**: Planned  
**Priority**: Medium

---

## Skills Development Guidelines

### 1. Contract-First Design
Always define Input/Output contracts before implementation:
```python
# skills/skill_name/contract.py
from pydantic import BaseModel

class SkillInput(BaseModel):
    """Input schema with validation."""
    pass

class SkillOutput(BaseModel):
    """Output schema with validation."""
    pass
```

### 2. Error Handling
All skills must handle errors gracefully:
```python
class SkillError(Exception):
    """Base exception for skill errors."""
    pass

class SkillTimeoutError(SkillError):
    """Raised when skill execution exceeds timeout."""
    pass

class SkillValidationError(SkillError):
    """Raised when input validation fails."""
    pass
```

### 3. Performance Monitoring
Track execution metrics:
```python
class SkillMetrics(BaseModel):
    execution_time_ms: int
    success: bool
    error_message: Optional[str]
    cost: Decimal
```

### 4. Testing Requirements
- Unit tests for contract validation
- Integration tests with mocked external services
- Performance tests against SLA targets
- Minimum 80% code coverage

---

## Integration with MCP

### Runtime MCP Tools (Agent Skills)

Agents use MCP tools at runtime for external integrations:

#### Image Generation
- **Tool**: DALL-E 3, Midjourney, Stable Diffusion
- **MCP Server**: Custom image-generation-mcp
- **Used By**: Artist Agent

#### Video Generation
- **Tool**: Runway Gen-2, Pika
- **MCP Server**: Custom video-generation-mcp
- **Used By**: Artist Agent

#### Audio Synthesis
- **Tool**: ElevenLabs, OpenAI TTS
- **MCP Server**: Custom audio-synthesis-mcp
- **Used By**: Artist Agent

#### Social Media APIs
- **Tool**: Twitter API, TikTok API
- **MCP Server**: Custom social-media-mcp
- **Used By**: Scout Agent, Publisher Agent

---

## Deployment Strategy

### Development Environment Setup
```bash
# Install core MCP servers
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-postgres

# Verify installation
make verify-mcp

# Configure in .cursor/mcp.json (version controlled)
```

### Production Environment
```yaml
# docker-compose.yml
services:
  mcp-gateway:
    image: chimera/mcp-gateway:latest
    environment:
      - MCP_SERVERS=image-gen,video-gen,audio-gen,social-media
```

---

## Success Metrics

### Developer Tools (MCP)
- Setup time: <5 minutes
- Tool availability: >99%
- Response time: <100ms

### Agent Skills (Runtime)
- Skill execution success rate: >95%
- Performance within SLA: >99%
- Error rate: <5%
- Cost per skill execution: <$0.10

---

## Next Steps

1. ✅ Define tooling strategy (this document)
2. ⏳ Create skills directory structure
3. ⏳ Implement 3 critical skills (Trend Analysis, Video Synthesis, Financial Approval)
4. ⏳ Write comprehensive tests for each skill
5. ⏳ Configure MCP servers for development
6. ⏳ Document skill usage patterns

---

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- Project Chimera Specifications: `specs/`
