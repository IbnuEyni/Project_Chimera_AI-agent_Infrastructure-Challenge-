#!/usr/bin/env bash
#
# MCP Diagnostic Script for Project Chimera
# Comprehensive check for MCP server integration issues
#

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "🔍 MCP Server Diagnostic for Project Chimera"
echo "============================================="

# Check 1: MCP Configuration
echo "1. Checking MCP Configuration..."
if [[ -f "$PROJECT_DIR/.cursor/mcp.json" ]]; then
    echo "✅ MCP config found"
    if command -v jq &>/dev/null; then
        echo "   URL: $(jq -r '.mcpServers.tenxfeedbackanalytics.url' "$PROJECT_DIR/.cursor/mcp.json")"
    fi
else
    echo "❌ MCP config missing at .cursor/mcp.json"
fi

# Check 2: Environment Variables
echo -e "\n2. Checking Environment Variables..."
if [[ -f "$PROJECT_DIR/.env" ]]; then
    echo "✅ .env file found"
    if grep -q "MCP_SENSE_TOKEN=" "$PROJECT_DIR/.env"; then
        if grep -q "MCP_SENSE_TOKEN=$" "$PROJECT_DIR/.env" || grep -q "MCP_SENSE_TOKEN=your_mcp_token_here" "$PROJECT_DIR/.env"; then
            echo "⚠️  MCP_SENSE_TOKEN is empty - you need to get your token from 10Academy"
        else
            echo "✅ MCP_SENSE_TOKEN is set"
        fi
    else
        echo "❌ MCP_SENSE_TOKEN not found in .env"
    fi
else
    echo "❌ .env file missing - created template for you"
fi

# Check 3: VS Code/Cursor MCP Integration
echo -e "\n3. Checking IDE Integration..."
if [[ -f "$HOME/.config/Cursor/User/settings.json" ]]; then
    echo "✅ Cursor settings found"
    if grep -q "mcp" "$HOME/.config/Cursor/User/settings.json"; then
        echo "✅ MCP settings detected in Cursor"
    else
        echo "⚠️  No MCP settings in Cursor - may need manual configuration"
    fi
else
    echo "⚠️  Cursor settings not found"
fi

# Check 4: Network Connectivity
echo -e "\n4. Testing Network Connectivity..."
if curl -s --connect-timeout 5 https://mcppulse.10academy.org/proxy > /dev/null; then
    echo "✅ MCP server is reachable"
else
    echo "❌ Cannot reach MCP server - check internet connection"
fi

# Check 5: GitHub Copilot Status
echo -e "\n5. Checking GitHub Copilot..."
if command -v code &>/dev/null; then
    if code --list-extensions | grep -q "github.copilot"; then
        echo "✅ GitHub Copilot extension installed"
    else
        echo "⚠️  GitHub Copilot extension not found"
    fi
else
    echo "⚠️  VS Code CLI not available"
fi

echo -e "\n📋 Next Steps:"
echo "1. Get your MCP_SENSE_TOKEN from 10Academy team"
echo "2. Add the token to your .env file"
echo "3. Restart VS Code/Cursor"
echo "4. Test with: make mcp-verify"
echo -e "\n💬 For team support, use the Slack message below:"