#!/bin/bash

# Auto-sync script for Project Chimera
# Pulls latest changes every 3 hours and maintains sync

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔄 Project Chimera Auto-Sync Policy"
echo "===================================="
echo "Timestamp: $(date)"
echo "Project Directory: $PROJECT_DIR"

cd "$PROJECT_DIR"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Fetch latest changes
echo "📡 Fetching latest changes from origin..."
git fetch origin main

# Check if there are remote changes
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "🔄 Remote changes detected, pulling..."
    
    # Stash any local changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "💾 Stashing local changes..."
        git stash push -m "Auto-stash before sync at $(date)"
    fi
    
    # Pull latest changes
    git pull origin main
    
    # Restore stashed changes if any
    if git stash list | grep -q "Auto-stash before sync"; then
        echo "🔄 Restoring stashed changes..."
        git stash pop
    fi
    
    echo "✅ Successfully synced with remote"
    echo "📊 Latest commit: $(git log -1 --oneline)"
else
    echo "✅ Already up to date with remote"
fi

# Update dependencies if pyproject.toml changed
if git diff HEAD~1 --name-only 2>/dev/null | grep -q "pyproject.toml"; then
    echo "📦 pyproject.toml changed, updating dependencies..."
    if command -v uv &> /dev/null; then
        uv sync --all-extras
    else
        echo "⚠️  uv not found, skipping dependency update"
    fi
fi

echo "🎯 Auto-sync completed successfully"
echo "Next sync in 3 hours"