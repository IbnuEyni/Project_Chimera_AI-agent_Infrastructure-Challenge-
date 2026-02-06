#!/usr/bin/env bash
#
# MCP Connection Verification Script for Project Chimera
# Verifies Tenx MCP Sense connectivity to mcppulse.10academy.org
#
# Usage: ./scripts/mcp-verify.sh [--verbose]
# Exit codes: 0 = success, 1 = connection failed, 2 = config error

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MCP_URL="${MCP_URL:-https://mcppulse.10academy.org/proxy}"
LOG_DIR="${PROJECT_DIR}/logs"
VERIFY_LOG="${LOG_DIR}/mcp-verify.log"
VERBOSE=false

[[ "${1:-}" == "--verbose" || "${1:-}" == "-v" ]] && VERBOSE=true

mkdir -p "$LOG_DIR"

log() {
    local level="$1" msg="$2"
    local ts
    ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "[$ts] [$level] $msg" >> "$VERIFY_LOG"
    $VERBOSE && echo "[$level] $msg"
}

log "INFO" "MCP verification started - URL: $MCP_URL"

# Load .env if present for MCP_SENSE_TOKEN
if [[ -f "${PROJECT_DIR}/.env" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "${PROJECT_DIR}/.env"
    set +a
fi

# Check MCP config exists
MCP_JSON="${PROJECT_DIR}/.cursor/mcp.json"
if [[ ! -f "$MCP_JSON" ]]; then
    log "ERROR" "MCP config not found at .cursor/mcp.json"
    echo "❌ MCP config missing"
    exit 2
fi

# Verify JSON validity
if ! command -v jq &>/dev/null; then
    log "WARN" "jq not installed - skipping JSON validation"
else
    if ! jq empty "$MCP_JSON" 2>/dev/null; then
        log "ERROR" "Invalid JSON in .cursor/mcp.json"
        echo "❌ Invalid MCP configuration"
        exit 2
    fi
    log "INFO" "MCP config JSON valid"
fi

# Test HTTP connectivity to MCP proxy
HTTP_CODE=""
if command -v curl &>/dev/null; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 15 \
        -H "X-Device: linux" \
        -H "X-Coding-Tool: vscode" \
        -H "X-Project: project-chimera" \
        -H "Content-Type: application/json" \
        -X POST "$MCP_URL" \
        -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2025-11-05","capabilities":{},"clientInfo":{"name":"mcp-verify","version":"1.0"}}}' 2>/dev/null || echo "000")
else
    log "ERROR" "curl not found - cannot verify connection"
    echo "❌ curl required for verification"
    exit 1
fi

if [[ "$HTTP_CODE" == "200" ]] || [[ "$HTTP_CODE" == "204" ]] || [[ "$HTTP_CODE" =~ ^2 ]]; then
    log "INFO" "MCP connection OK (HTTP $HTTP_CODE)"
    echo "✅ Tenx MCP Sense connection verified"
    exit 0
elif [[ "$HTTP_CODE" == "000" ]]; then
    log "ERROR" "Connection failed - timeout or network error"
    echo "❌ MCP connection failed (timeout/network)"
    exit 1
else
    log "WARN" "Unexpected HTTP response: $HTTP_CODE"
    # Some MCP endpoints return 4xx for malformed requests but are reachable
    if [[ "$HTTP_CODE" =~ ^[45] ]]; then
        log "INFO" "Server reachable but returned $HTTP_CODE - endpoint may require valid MCP handshake"
        echo "⚠️  MCP endpoint reachable (HTTP $HTTP_CODE) - IDE integration may still work"
        exit 0
    fi
    echo "⚠️  Unexpected response: HTTP $HTTP_CODE"
    exit 1
fi
