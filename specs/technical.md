# 🔧 Project Chimera - Technical Specification

**Version**: 1.0.0  
**Last Updated**: 2026-02-06

---

## 1. Database Schema (PostgreSQL)

### Table: `agents`

```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role VARCHAR(50) NOT NULL CHECK (role IN ('scout', 'director', 'artist', 'cfo', 'planner', 'worker', 'judge')),
    status VARCHAR(20) NOT NULL DEFAULT 'idle' CHECK (status IN ('idle', 'busy', 'offline', 'error')),
    config JSONB NOT NULL DEFAULT '{}',
    capabilities JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_heartbeat TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_agents_role ON agents(role);
CREATE INDEX idx_agents_status ON agents(status);
```

**Description**: Stores agent metadata and operational state. `config` holds dynamic prompt configuration.

---

### Table: `trends`

```sql
CREATE TABLE trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic VARCHAR(255) NOT NULL,
    volume INTEGER NOT NULL CHECK (volume >= 0),
    sentiment_score DECIMAL(3,2) NOT NULL CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0),
    rising_velocity DECIMAL(5,2) NOT NULL,
    platforms JSONB NOT NULL DEFAULT '[]',
    metadata JSONB NOT NULL DEFAULT '{}',
    scout_agent_id UUID REFERENCES agents(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_trends_topic ON trends(topic);
CREATE INDEX idx_trends_created ON trends(created_at DESC);
CREATE INDEX idx_trends_velocity ON trends(rising_velocity DESC);
```

**Description**: Stores trend analysis results from TrendScout agents.

---

### Table: `content_pipeline`

```sql
CREATE TABLE content_pipeline (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_source_id UUID NOT NULL REFERENCES trends(id) ON DELETE CASCADE,
    stage VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (stage IN ('draft', 'generating', 'review', 'published', 'failed')),
    format VARCHAR(20) CHECK (format IN ('video', 'image', 'thread', 'carousel')),
    script TEXT,
    visual_prompts JSONB DEFAULT '[]',
    media_url TEXT,
    production_cost DECIMAL(10,2) DEFAULT 0.00,
    quality_score DECIMAL(3,2) CHECK (quality_score >= 0.0 AND quality_score <= 1.0),
    metadata JSONB NOT NULL DEFAULT '{}',
    director_agent_id UUID REFERENCES agents(id),
    artist_agent_id UUID REFERENCES agents(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_content_stage ON content_pipeline(stage);
CREATE INDEX idx_content_trend ON content_pipeline(trend_source_id);
CREATE INDEX idx_content_created ON content_pipeline(created_at DESC);
```

**Description**: Tracks content from ideation to publication. `media_url` points to S3/local storage.

---

### Table: `video_metadata`

```sql
CREATE TABLE video_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL REFERENCES content_pipeline(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_seconds INTEGER NOT NULL CHECK (duration_seconds > 0),
    resolution VARCHAR(20) CHECK (resolution IN ('720p', '1080p', '4k')),
    fps INTEGER CHECK (fps IN (24, 30, 60)),
    codec VARCHAR(50),
    file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes > 0),
    thumbnail_url TEXT,
    video_url TEXT NOT NULL,
    platform_ids JSONB DEFAULT '{}',
    engagement_metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_video_content ON video_metadata(content_id);
CREATE INDEX idx_video_duration ON video_metadata(duration_seconds);
CREATE INDEX idx_video_created ON video_metadata(created_at DESC);
```

**Description**: Stores video-specific metadata. `platform_ids` contains IDs from YouTube, TikTok, etc. `engagement_metrics` tracks views, likes, shares.

---

### Table: `ledger`

```sql
CREATE TABLE ledger (
    tx_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    request_type VARCHAR(50) NOT NULL CHECK (request_type IN ('api_call', 'compute', 'storage', 'blockchain')),
    amount DECIMAL(18,2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    projected_roi DECIMAL(10,2),
    risk_score DECIMAL(3,2) CHECK (risk_score >= 0.0 AND risk_score <= 1.0),
    approved BOOLEAN NOT NULL DEFAULT FALSE,
    approval_signature TEXT NOT NULL,
    cfo_agent_id UUID REFERENCES agents(id),
    justification TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    approved_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_ledger_agent ON ledger(agent_id);
CREATE INDEX idx_ledger_approved ON ledger(approved);
CREATE INDEX idx_ledger_created ON ledger(created_at DESC);
CREATE INDEX idx_ledger_type ON ledger(request_type);
```

**Description**: Immutable financial ledger. `approval_signature` contains CFO cryptographic signature.

---

### Table: `budget_tracking`

```sql
CREATE TABLE budget_tracking (
    id SERIAL PRIMARY KEY,
    period VARCHAR(20) NOT NULL CHECK (period IN ('daily', 'weekly', 'monthly')),
    category VARCHAR(50) NOT NULL CHECK (category IN ('api_call', 'compute', 'storage', 'total')),
    limit_amount DECIMAL(10,2) NOT NULL CHECK (limit_amount > 0),
    spent_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (spent_amount >= 0),
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT check_spent_within_limit CHECK (spent_amount <= limit_amount)
);

CREATE UNIQUE INDEX idx_budget_period_category ON budget_tracking(period, category, period_start);
```

**Description**: Enforces budget caps at database level. Constraint prevents over-spending.

---

---

## 2. Entity Relationship Diagram (ERD)

```
┌─────────────┐
│   agents    │
│             │
│ - id (PK)   │
│ - role      │
│ - status    │
│ - config    │
└──────┬──────┘
       │
       │ 1:N (scout_agent_id)
       ▼
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   trends    │────────▶│content_pipeline  │────────▶│video_metadata   │
│             │  1:N    │                  │  1:1    │                 │
│ - id (PK)   │         │ - id (PK)        │         │ - id (PK)       │
│ - topic     │         │ - trend_id (FK)  │         │ - content_id(FK)│
│ - volume    │         │ - stage          │         │ - title         │
│ - sentiment │         │ - format         │         │ - duration      │
│ - velocity  │         │ - script         │         │ - resolution    │
└─────────────┘         │ - media_url      │         │ - video_url     │
                        │ - quality_score  │         │ - platform_ids  │
                        └────────┬─────────┘         │ - engagement    │
                                 │                   └─────────────────┘
                                 │ N:1 (director_agent_id)
                                 │ N:1 (artist_agent_id)
                                 ▼
                        ┌─────────────┐
                        │   agents    │
                        └─────────────┘

┌─────────────┐         ┌──────────────────┐
│   agents    │────────▶│     ledger       │
│             │  1:N    │                  │
│ - id (PK)   │         │ - tx_id (PK)     │
└─────────────┘         │ - agent_id (FK)  │
       │                │ - amount         │
       │ 1:1 (cfo)      │ - approved       │
       └───────────────▶│ - signature      │
                        │ - cfo_agent_id   │
                        └──────────────────┘

┌──────────────────┐
│budget_tracking   │
│                  │
│ - id (PK)        │
│ - period         │
│ - category       │
│ - limit_amount   │
│ - spent_amount   │
│ - period_start   │
│ - period_end     │
└──────────────────┘
```

**Key Relationships**:

- `agents` → `trends`: Scout agents create trends (1:N)
- `trends` → `content_pipeline`: Each trend generates content (1:N)
- `content_pipeline` → `video_metadata`: Video content has detailed metadata (1:1)
- `agents` → `content_pipeline`: Director and Artist agents work on content (N:1 each)
- `agents` → `ledger`: Agents make financial requests (1:N)
- `agents` (CFO) → `ledger`: CFO approves transactions (1:N)

---

## 3. API Contracts (Inter-Agent Protocol)

### Trend Analysis Interface

**Endpoint**: `internal.agent.scout.analyze`

**Input**:

```json
{
  "keywords": ["AI", "Crypto"],
  "timeframe": "24h",
  "min_velocity": 0.5,
  "platforms": ["twitter", "tiktok", "google_trends"]
}
```

**Output**:

```json
{
  "trends": [
    {
      "trend_id": "uuid",
      "topic": "string",
      "volume": 15000,
      "sentiment_score": 0.75,
      "rising_velocity": 2.3,
      "platforms": ["twitter", "tiktok"],
      "metadata": {
        "top_posts": ["url1", "url2"],
        "influencers": ["@user1", "@user2"]
      }
    }
  ],
  "execution_time_ms": 1850
}
```

**Constraints**:

- `timeframe`: ISO8601 duration (e.g., "24h", "7d")
- `min_velocity`: Minimum rising rate (0.0-10.0)
- Response time: <2s
- Returns 1-20 trends

---

### Content Brief Generation

**Endpoint**: `internal.agent.director.create_brief`

**Input**:

```json
{
  "trend_id": "uuid",
  "personality_profile": {
    "name": "Sarcastic Tech Reviewer",
    "tone": "humorous",
    "target_audience": "tech-savvy millennials",
    "brand_guidelines": {
      "voice": "casual",
      "avoid": ["jargon", "corporate-speak"]
    }
  }
}
```

**Output**:

```json
{
  "brief_id": "uuid",
  "trend_id": "uuid",
  "format": "video",
  "script": "string (full script)",
  "visual_prompts": [
    "Futuristic tech lab with neon lights",
    "Close-up of AI chip glowing"
  ],
  "tone_guidelines": "Sarcastic but informative",
  "target_platforms": ["youtube", "tiktok"],
  "estimated_cost": 12.5,
  "projected_engagement": 0.035,
  "execution_time_ms": 850
}
```

**Constraints**:

- Response time: <1s
- Cost estimate accuracy: ±10%
- Script length: 100-500 words

---

### Asset Production

**Endpoint**: `internal.agent.artist.produce`

**Input**:

```json
{
  "brief_id": "uuid",
  "tools": {
    "image": "dall-e-3",
    "video": "runway-gen2",
    "audio": "elevenlabs"
  },
  "quality_preset": "high"
}
```

**Output**:

```json
{
  "asset_id": "uuid",
  "brief_id": "uuid",
  "format": "video",
  "files": [
    {
      "type": "video",
      "url": "s3://bucket/assets/video_123.mp4",
      "size_bytes": 15728640,
      "duration_seconds": 30
    },
    {
      "type": "thumbnail",
      "url": "s3://bucket/assets/thumb_123.jpg",
      "size_bytes": 204800
    }
  ],
  "production_cost": 11.8,
  "quality_score": 0.92,
  "execution_time_ms": 45000
}
```

**Constraints**:

- Image generation: <30s
- Video generation: <120s
- Quality score: >0.8
- Max file size: 100MB

---

### Financial Approval

**Endpoint**: `internal.agent.cfo.approve`

**Input**:

```json
{
  "request_id": "uuid",
  "agent_id": "uuid",
  "request_type": "api_call",
  "request_cost": 15.0,
  "projected_roi": 2.5,
  "justification": "Generate viral video for trending topic"
}
```

**Output**:

```json
{
  "request_id": "uuid",
  "approved": true,
  "reason": "Within budget, ROI exceeds hurdle rate (1.5)",
  "risk_score": 0.25,
  "approval_signature": "0x1234...abcd",
  "budget_remaining": {
    "daily": 485.0,
    "weekly": 2340.0,
    "monthly": 8920.0
  },
  "conditions": [],
  "execution_time_ms": 120
}
```

**Rules**:

1. If `request_cost` > `daily_remaining_budget` → REJECT
2. If `projected_roi` < 1.5 → REJECT
3. If `risk_score` > 0.7 → ESCALATE to human
4. Log to immutable ledger

**Constraints**:

- Response time: <300ms
- 100% logging to ledger
- Signature verification required

---

---

## 4. Redis Schema (Agent State)

### Key: `agent:{agent_id}:state`

```json
{
  "agent_id": "uuid",
  "role": "scout",
  "status": "busy",
  "current_task": "uuid",
  "last_heartbeat": "2026-02-06T12:00:00Z",
  "metrics": {
    "tasks_completed": 1247,
    "avg_execution_time_ms": 1850,
    "error_count": 3
  }
}
```

**TTL**: 300 seconds

---

### Key: `budget:{period}:{category}`

```json
{
  "period": "daily",
  "category": "api_call",
  "limit": 1000.0,
  "spent": 515.0,
  "remaining": 485.0,
  "last_updated": "2026-02-06T12:00:00Z"
}
```

**TTL**: Based on period (86400s for daily)

---

### Key: `task_queue:{priority}`

```
LPUSH task_queue:high '{"task_id": "uuid", "agent_role": "scout"}'
```

**Description**: Priority queues for task distribution

---

## 5. Data Flow Diagrams

### Content Pipeline Flow

```
1. TrendScout Agent
   ↓ (writes to)
2. trends table
   ↓ (read by)
3. Director Agent
   ↓ (writes to)
4. content_pipeline (stage: draft)
   ↓ (read by)
5. Artist Agent → MCP Tools (DALL-E, Runway, ElevenLabs)
   ↓ (updates)
6. content_pipeline (stage: generating)
   ↓ (writes to)
7. video_metadata (title, duration, resolution, video_url)
   ↓ (read by)
8. SafetyGateway
   ↓ (updates)
9. content_pipeline (stage: published)
   ↓ (publishes to)
10. YouTube/TikTok (platform_ids updated)
```

### Financial Approval Flow

```
1. Worker Agent (requests resource)
   ↓
2. CFO Agent (evaluates)
   ├─ Check budget_tracking (spent vs limit)
   ├─ Calculate risk_score
   └─ Evaluate projected_roi
   ↓
3. Decision (approve/reject)
   ↓
4. ledger table (immutable record)
   ├─ approval_signature (cryptographic)
   └─ cfo_agent_id
   ↓
5. budget_tracking (update spent_amount)
```

---

## 6. Performance Specifications

### Response Time Targets (P95)

- Trend analysis: <2000ms (completion)
- Brief generation: <1000ms (completion)
- Asset production (async): <30000ms images, <120000ms video (completion)
- CFO approval: <300ms (completion)
- Database queries: <50ms (completion)

**Note**: The <2s system latency applies to synchronous operations (task acceptance, routing, approval). Asynchronous operations like asset generation have separate completion time targets and do not block the agent decision loop.

- Trend analysis: <2000ms
- Brief generation: <1000ms
- Asset production: <30000ms (images), <120000ms (video)
- CFO approval: <300ms
- Database queries: <50ms

### Throughput Targets

- Trends/hour: 1000+
- Content pieces/day: 500+
- Transactions/second: 100+
- Concurrent agents: 10,000+

### Resource Limits

- Max trend volume: 1,000,000
- Max script length: 5000 chars
- Max video duration: 600 seconds (10 min)
- Max file size: 100MB
- Max transaction: $10,000
- Max daily budget: $1,000

---

## 7. Security Specifications

### Authentication

- JWT tokens for all inter-agent communication
- Token expiry: 1 hour
- Refresh token: 7 days
- Signature algorithm: RS256

### Authorization (RBAC)

```json
{
  "scout": ["read:trends", "write:trends"],
  "director": ["read:trends", "write:content_pipeline"],
  "artist": [
    "read:content_pipeline",
    "write:content_pipeline",
    "write:video_metadata",
    "call:mcp_tools"
  ],
  "cfo": ["read:ledger", "write:ledger", "approve:transactions"]
}
```

### Encryption

- At rest: AES-256
- In transit: TLS 1.3
- Secrets: AWS Secrets Manager / HashiCorp Vault

---

## 8. Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "BUDGET_EXCEEDED",
    "message": "Daily budget limit reached",
    "details": {
      "requested": 150.0,
      "remaining": 50.0
    },
    "timestamp": "2026-02-06T12:00:00Z",
    "request_id": "uuid"
  }
}
```

### Error Codes

- `BUDGET_EXCEEDED`: Budget limit reached
- `ROI_TOO_LOW`: Projected ROI below hurdle rate
- `INVALID_SIGNATURE`: CFO signature verification failed
- `AGENT_OFFLINE`: Target agent unavailable
- `MCP_TIMEOUT`: External tool timeout
- `QUALITY_FAILED`: Asset quality below threshold
- `VIDEO_TOO_LONG`: Duration exceeds 600 seconds

---

## 9. Monitoring & Observability

### Metrics to Track

```python
# Prometheus metrics
agent_tasks_total{role="scout", status="completed"}
agent_response_time_seconds{role="cfo", quantile="0.95"}
budget_spent_total{period="daily", category="api_call"}
content_pipeline_stage_duration_seconds{stage="generating"}
ledger_transactions_total{approved="true"}
video_production_duration_seconds{resolution="1080p"}
```

### Health Check Endpoint

```
GET /health

Response:
{
  "status": "healthy",
  "components": {
    "database": "healthy",
    "redis": "healthy",
    "mcp_layer": "healthy",
    "agents": {
      "scout": 10,
      "director": 5,
      "artist": 20,
      "cfo": 1
    }
  },
  "timestamp": "2026-02-06T12:00:00Z"
}
```

---

## 10. Deployment Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/chimera
REDIS_URL=redis://localhost:6379/0

# Budget Limits
DAILY_BUDGET_LIMIT=1000.00
WEEKLY_BUDGET_LIMIT=5000.00
MONTHLY_BUDGET_LIMIT=20000.00
MIN_ROI_HURDLE_RATE=1.5

# MCP Tools
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
RUNWAY_API_KEY=...

# Storage
S3_BUCKET=chimera-assets
S3_REGION=us-east-1

# Security
JWT_SECRET=...
CFO_PRIVATE_KEY=...
```

### Docker Compose

```yaml
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: chimera

  redis:
    image: redis:7

  app:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres@postgres:5432/chimera
      REDIS_URL: redis://redis:6379/0
```
