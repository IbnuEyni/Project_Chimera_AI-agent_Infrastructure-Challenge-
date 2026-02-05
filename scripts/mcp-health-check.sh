#!/usr/bin/env bash
#
# MCP Health Check Script - Continuous monitoring for Project Chimera
# Run via cron for periodic health checks and logging
#
# Usage: ./scripts/mcp-health-check.sh
# Cron: */15 * * * * (every 15 min) or */5 * * * * (every 5 min)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="${PROJECT_DIR}/logs"
HEALTH_LOG="${LOG_DIR}/mcp-health.log"
VERIFY_SCRIPT="${SCRIPT_DIR}/mcp-verify.sh"
RETENTION_DAYS=7

mkdir -p "$LOG_DIR"

run_check() {
    local result
    if "$VERIFY_SCRIPT" >> "$HEALTH_LOG" 2>&1; then
        result="OK"
    else
        result="FAIL"
    fi
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S") UTC] MCP health: $result"
    return 0
}

# Rotate logs if too large (>1MB)
if [[ -f "$HEALTH_LOG" ]] && [[ $(stat -c%s "$HEALTH_LOG" 2>/dev/null || echo 0) -gt 1048576 ]]; then
    mv "$HEALTH_LOG" "${HEALTH_LOG}.old"
fi

# Run health check
run_check

# Optional: trim old logs
find "$LOG_DIR" -name "mcp-health.log.*" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
