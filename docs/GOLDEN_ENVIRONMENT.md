# Golden Development Environment - Project Chimera

This document describes the "Golden" development environment for Project Chimera, including professional tooling and Tenx MCP Sense integration for telemetry, connection verification, and full development activity traceability.

## Overview

The Golden environment provides:

- **Tenx MCP Sense** connection to the IDE for telemetry
- **Connection logging and verification** scripts
- **Continuous monitoring and health checks** (optional cron)
- **Traceability** for all development activities via structured logging

## Quick Start

```bash
# Full Golden environment setup
make setup-golden

# Verify MCP connection anytime
make mcp-verify

# Run health check (e.g. from cron)
make mcp-health
```

## MCP Sense Integration

### Configuration

MCP Sense is configured in `.cursor/mcp.json`:

- **URL**: `https://mcppulse.10academy.org/proxy`
- **Headers**: `X-Device`, `X-Coding-Tool`, `X-Project`, `X-Environment`, `X-Project-Phase`

These headers enable telemetry and traceability on the 10Academy MCP Pulse service.

### Verification

1. **Manual verification**:

   ```bash
   make mcp-verify
   # or
   ./scripts/mcp-verify.sh --verbose
   ```

2. **In Cursor**: Settings → MCP → Check that `tenxfeedbackanalytics` is connected and green.

### Available MCP Tools

Once connected, the following tools are available via MCP Sense:

- `list_managed_servers` - Lists downstream MCP servers and their status
- `log_passage_time_trigger` - Logs passage time events (traceability)
- `log_performance_outlier_trigger` - Logs performance outlier events

## Connection Logging

All MCP connection attempts and verifications are logged to:

- `logs/mcp-verify.log` - Verification script output
- `logs/mcp-health.log` - Health check output (when using cron)

The Python module `chimera.mcp.sense` provides structured logging for:

- Connection attempts
- Verification results
- Development activity events

## Continuous Monitoring

To enable periodic health checks:

```bash
make mcp-monitor-setup
```

This adds a cron job that runs `mcp-health-check.sh` every 15 minutes. Logs are written to `logs/mcp-health.log` and rotated when exceeding 1MB.

## Environment Variables

| Variable          | Description                      | Default                                |
| ----------------- | -------------------------------- | -------------------------------------- |
| `MCP_SENSE_URL`   | MCP Pulse proxy URL              | `https://mcppulse.10academy.org/proxy` |
| `MCP_SENSE_TOKEN` | Optional auth token              | (empty)                                |
| `MCP_PROJECT`     | Project identifier for telemetry | `project-chimera`                      |
| `MCP_ENVIRONMENT` | Environment label                | `golden`                               |

## Traceability

Development activity traceability is achieved through:

1. **MCP headers** - Every request includes project and environment identifiers
2. **Structured logs** - `chimera.mcp.sense.MCPSenseLogger` logs connection and activity events
3. **MCP Sense tools** - `log_passage_time_trigger` and `log_performance_outlier_trigger` send events to the telemetry backend

### Using the Sense Logger

```python
from chimera.mcp.sense import get_sense_logger

logger = get_sense_logger()
logger.log_connection_attempt(success=True)
logger.log_verification(success=True, http_code=200)
logger.log_activity("task_completion", metadata={"task_id": "xyz"})
```

## Troubleshooting

| Issue                        | Action                                                      |
| ---------------------------- | ----------------------------------------------------------- |
| MCP config not found         | Ensure `.cursor/mcp.json` exists and is valid JSON          |
| Connection timeout           | Check network; verify `mcppulse.10academy.org` is reachable |
| MCP server errored in Cursor | Restart Cursor; run `make mcp-verify`; check Settings → MCP |
| Curl not found               | Install curl (required for `mcp-verify.sh`)                 |

## File Structure

```
.cursor/
  mcp.json                 # MCP Sense configuration
scripts/
  mcp-verify.sh            # Connection verification
  mcp-health-check.sh      # Health check (for cron)
  setup-golden-env.sh      # Golden environment setup
logs/
  mcp-verify.log           # Verification logs
  mcp-health.log           # Health check logs
src/chimera/mcp/
  sense.py                 # MCP Sense Python integration
```
