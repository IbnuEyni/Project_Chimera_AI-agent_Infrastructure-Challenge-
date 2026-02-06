# 🧠 Project Chimera - AI Agent Rules

## 1. 🌍 Project Context

**This is Project Chimera, an autonomous AI influencer system.**

You are the Lead Engineer for **Project Chimera**, an autonomous AI influencer swarm system.

**Goal**: Build a hierarchical swarm of agents (Python 3.11+) that manages social media influence, content generation, and economic operations.

**Architecture**:

- **Orchestrator**: High-level mission control (global coordination)
- **Manager**: Task decomposition and routing (10-100 managers)
- **Worker**: Specialized execution agents (10,000+ workers)
  - Scout: Trend detection from social media
  - Director: Content strategy and briefs
  - Artist: Media production (video, image, audio)
  - CFO: Financial governance and approval

**Stack**: Python 3.11+, Docker, PostgreSQL, Redis, Celery, MCP (Model Context Protocol)

**Key Metrics**:

- 10,000+ concurrent agents with <2s response time
- Target: >90% autonomy, >2% engagement, <$0.05 per asset
- Zero-trust security with SafetyGateway
- Economic sovereignty with CFO approval for all transactions

---

## 2. 🛑 The Prime Directive

**NEVER generate implementation code without first reading the relevant documentation in the `specs/` directory.**

Before writing ANY code:

1. Read the relevant specification file in `specs/`
2. Verify the API contract (input/output schemas)
3. Check database schema if data persistence is involved
4. Confirm constraints and acceptance criteria

**If I ask for a database model**: You MUST read `specs/technical.md` first.
**If I ask for agent logic**: You MUST read `specs/functional.md` first.
**If a spec is missing or ambiguous**: Ask me to define it before you write code.

**Specification Files**:

- `specs/_meta.md`: Vision, constraints, KPIs, architecture principles
- `specs/functional.md`: User stories, workflows, acceptance criteria
- `specs/technical.md`: Database schema, API contracts, ERD, performance specs
- `specs/openclaw_integration.md`: OpenClaw DHT integration (optional)

**If specifications are unclear or missing**: Ask for clarification before proceeding.

---

## 3. 📝 Traceability & Workflow

**Before writing a single line of code, you must output a PLAN Block:**

```markdown
**PLAN:**

1. **Analyze:** [Reference specific file in specs/...]
2. **Design:** [Briefly describe the classes/functions you will create]
3. **Safety:** [How does this handle errors or security (e.g., Prompt Injection)?]
4. **Test:** [What tests will verify this works?]
```

---

## 4. 🛡️ Coding Standards

**Language**: Python 3.11+

**Typing**: Strict Type Hints are MANDATORY

- Use `typing.Annotated`, `pydantic.BaseModel`, and `typing.Optional` explicitly
- Type hints on ALL functions

```python
# ✅ CORRECT
def analyze(self, keywords: list[str], timeframe: str) -> TrendReport:
    pass

# ❌ WRONG
def analyze(self, keywords, timeframe):
    pass
```

**Async**: The system is high-concurrency

- Use `async/await` for ALL I/O bound operations (DB, API calls)

**Docstrings**: Use Google-style docstrings (MANDATORY for public methods)

**Error Handling**: No bare `try/except`

- Catch specific errors and log them using the project's standard logger

```python
def analyze(self, keywords: list[str], timeframe: str) -> TrendReport:
    """
    Analyze social media trends for given keywords.

    Args:
        keywords: List of search terms
        timeframe: ISO8601 duration (e.g., "24h", "7d")

    Returns:
        TrendReport with topics, volume, sentiment scores

    Raises:
        ValueError: If timeframe format invalid
    """
    pass
```

### Error Handling

```python
# ✅ CORRECT - Specific exceptions
if not keywords:
    raise ValueError("Keywords cannot be empty")

# ❌ WRONG - Bare except
try:
    result = api_call()
except:
    pass
```

### Validation Against Specs

```python
# Always validate against specs/technical.md schemas
def create_brief(self, trend_id: str) -> ContentBrief:
    brief = {
        "brief_id": str(uuid.uuid4()),
        "trend_id": trend_id,
        "format": "video",  # Must be: video | image | thread | carousel
        "script": script,
        "visual_prompts": prompts,
        "estimated_cost": cost,
        "projected_engagement": engagement
    }
    # Validate all required fields present
    assert all(k in brief for k in ["brief_id", "trend_id", "format"])
    return brief
```

---

## 5. 📂 Project Structure Map

```
specs/              → The source of truth (ALWAYS check first)
src/chimera/agents/ → Core agent logic (Scout, Director, Artist, CFO)
src/chimera/core/   → Swarm coordination (Orchestrator, Manager)
src/chimera/security/ → Zero-trust security (SafetyGateway)
src/chimera/commerce/ → Financial logic (CFO approval, budget)
src/chimera/mcp/    → MCP integration layer
tests/              → Pytest suite (mirrors src structure)
```

## 6. ⚠️ Critical Constraints

**Zero Trust**: All external inputs (prompts, API responses) must be validated through SecurityGateway

**Finance Safety**:

- No private keys in code
- All financial logic requires CFO_Agent approval interface
- Budget caps enforced at database level

**Dependencies**: Use `uv` for package management

**Performance**: <2s response time (P95) for agent operations

---

## Architecture Patterns

```python
# Orchestrator assigns to Manager, Manager assigns to Workers
class ChimeraSwarm:
    def coordinate_task(self, task: Task) -> Result:
        # 1. Planner decomposes task
        subtasks = self.planner.decompose(task)

        # 2. Workers execute in parallel
        results = await asyncio.gather(*[
            self.worker_pool.execute(st) for st in subtasks
        ])

        # 3. Judge validates outputs
        validated = self.judge.validate(results)

        return validated
```

### Financial Safety (CFO Approval)

```python
# NO worker agent holds private keys
class WorkerAgent:
    async def request_resource(self, cost: Decimal) -> bool:
        # Request approval from CFO
        approval = await self.cfo_agent.approve(
            request_cost=cost,
            projected_roi=self.estimate_roi(),
            justification="API credits for trend analysis"
        )

        if not approval.approved:
            raise BudgetExceededError(approval.reason)

        return True
```

### Zero-Trust Security

```python
# All inputs pass through SecurityGateway
class SecurityGateway:
    def validate_request(self, user_input: str) -> ValidationResult:
        # 1. Prompt injection check
        if self.prompt_filter.scan(user_input).threat_level > 0.7:
            return ValidationResult(approved=False, reason="Prompt injection detected")

        # 2. Permission validation
        # 3. Rate limiting
        # 4. Audit logging

        return ValidationResult(approved=True)
```

---

## Testing Requirements

### Test-Driven Development (TDD)

Write tests BEFORE implementation:

```python
# tests/test_scout.py
def test_trend_analysis_returns_valid_report():
    """Test TrendScout returns TrendReport matching spec."""
    scout = TrendScout()

    report = scout.analyze(
        keywords=["AI", "Crypto"],
        timeframe="24h"
    )

    # Validate against specs/technical.md
    assert "trend_id" in report
    assert "topic" in report
    assert -1.0 <= report["sentiment_score"] <= 1.0
    assert len(report["platforms"]) > 0
```

### Mocking External Services

```python
# Mock MCP tools, blockchain, external APIs
@pytest.fixture
def mock_openai():
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = {"choices": [{"message": {"content": "test"}}]}
        yield mock

def test_artist_produces_asset(mock_openai):
    artist = ArtistAgent()
    asset = artist.produce(brief_id="test-123")
    assert asset.quality_score > 0.8
```

### Coverage Target

- Minimum: 80% code coverage
- Critical paths (CFO approval, SecurityGateway): 100%

---

## Database Operations

### Always Use Transactions

```python
# ✅ CORRECT
async with db.transaction():
    await db.execute("INSERT INTO ledger ...")
    await db.execute("UPDATE budget_tracking ...")

# ❌ WRONG - No transaction
await db.execute("INSERT INTO ledger ...")
await db.execute("UPDATE budget_tracking ...")
```

### Validate Against Schema

```python
# Check specs/technical.md for table definitions
def create_content(self, trend_id: str) -> UUID:
    # content_pipeline table requires: trend_source_id, stage, format
    content_id = uuid.uuid4()
    await db.execute(
        """
        INSERT INTO content_pipeline (id, trend_source_id, stage, format)
        VALUES ($1, $2, $3, $4)
        """,
        content_id, trend_id, "draft", "video"
    )
    return content_id
```

---

## Performance Requirements

### Response Time Targets (from specs/\_meta.md)

- Agent decision loop: <2000ms (P95)
- Trend analysis: <2000ms
- Brief generation: <1000ms
- CFO approval: <300ms
- Database queries: <50ms

### Optimization Strategies

```python
# Use async/await for I/O operations
async def analyze_trends(self, keywords: list[str]) -> list[Trend]:
    # Parallel API calls
    results = await asyncio.gather(
        self.twitter_api.search(keywords),
        self.tiktok_api.search(keywords),
        self.google_trends.search(keywords)
    )
    return self.aggregate(results)
```

---

## Security Rules

### Never Hardcode Secrets

```python
# ✅ CORRECT
api_key = os.getenv("OPENAI_API_KEY")

# ❌ WRONG
api_key = "sk-1234567890abcdef"
```

### Validate All Inputs

```python
# ✅ CORRECT
def process_user_input(self, text: str) -> str:
    # Check specs/_meta.md: All inputs through SafetyGateway
    validation = self.security_gateway.validate(text)
    if not validation.approved:
        raise SecurityError(validation.reason)
    return validation.sanitized_input
```

### Audit Logging

```python
# Log all financial transactions, security events
await audit_log.record(
    event_type="transaction_approved",
    agent_id=agent_id,
    details={"amount": amount, "cfo_signature": signature}
)
```

---

## Forbidden Patterns

### ❌ DO NOT bypass CFO approval

```python
# WRONG - Direct transaction without approval
wallet.send_transaction(amount=100)

# CORRECT - Request CFO approval first
approval = await cfo_agent.approve(request_cost=100, ...)
if approval.approved:
    wallet.send_transaction(amount=100, signature=approval.signature)
```

### ❌ DO NOT skip input validation

```python
# WRONG - Direct use of user input
result = agent.execute(user_input)

# CORRECT - Validate through SecurityGateway
validated = security_gateway.validate(user_input)
result = agent.execute(validated.sanitized_input)
```

### ❌ DO NOT ignore spec constraints

```python
# WRONG - Violates specs/technical.md (max video duration: 600s)
video = generate_video(duration=900)

# CORRECT - Enforce spec constraints
if duration > 600:
    raise ValueError("Video duration exceeds 600s limit")
video = generate_video(duration=duration)
```

---

## Git Commit Standards

### Conventional Commits

```bash
# Format: <type>(<scope>): <description>

feat(scout): Implement trend analysis with sentiment scoring
fix(cfo): Correct budget calculation for weekly limits
docs(specs): Update API contracts for video metadata
test(artist): Add unit tests for asset production
refactor(security): Optimize prompt injection detection
```

### Commit Message Body

```
feat(scout): Implement trend analysis with sentiment scoring

- Implements specs/functional.md Story 1: Trend Acquisition
- Adds semantic deduplication (>90% noise reduction)
- Calculates sentiment scores (-1.0 to 1.0)
- Returns TrendReport matching specs/technical.md API contract
- Completes in <2s as per specs/_meta.md performance requirements

Tested: test_trend_analysis_returns_valid_report
```

---

## Development Workflow

### Before Starting

1. Read relevant spec in `specs/`
2. Check existing implementation in `src/chimera/`
3. Review related tests in `tests/`
4. Verify database schema if needed

### During Implementation

1. Write failing test first (TDD)
2. Implement minimal code to pass test
3. Validate against spec
4. Refactor if needed
5. Run full test suite

### Before Committing

1. Run `make quality` (format, lint, type-check, security)
2. Run `make test` (all tests pass)
3. Run `make spec-check` (verify spec alignment)
4. Write descriptive commit message

---

## Questions to Ask Before Coding

1. **What spec section covers this?** → Check `specs/`
2. **What's the API contract?** → Check `specs/technical.md`
3. **What are the constraints?** → Check `specs/_meta.md`
4. **What's the acceptance criteria?** → Check `specs/functional.md`
5. **Are there security implications?** → Check zero-trust requirements
6. **Does this need CFO approval?** → Check financial safety rules
7. **What's the performance target?** → Check response time requirements
8. **How do I test this?** → Write test first (TDD)

---

## Success Checklist

Before marking any task complete:

- [ ] Spec reviewed and understood
- [ ] Plan explained before coding
- [ ] Type hints on all functions
- [ ] Docstrings on public methods
- [ ] Tests written and passing
- [ ] Spec constraints validated
- [ ] Security checks applied
- [ ] Performance targets met
- [ ] Code quality checks passed (`make quality`)
- [ ] Spec alignment verified (`make spec-check`)
- [ ] Commit message follows conventions

---

## Remember

**Chimera is not just code—it's a specification-driven system.**

Every line of code must trace back to a requirement in `specs/`. When in doubt, check the specs. When specs are unclear, ask for clarification. Never assume—always verify.

**The goal**: >90% autonomy, >2% engagement, <$0.05 per asset, with enterprise-grade security and financial safety.
