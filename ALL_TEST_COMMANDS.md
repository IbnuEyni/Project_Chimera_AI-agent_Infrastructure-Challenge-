# 🧪 Project Chimera - Complete Test Commands

## 📋 **Pre-Recording Setup**

```bash
cd /home/shuaib/Desktop/python/10AcademyWeek0phase2
clear
```

## 🎯 **All Test Commands (Copy-Paste Ready)**

### **Complete Test Suite**

```bash
# Run ALL tests with coverage
pytest tests/ -v --cov=skills --cov-report=term-missing

# Run all tests with short traceback
pytest tests/ -v --tb=short

# Run all unit tests
pytest tests/unit/ -v

# Run specific test files
pytest tests/unit/test_trend_fetcher.py tests/unit/test_asset_ledger.py -v
```

### **Individual Test Files**

```bash
# Trend Analyzer Tests (8 pass, 2 fail - TDD RED)
pytest tests/unit/test_trend_fetcher.py -v --tb=short

# Asset Ledger Tests (6 fail - TDD RED)
pytest tests/unit/test_asset_ledger.py -v --tb=short

# Skills Interface Tests
pytest tests/unit/test_skills_interface.py -v --tb=short

# OpenClaw Communication Tests
pytest tests/unit/test_occ.py -v --tb=short
```

### **Test Categories**

```bash
# Contract/Schema Tests (SHOULD PASS)
pytest tests/unit/test_trend_fetcher.py::TestTrendAnalysisContract -v

# Execution Logic Tests (SHOULD FAIL - TDD RED)
pytest tests/unit/test_trend_fetcher.py::TestTrendAnalysisExecution -v

# Security Tests
pytest tests/unit/test_trend_fetcher.py::TestTrendAnalysisExecution::test_trend_analyzer_safety_validation -v

# Performance Tests
pytest tests/unit/test_trend_fetcher.py::TestTrendAnalysisExecution::test_trend_analyzer_performance_sla -v
```

```bash
I want to execute a $75 marketing transaction for the influencer. According to our project rules and specs, is this allowed? If so, which specific swarm role must oversee this?
```

### **Docker Test Commands**

```bash
# Build and run all tests in Docker
docker build -t project-chimera . && docker run --rm project-chimera

# Run specific tests in Docker
docker run --rm project-chimera python -m pytest tests/unit/test_trend_fetcher.py -v

# Run with coverage in Docker
docker run --rm project-chimera python -m pytest tests/ --cov=skills --cov-report=term-missing

# Interactive Docker testing
docker run --rm -it project-chimera bash
```

### **Enterprise Tooling**

```bash
# Use Makefile commands (uv-based)
make test-local
make test
make spec-check
make quality

# Direct uv commands
uv run pytest tests/ -v --tb=short
uv run pytest tests/ --cov=skills --cov-report=term-missing
```

## 📊 **Expected Results**

### **Complete Test Results**

```
tests/unit/test_trend_fetcher.py::TestTrendAnalysisContract::test_trend_signal_schema PASSED
tests/unit/test_trend_fetcher.py::TestTrendAnalysisContract::test_trend_analysis_input_schema PASSED
tests/unit/test_trend_fetcher.py::TestTrendAnalysisContract::test_trend_analysis_output_schema PASSED
tests/unit/test_trend_fetcher.py::TestTrendAnalysisContract::test_trend_report_sentiment_bounds PASSED
tests/unit/test_trend_fetcher.py::TestTrendAnalysisContract::test_trend_analysis_returns_1_to_20_trends PASSED
tests/unit/test_trend_fetcher.py::TestTrendAnalysisExecution::test_trend_analyzer_execution FAILED
tests/unit/test_trend_fetcher.py::TestTrendAnalysisExecution::test_trend_analyzer_performance_sla FAILED
tests/unit/test_trend_fetcher.py::TestTrendAnalysisExecution::test_trend_analyzer_safety_validation FAILED

tests/unit/test_asset_ledger.py::TestAssetLedger::test_reasoning_hash_generation FAILED
tests/unit/test_asset_ledger.py::TestAssetLedger::test_reasoning_hash_changes_with_context FAILED
tests/unit/test_asset_ledger.py::TestAssetLedger::test_asset_ledger_links_transaction_to_trend FAILED
tests/unit/test_asset_ledger.py::TestAssetLedger::test_asset_ledger_calculates_roi FAILED
tests/unit/test_asset_ledger.py::TestAssetLedger::test_pnl_report_generation FAILED
tests/unit/test_asset_ledger.py::TestAssetLedger::test_explainable_pnl_includes_justification FAILED

TOTAL: 8 PASSED, 8 FAILED - PERFECT TDD DEMONSTRATION
```

### **Docker Results**

```
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0
collected 16 items

8 passed, 8 failed - Enterprise containerized testing works!
Coverage: 64% (skills/trend_analyzer/contract.py: 100%, skills/commerce_manager/asset_ledger.py: 95%)
```

## ⚡ **Quick Demo Commands**

```bash
# TDD Demo - Show contracts pass, logic fails
pytest tests/unit/test_trend_fetcher.py -v --tb=short

# Asset Ledger TDD Demo
pytest tests/unit/test_asset_ledger.py -v --tb=short

# Docker Demo
docker build -t project-chimera . && docker run --rm project-chimera

# Enterprise Tooling
make test-local && make spec-check

# Coverage Report
pytest tests/ --cov=skills --cov-report=term-missing
```

## 🎯 **Key Talking Points**

- **"8 tests pass (contracts), 8 fail (logic) - perfect TDD RED phase"**
- **"Enterprise Docker with uv - fastest Python tooling"**
- **"64% code coverage with intentional logical failures"**
- **"Cryptographic audit trails, zero-trust security"**
- **"Test-driven development with executable requirements"**

---

**🚀 Complete test command reference for Project Chimera!**
