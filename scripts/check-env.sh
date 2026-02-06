#!/bin/bash
# Environment Variable Validation Script
# Ensures critical keys are present and meet security formats
# Prevents AI Agent from deploying with malformed or insecure keys

set -e

echo "🔒 Project Chimera - Environment Variable Validation"
echo "===================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ ERROR: .env file not found${NC}"
    echo "   Run: cp .env.template .env"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Load .env file
set -a
source .env
set +a

# ============================================================================
# Validation Functions
# ============================================================================

check_required() {
    local var_name=$1
    local var_value="${!var_name}"
    
    if [ -z "$var_value" ]; then
        echo -e "${RED}❌ ERROR: $var_name is not set${NC}"
        ((ERRORS++))
        return 1
    else
        echo -e "${GREEN}✅ $var_name is set${NC}"
        return 0
    fi
}

check_format() {
    local var_name=$1
    local var_value="${!var_name}"
    local pattern=$2
    local description=$3
    
    if [[ ! "$var_value" =~ $pattern ]]; then
        echo -e "${RED}❌ ERROR: $var_name format invalid${NC}"
        echo "   Expected: $description"
        echo "   Got: ${var_value:0:20}..."
        ((ERRORS++))
        return 1
    else
        echo -e "${GREEN}✅ $var_name format valid${NC}"
        return 0
    fi
}

check_length() {
    local var_name=$1
    local var_value="${!var_name}"
    local min_length=$2
    
    if [ ${#var_value} -lt $min_length ]; then
        echo -e "${RED}❌ ERROR: $var_name too short (min: $min_length chars)${NC}"
        echo "   Current length: ${#var_value}"
        ((ERRORS++))
        return 1
    else
        echo -e "${GREEN}✅ $var_name length valid (${#var_value} chars)${NC}"
        return 0
    fi
}

check_numeric() {
    local var_name=$1
    local var_value="${!var_name}"
    
    if ! [[ "$var_value" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        echo -e "${RED}❌ ERROR: $var_name must be numeric${NC}"
        echo "   Got: $var_value"
        ((ERRORS++))
        return 1
    else
        echo -e "${GREEN}✅ $var_name is numeric${NC}"
        return 0
    fi
}

check_url() {
    local var_name=$1
    local var_value="${!var_name}"
    
    if [[ ! "$var_value" =~ ^(postgresql|redis|http|https):// ]]; then
        echo -e "${YELLOW}⚠️  WARNING: $var_name may not be a valid URL${NC}"
        echo "   Got: $var_value"
        ((WARNINGS++))
        return 1
    else
        echo -e "${GREEN}✅ $var_name is valid URL${NC}"
        return 0
    fi
}

# ============================================================================
# Critical Variables Validation
# ============================================================================

echo "📋 Checking Critical Variables..."
echo "-----------------------------------"

# Database
check_required "DATABASE_URL"
check_url "DATABASE_URL"
echo ""

# Redis
check_required "REDIS_URL"
check_url "REDIS_URL"
echo ""

# Budget Limits (Financial Safety)
echo "💰 Financial Safety Checks..."
check_required "DAILY_BUDGET_LIMIT"
check_numeric "DAILY_BUDGET_LIMIT"

check_required "WEEKLY_BUDGET_LIMIT"
check_numeric "WEEKLY_BUDGET_LIMIT"

check_required "MONTHLY_BUDGET_LIMIT"
check_numeric "MONTHLY_BUDGET_LIMIT"

check_required "MIN_ROI_HURDLE_RATE"
check_numeric "MIN_ROI_HURDLE_RATE"
echo ""

# Validate budget hierarchy
if [ -n "$DAILY_BUDGET_LIMIT" ] && [ -n "$WEEKLY_BUDGET_LIMIT" ]; then
    daily_float=$(echo "$DAILY_BUDGET_LIMIT" | bc)
    weekly_float=$(echo "$WEEKLY_BUDGET_LIMIT" | bc)
    
    if (( $(echo "$daily_float * 7 > $weekly_float" | bc -l) )); then
        echo -e "${YELLOW}⚠️  WARNING: Daily budget * 7 exceeds weekly budget${NC}"
        ((WARNINGS++))
    fi
fi

# ============================================================================
# API Keys Validation
# ============================================================================

echo "🔑 API Keys Validation..."
echo "-------------------------"

# OpenAI
if [ -n "$OPENAI_API_KEY" ]; then
    check_format "OPENAI_API_KEY" "^sk-" "Must start with 'sk-'"
    check_length "OPENAI_API_KEY" 40
else
    echo -e "${YELLOW}⚠️  WARNING: OPENAI_API_KEY not set (optional)${NC}"
    ((WARNINGS++))
fi
echo ""

# Coinbase CDP (Critical for Agentic Commerce)
echo "🏦 Coinbase CDP Keys (Critical)..."
if [ -n "$CDP_API_KEY_NAME" ]; then
    check_length "CDP_API_KEY_NAME" 10
else
    echo -e "${RED}❌ ERROR: CDP_API_KEY_NAME not set${NC}"
    echo "   Required for agentic commerce"
    ((ERRORS++))
fi

if [ -n "$CDP_API_KEY_PRIVATE_KEY" ]; then
    check_length "CDP_API_KEY_PRIVATE_KEY" 32
    
    # Check if it's a placeholder
    if [[ "$CDP_API_KEY_PRIVATE_KEY" == *"your"* ]] || [[ "$CDP_API_KEY_PRIVATE_KEY" == *"placeholder"* ]]; then
        echo -e "${RED}❌ ERROR: CDP_API_KEY_PRIVATE_KEY is a placeholder${NC}"
        echo "   Replace with actual private key"
        ((ERRORS++))
    fi
else
    echo -e "${RED}❌ ERROR: CDP_API_KEY_PRIVATE_KEY not set${NC}"
    echo "   Required for agentic commerce"
    ((ERRORS++))
fi
echo ""

# ============================================================================
# Security Checks
# ============================================================================

echo "🛡️  Security Checks..."
echo "---------------------"

# Check for common insecure values
insecure_patterns=("password" "123456" "admin" "test" "demo")

for pattern in "${insecure_patterns[@]}"; do
    if grep -qi "$pattern" .env 2>/dev/null; then
        echo -e "${YELLOW}⚠️  WARNING: Potentially insecure value detected: '$pattern'${NC}"
        ((WARNINGS++))
    fi
done

# Check JWT secret length
if [ -n "$JWT_SECRET" ]; then
    if [ ${#JWT_SECRET} -lt 32 ]; then
        echo -e "${RED}❌ ERROR: JWT_SECRET too short (min: 32 chars)${NC}"
        ((ERRORS++))
    else
        echo -e "${GREEN}✅ JWT_SECRET length valid${NC}"
    fi
fi

# Check if .env is in .gitignore
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo -e "${RED}❌ ERROR: .env not in .gitignore${NC}"
    echo "   Add '.env' to .gitignore to prevent committing secrets"
    ((ERRORS++))
else
    echo -e "${GREEN}✅ .env is in .gitignore${NC}"
fi

echo ""

# ============================================================================
# Summary
# ============================================================================

echo "===================================================="
echo "📊 Validation Summary"
echo "===================================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo "   Environment is properly configured"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  $WARNINGS warning(s) found${NC}"
    echo "   Environment is usable but has warnings"
    exit 0
else
    echo -e "${RED}❌ $ERRORS error(s) found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  $WARNINGS warning(s) found${NC}"
    fi
    echo ""
    echo "Fix errors before deploying the AI swarm"
    exit 1
fi
