# ADR-002: Test-Driven Development (TDD) Methodology

## Status
**Accepted** - 2024

## Context
Project Chimera is an autonomous AI agent system where correctness is critical. Traditional development approaches risk building the wrong thing or introducing bugs in complex agent interactions.

## Decision
Adopt **Test-Driven Development (TDD)** as the mandatory development methodology.

## Rationale

### TDD Cycle
1. **RED**: Write failing test that defines desired behavior
2. **GREEN**: Write minimal code to pass the test
3. **REFACTOR**: Improve code while keeping tests green

### Benefits for Agent Systems
1. **Contract-First**: Tests define agent interfaces before implementation
2. **Regression Prevention**: Agents can't break existing behavior
3. **Documentation**: Tests serve as executable specifications
4. **Confidence**: High test coverage enables autonomous refactoring

## Implementation

### Test Structure
```
tests/
├── unit/                    # Component tests
│   ├── test_trend_fetcher.py
│   ├── test_skills_interface.py
│   └── test_asset_ledger.py
├── integration/             # System integration tests
└── e2e/                     # End-to-end scenarios
```

### Test Requirements
- **Coverage Target**: 80%+ for core systems
- **Test Types**: Unit, integration, E2E
- **Mocking**: Mock external MCP servers
- **CI/CD**: Tests run on every commit

### Example: Skill Contract Test
```python
def test_trend_analyzer_inherits_chimera_skill():
    """Test TrendAnalyzer inherits from ChimeraSkill."""
    from skills.trend_analyzer import TrendAnalyzer
    from skills.interface import ChimeraSkill
    
    analyzer = TrendAnalyzer()
    assert isinstance(analyzer, ChimeraSkill)
```

## Consequences

### Positive
- ✅ Fewer bugs in production
- ✅ Faster refactoring with confidence
- ✅ Clear contracts between components
- ✅ Living documentation
- ✅ Easier onboarding for new developers

### Negative
- ⚠️ Initial development slower (write tests first)
- ⚠️ Requires discipline to maintain
- ⚠️ Test maintenance overhead

## Enforcement

### Pre-commit Hooks
```yaml
- repo: local
  hooks:
    - id: pytest-check
      name: pytest-check
      entry: pytest tests/unit --maxfail=1
      language: system
      pass_filenames: false
```

### CI/CD Pipeline
```yaml
test:
  script:
    - pytest tests/ --cov=src --cov-report=xml
    - coverage report --fail-under=80
```

### Code Review Checklist
- [ ] Tests written before implementation
- [ ] All tests passing
- [ ] Coverage maintained or improved
- [ ] No skipped tests without justification

## Alternatives Considered

### 1. Behavior-Driven Development (BDD)
- **Pros**: Business-readable tests
- **Cons**: Overhead for technical components
- **Rejected**: TDD sufficient for agent systems

### 2. Traditional Testing (After Implementation)
- **Pros**: Faster initial development
- **Cons**: Tests often skipped, lower quality
- **Rejected**: Too risky for autonomous agents

### 3. Property-Based Testing
- **Pros**: Finds edge cases
- **Cons**: Complex to write
- **Decision**: Use as supplement, not replacement

## Metrics

### Test Health
- Test execution time < 5 minutes
- Flaky test rate < 1%
- Coverage trend (should increase)
- Test-to-code ratio: ~1:1

### Quality Indicators
- Bugs found in production (should decrease)
- Time to fix bugs (should decrease)
- Refactoring confidence (should increase)

## Training

### Developer Onboarding
1. TDD workshop (2 hours)
2. Pair programming with TDD expert
3. Code review feedback on test quality

### Resources
- `TDD_STATUS.md` - Current TDD state
- `tests/README.md` - Testing guide
- Internal TDD best practices wiki

## References
- Kent Beck - "Test-Driven Development by Example"
- Martin Fowler - "Refactoring"
- `specs/traceability.md` - Test-to-requirement mapping

---

**Author:** Engineering Team
**Reviewers:** Architecture, QA
**Date:** 2024
