#!/bin/bash

# Project Chimera Environment Setup Script
# This script initializes the development environment for Project Chimera

set -e

echo "🚀 Initializing Project Chimera Environment..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        # Try multiple ways to source uv
        if [ -f "$HOME/.cargo/env" ]; then
            source "$HOME/.cargo/env"
        elif [ -f "$HOME/.local/bin/uv" ]; then
            export PATH="$HOME/.local/bin:$PATH"
        fi
        
        # Verify uv is now available
        if ! command -v uv &> /dev/null; then
            echo "❌ Failed to install uv. Please install manually and retry."
            exit 1
        fi
    else
        echo "❌ Failed to download uv installer. Check your internet connection."
        exit 1
    fi
fi

# Initialize Python project with uv
echo "🐍 Setting up Python environment..."
# Try Python 3.11 first, fallback to available versions
if ! uv init --python 3.11 2>/dev/null; then
    echo "⚠️ Python 3.11 not found, trying Python 3.10+..."
    if ! uv init --python 3.10+ 2>/dev/null; then
        echo "⚠️ Trying any available Python 3.x..."
        if ! uv init --python 3.8+ 2>/dev/null; then
            echo "❌ No compatible Python version found. Please install Python 3.8+ and retry."
            exit 1
        fi
    fi
fi

# Install core dependencies
echo "📚 Installing dependencies..."
uv add fastapi uvicorn pydantic sqlalchemy alembic redis celery
uv add --dev pytest pytest-asyncio black isort mypy pre-commit

# Create .env template
echo "⚙️ Creating environment configuration..."
cat > .env.template << EOF
# Project Chimera Environment Variables
DATABASE_URL=postgresql://user:password@localhost:5432/chimera
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
MCP_SENSE_TOKEN=your_mcp_token_here
LOG_LEVEL=INFO
ENVIRONMENT=development
EOF

# Initialize git repository
echo "📝 Initializing Git repository..."
git init
git add .
git commit -m "Initial commit: Project Chimera foundation"

echo "✅ Environment setup complete!"
echo "📋 Next steps:"
echo "   1. Copy .env.template to .env and fill in your API keys"
echo "   2. Run 'make setup-golden' for MCP Sense + Golden environment"
echo "   3. Run 'make setup' to complete installation"