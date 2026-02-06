# Test Suite Documentation

**Version**: 1.0.0  
**Last Updated**: 2026-02-06  
**Status**: TDD Phase - Tests Define Contracts

---

## Overview

This test suite follows Test-Driven Development (TDD) principles. All tests are designed to **FAIL initially** - this is correct and expected behavior. The tests define the "empty slots" that implementations must fill.

---

## Test Structure

```
tests/
├── __init__.py                      # Test package initialization
├── unit/                            # Unit tests
│   ├── __init__.py
│   ├── test_trend_fetcher.py        # Trend analysis contract tests
│   └── test_skills_interface.py     # Skills interface contract tests
└── integration/                     # Integration tests (future)
    └── __init__.py
```

---

## Test Files

### 1. test_trend_fetcher.py
**Purpose**: Validates trend data structures match `specs/technical.md` API contract

**Test Classes**:
- `TestTrendAnalysisContract`: Input/Output schema validation
- `TestTrendAnalysisExecution`: Skill execution and performance
- `TestTrendDatabaseIntegration`: Database schema validation

**Key Tests**:
- ✅ Input schema matches spec (keywords, platforms, timeframe)
- ✅ Output schema matches spec (trends, execution_time_ms)
- ✅ Sentiment score bounded [-1.0, 1.0]
- ✅ Returns 1-20 trends per spec
- ✅ Performance SLA <2000ms
- ✅ Safety validation implemented
- ✅ Database schema matches spec

**Expected Status**: 9 tests, all FAILING (correct)

---

### 2. test_skills_interface.py
**Purpose**: Validates skills modules implement ChimeraSkill interface correctly

**Test Classes**:
- `TestChimeraSkillInterface`: Base class contract
- `TestTrendAnalyzerSkill`: TrendAnalyzer implementation
- `TestAssetFactorySkill`: AssetFactory implementation
- `TestCommerceManagerSkill`: CommerceManager implementation
- `TestSkillSafetyValidation`: Safety validation across skills
- `TestSkillMetrics`: Execution metrics tracking

**Key Tests**:
- ✅ ChimeraSkill is abstract base class
- ✅ Required methods: name, execute, validate_safety
- ✅ Generic types Generic[T_In, T_Out]
- ✅ All skills inherit ChimeraSkill
- ✅ All skills implement name property
- ✅ All skills have async execute() method
- ✅ Input validation with Pydantic
- ✅ Safety validation returns bool
- ✅ Metrics tracking (execution_time_ms, success, cost)

**Expected Status**: 20 tests, 16 FAILING (correct)

---

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/unit/test_trend_fetcher.py -v
pytest tests/unit/test_skills_interface.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=skills --cov-report=html
```

### Run Specific Test
```bash
pytest tests/unit/test_trend_fetcher.py::TestTrendAnalysisContract::test_trend_analysis_input_schema -v
```

---

## Current Test Status

### test_trend_fetcher.py
```
COLLECTED: 9 tests
PASSED: 1 test (test_trends_table_schema - placeholder)
FAILED: 8 tests (expected - implementations missing)

Failures:
- ModuleNotFoundError: skills.trend_analyzer.contract
- ImportError: TrendAnalyzer class not implemented
```

### test_skills_interface.py
```
COLLECTED: 20 tests
PASSED: 4 tests (ChimeraSkill interface exists)
FAILED: 16 tests (expected - skill implementations missing)

Failures:
- ImportError: TrendAnalyzer, AssetFactory, CommerceManager not implemented
- ModuleNotFoundError: contract modules not created
```

---

## Implementation Checklist

To make tests pass, implement the following:

### Phase 1: Contracts (Pydantic Models)
- [ ] `skills/trend_analyzer/contract.py`
  - [ ] TrendAnalysisInput
  - [ ] TrendAnalysisOutput
  - [ ] TrendReport
  
- [ ] `skills/asset_factory/contract.py`
  - [ ] VideoSynthesisInput
  - [ ] VideoSynthesisOutput
  
- [ ] `skills/commerce_manager/contract.py`
  - [ ] FinancialApprovalInput
  - [ ] FinancialApprovalOutput

### Phase 2: Skill Implementations
- [ ] `skills/trend_analyzer/__init__.py`
  - [ ] TrendAnalyzer class
  - [ ] Inherits ChimeraSkill
  - [ ] Implements execute() method
  
- [ ] `skills/asset_factory/__init__.py`
  - [ ] AssetFactory class
  - [ ] Inherits ChimeraSkill
  - [ ] Implements execute() method
  
- [ ] `skills/commerce_manager/__init__.py`
  - [ ] CommerceManager class
  - [ ] Inherits ChimeraSkill
  - [ ] Implements execute() method

### Phase 3: Database Layer
- [ ] Database connection setup
- [ ] Trends table creation
- [ ] Persistence methods

---

## TDD Workflow

1. **RED**: Tests fail (current state) ✅
2. **GREEN**: Write minimal code to pass tests
3. **REFACTOR**: Improve code while keeping tests green

---

## Success Criteria

Tests are successful when they:
1. ✅ Define clear contracts from specs
2. ✅ Fail initially (no implementation)
3. ✅ Provide clear error messages
4. ✅ Cover all critical paths
5. ✅ Match specs/technical.md exactly

---

## References

- Specifications: `../specs/technical.md`, `../specs/functional.md`
- Skills Interface: `../skills/interface.py`
- Skills Documentation: `../skills/README.md`
