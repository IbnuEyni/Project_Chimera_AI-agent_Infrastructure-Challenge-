#!/bin/bash
# Spec alignment verification script

set -e

echo "📋 Checking specification alignment..."

# Check if specs directory exists
if [ ! -d "specs" ]; then
    echo "❌ specs/ directory not found"
    exit 1
fi

# Check for required spec files
REQUIRED_SPECS=("_meta.md" "technical.md" "functional.md")
for spec in "${REQUIRED_SPECS[@]}"; do
    if [ ! -f "specs/$spec" ]; then
        echo "❌ Missing spec: specs/$spec"
        exit 1
    fi
done

echo "✅ All required spec files present"

# Check if implementation matches architecture
if grep -q "ChimeraSwarm" src/chimera/core/__init__.py && \
   grep -q "SecurityGateway" src/chimera/security/__init__.py && \
   grep -q "AgenticCommerce" src/chimera/commerce/__init__.py; then
    echo "✅ Core architecture implemented"
else
    echo "❌ Core architecture incomplete"
    exit 1
fi

echo "✅ Spec alignment verified"
