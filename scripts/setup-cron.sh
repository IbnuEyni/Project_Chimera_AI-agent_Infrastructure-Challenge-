#!/bin/bash

# Setup cron job for 3-hour auto-sync policy
# Run this script once to install the cron job

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SYNC_SCRIPT="$PROJECT_DIR/scripts/auto-sync.sh"

echo "🕐 Setting up 3-hour auto-sync cron job"
echo "======================================"

# Check if sync script exists
if [ ! -f "$SYNC_SCRIPT" ]; then
    echo "❌ Error: auto-sync.sh not found at $SYNC_SCRIPT"
    exit 1
fi

# Create cron job entry
CRON_JOB="0 */3 * * * cd $PROJECT_DIR && $SYNC_SCRIPT >> $PROJECT_DIR/logs/auto-sync.log 2>&1"

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "auto-sync.sh"; then
    echo "⚠️  Cron job already exists, updating..."
    # Remove existing job
    crontab -l 2>/dev/null | grep -v "auto-sync.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job installed successfully"
echo "📅 Schedule: Every 3 hours (0, 3, 6, 9, 12, 15, 18, 21)"
echo "📝 Logs: $PROJECT_DIR/logs/auto-sync.log"
echo ""
echo "To verify installation:"
echo "  crontab -l"
echo ""
echo "To remove the cron job:"
echo "  crontab -l | grep -v 'auto-sync.sh' | crontab -"