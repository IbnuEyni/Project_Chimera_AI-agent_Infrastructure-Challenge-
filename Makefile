.PHONY: help install install-dev setup setup-golden mcp-verify mcp-health mcp-monitor-setup test test-cov lint format type-check security clean build docs serve-docs docker-build docker-run deploy-local deploy-staging deploy-prod

# Default target
help: ## Show this help message
	@echo "Project Chimera - Development Commands"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment Setup
install: ## Install production dependencies
	uv sync --no-dev

install-dev: ## Install development dependencies
	uv sync --all-extras

setup: ## Complete development environment setup
	@echo "🚀 Setting up Project Chimera development environment..."
	uv sync --all-extras
	pre-commit install
	@echo "✅ Setup complete!"

setup-golden: ## Golden environment: tooling + MCP Sense integration
	@./scripts/setup-golden-env.sh

# MCP Sense Integration
mcp-verify: ## Verify Tenx MCP Sense connection
	@./scripts/mcp-verify.sh --verbose

mcp-diagnostic: ## Run comprehensive MCP diagnostic
	@./scripts/mcp-diagnostic.sh

mcp-health: ## Run MCP health check (for cron/monitoring)
	@./scripts/mcp-health-check.sh

mcp-monitor-setup: ## Install cron job for MCP health monitoring (every 15 min)
	@echo "Adding MCP health check to crontab..."
	@(crontab -l 2>/dev/null | grep -v "mcp-health-check"; echo "*/15 * * * * $(shell pwd)/scripts/mcp-health-check.sh") | crontab -
	@echo "✅ MCP monitoring installed (every 15 min)"

# Code Quality
format: ## Format code with black and isort
	uv run black src tests
	uv run isort src tests

lint: ## Run linting checks
	uv run flake8 src tests
	uv run black --check src tests
	uv run isort --check-only src tests

type-check: ## Run type checking with mypy
	uv run mypy src

security: ## Run security checks
	uv run bandit -r src
	uv run safety check

quality: format lint type-check security ## Run all code quality checks

# Testing
test: ## Run tests in Docker container
	@echo "🧪 Running tests in Docker..."
	@if [ -f test_docker.sh ]; then \
		./test_docker.sh; \
	else \
		docker run --rm -v "$$(pwd)":/app -w /app python:3.11-slim bash -c "pip install -q pytest && pytest tests/unit -v"; \
	fi

test-local: ## Run unit tests locally
	uv run pytest tests/unit -v

spec-check: ## Verify code aligns with specifications
	@echo "🔍 Checking spec alignment..."
	@./scripts/spec-check.sh

test-integration: ## Run integration tests
	uv run pytest tests/integration -v

test-e2e: ## Run end-to-end tests
	uv run pytest tests/e2e -v

test-all: ## Run all tests
	uv run pytest tests -v

test-cov: ## Run tests with coverage
	uv run pytest tests --cov=src --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	uv run pytest-watch tests

# Documentation
docs: ## Build documentation
	uv run mkdocs build

docs-serve: ## Serve documentation locally
	uv run mkdocs serve

docs-deploy: ## Deploy documentation
	uv run mkdocs gh-deploy

# Development Server
serve: ## Run development server
	uv run uvicorn chimera.main:app --reload --host 0.0.0.0 --port 8000

serve-prod: ## Run production server
	uv run uvicorn chimera.main:app --host 0.0.0.0 --port 8000 --workers 4

# Database
db-upgrade: ## Run database migrations
	uv run alembic upgrade head

db-downgrade: ## Rollback database migration
	uv run alembic downgrade -1

db-revision: ## Create new database migration
	uv run alembic revision --autogenerate -m "$(msg)"

db-reset: ## Reset database (WARNING: destroys data)
	uv run alembic downgrade base
	uv run alembic upgrade head

# Docker
docker-build: ## Build Docker image
	docker build -t project-chimera:latest .

docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env project-chimera:latest

docker-compose-up: ## Start services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	docker-compose down

# Deployment
deploy-local: ## Deploy to local environment
	@echo "🚀 Deploying to local environment..."
	docker-compose up -d

deploy-staging: ## Deploy to staging environment
	@echo "🚀 Deploying to staging environment..."
	# Add staging deployment commands here

deploy-prod: ## Deploy to production environment
	@echo "🚀 Deploying to production environment..."
	# Add production deployment commands here

# Monitoring
logs: ## View application logs
	docker-compose logs -f app

monitor: ## Start monitoring stack
	docker-compose -f docker-compose.monitoring.yml up -d

# Utilities
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build package
	uv build

release: ## Create release
	@echo "Creating release..."
	# Add release commands here

# CI/CD
ci-test: ## Run CI test suite
	uv run pytest tests --cov=src --cov-report=xml --junitxml=junit.xml

ci-quality: ## Run CI quality checks
	uv run black --check src tests
	uv run isort --check-only src tests
	uv run flake8 src tests
	uv run mypy src
	uv run bandit -r src
	uv run safety check

ci: ci-quality ci-test ## Run full CI pipeline

# Development Helpers
shell: ## Start Python shell with project context
	uv run python

notebook: ## Start Jupyter notebook
	uv run jupyter notebook

profile: ## Profile application performance
	uv run python -m cProfile -o profile.stats src/chimera/main.py

benchmark: ## Run performance benchmarks
	uv run pytest tests/benchmarks --benchmark-only

# Git Hooks
pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

commit: ## Interactive commit with conventional commits
	@echo "Making conventional commit..."
	git add .
	git commit

# Environment Variables
check-env: ## Validate environment variables for security
	@./scripts/check-env.sh

env-template: ## Create .env template
	@echo "Creating .env template..."
	@./scripts/gen-env-template.sh
	@echo "✅ .env.template created. Copy to .env and fill in your values."

# Auto-sync helpers
auto-sync: ## Run auto-sync to pull latest changes
	./scripts/auto-sync.sh

setup-sync: ## Setup 3-hour auto-sync cron job
	./scripts/setup-cron.sh

check-sync: ## Check auto-sync status and logs
	@echo "📊 Auto-sync Status:"
	@if crontab -l 2>/dev/null | grep -q "auto-sync.sh"; then \
		echo "✅ Cron job active"; \
		crontab -l | grep "auto-sync.sh"; \
	else \
		echo "❌ Cron job not found"; \
	fi
	@echo ""
	@echo "📝 Recent sync logs:"
	@if [ -f logs/auto-sync.log ]; then tail -10 logs/auto-sync.log; else echo "No logs found"; fi

# Daily Development
daily: ## Daily development routine
	@echo "🌅 Starting daily development routine..."
	git pull origin main
	uv sync --all-extras
	make quality
	make test
	@echo "✅ Daily routine complete!"

commit-daily: ## Make daily commit
	@echo "📝 Making daily commit..."
	git add .
	git commit -m "Daily progress: $(shell date '+%Y-%m-%d')"
	git push origin main
	@echo "✅ Daily commit pushed!"