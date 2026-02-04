# Project Chimera Makefile
# Standardized commands for development workflow

.PHONY: help setup test lint format clean docker-build docker-test spec-check

# Default target
help:
	@echo "🏗️  Project Chimera - Autonomous Influencer Factory"
	@echo ""
	@echo "Available commands:"
	@echo "  setup        - Install dependencies and set up environment"
	@echo "  test         - Run all tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  clean        - Clean up temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-test  - Run tests in Docker container"
	@echo "  spec-check   - Verify code alignment with specifications"

# Environment setup
setup:
	@echo "📦 Setting up Project Chimera environment..."
	uv sync --dev
	uv run pre-commit install
	@echo "✅ Setup complete!"

# Testing
test:
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v --cov=chimera --cov-report=html --cov-report=term

test-unit:
	@echo "🔬 Running unit tests..."
	uv run pytest tests/ -m "unit" -v

test-integration:
	@echo "🔗 Running integration tests..."
	uv run pytest tests/ -m "integration" -v

# Code quality
lint:
	@echo "🔍 Running linting checks..."
	uv run ruff check .
	uv run mypy chimera/
	uv run black --check .
	uv run isort --check-only .

format:
	@echo "✨ Formatting code..."
	uv run black .
	uv run isort .
	uv run ruff --fix .

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

# Docker operations
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t project-chimera:latest .

docker-test:
	@echo "🐳 Running tests in Docker..."
	docker run --rm -v $(PWD):/app project-chimera:latest make test

# Specification compliance
spec-check:
	@echo "📋 Checking specification compliance..."
	@if [ ! -d "specs/" ]; then \
		echo "❌ specs/ directory not found"; \
		exit 1; \
	fi
	@if [ ! -f "specs/_meta.md" ]; then \
		echo "❌ specs/_meta.md not found"; \
		exit 1; \
	fi
	@if [ ! -f "specs/functional.md" ]; then \
		echo "❌ specs/functional.md not found"; \
		exit 1; \
	fi
	@if [ ! -f "specs/technical.md" ]; then \
		echo "❌ specs/technical.md not found"; \
		exit 1; \
	fi
	@echo "✅ All required specifications found"
	@echo "🔍 Validating spec structure..."
	uv run python scripts/validate_specs.py

# Development server
dev:
	@echo "🚀 Starting development server..."
	uv run uvicorn chimera.main:app --reload --host 0.0.0.0 --port 8000

# Database operations
db-upgrade:
	@echo "📊 Running database migrations..."
	uv run alembic upgrade head

db-downgrade:
	@echo "📊 Rolling back database migrations..."
	uv run alembic downgrade -1

db-reset:
	@echo "📊 Resetting database..."
	uv run alembic downgrade base
	uv run alembic upgrade head

# MCP operations
mcp-check:
	@echo "🔌 Checking MCP Sense connection..."
	@if [ -z "$$MCP_SENSE_TOKEN" ]; then \
		echo "❌ MCP_SENSE_TOKEN not set in environment"; \
		exit 1; \
	fi
	@echo "✅ MCP Sense token configured"

# CI/CD helpers
ci-test: lint test
	@echo "✅ All CI checks passed"

# Release preparation
release-check: spec-check ci-test
	@echo "🚀 Release checks complete"