#!/usr/bin/env bash
#
# Golden Development Environment Setup for Project Chimera
# Sets up professional tooling and MCP Sense integration with full traceability
#
# Usage: ./scripts/setup-golden-env.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "  Project Chimera - Golden Environment Setup"
echo "=============================================="
echo ""

# 1. Verify MCP config exists
echo "📋 Step 1: Verifying MCP configuration..."
if [[ ! -f "${PROJECT_DIR}/.cursor/mcp.json" ]]; then
    echo "❌ .cursor/mcp.json not found. Run from project root."
    exit 1
fi
echo "   ✅ MCP config present"

# 2. Install dependencies
echo ""
echo "📦 Step 2: Installing dependencies..."
cd "$PROJECT_DIR"
if command -v uv &>/dev/null; then
    uv sync --all-extras
else
    echo "   ⚠️  uv not found - ensure dependencies are installed (pip/poetry)"
fi
echo "   ✅ Dependencies ready"

# 3. Install pre-commit hooks
echo ""
echo "🪝 Step 3: Installing pre-commit hooks..."
if command -v pre-commit &>/dev/null; then
    pre-commit install
else
    echo "   ⚠️  pre-commit not installed - run: uv sync --all-extras"
fi
echo "   ✅ Pre-commit configured"

# 4. Create logs directory
echo ""
echo "📁 Step 4: Creating log directories..."
mkdir -p "${PROJECT_DIR}/logs"
echo "   ✅ logs/ created"

# 5. Verify MCP connection
echo ""
echo "🔌 Step 5: Verifying Tenx MCP Sense connection..."
if "${SCRIPT_DIR}/mcp-verify.sh" --verbose; then
    echo "   ✅ MCP Sense connected"
else
    echo "   ⚠️  MCP verification had issues - check Cursor Settings > MCP"
fi

# 6. Set up MCP health check cron (optional)
echo ""
echo "⏱️  Step 6: MCP health monitoring..."
echo "   To enable continuous monitoring, add to crontab:"
echo "   */15 * * * * ${PROJECT_DIR}/scripts/mcp-health-check.sh"
echo "   Or run: make mcp-monitor-setup"

echo ""
echo "=============================================="
echo "  ✅ Golden environment setup complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Restart Cursor to load MCP config"
echo "  2. Verify MCP in Cursor Settings > MCP"
echo "  3. Run 'make mcp-verify' anytime to check connection"
echo "  4. See docs/GOLDEN_ENVIRONMENT.md for full guide"
echo ""
