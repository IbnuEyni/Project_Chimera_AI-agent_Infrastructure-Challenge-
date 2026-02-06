# Skill: Financial Approval

**Agent**: CFO  
**Version**: 1.0.0  
**Status**: Ready for Implementation

---

## Purpose

Approve or reject resource requests from worker agents based on budget constraints, ROI projections, and risk assessment.

---

## Input Contract

```python
from pydantic import BaseModel, Field
from typing import Literal
from decimal import Decimal

class FinancialApprovalInput(BaseModel):
    """Input schema for financial approval."""
    
    request_id: str = Field(
        ...,
        description="Unique request UUID"
    )
    
    agent_id: str = Field(
        ...,
        description="Requesting agent UUID"
    )
    
    request_type: Literal["api_call", "compute", "storage", "blockchain"] = Field(
        ...,
        description="Type of resource request"
    )
    
    request_cost: Decimal = Field(
        ...,
        gt=0,
        description="Requested amount in USD"
    )
    
    projected_roi: float = Field(
        ...,
        ge=0.0,
        description="Projected return on investment"
    )
    
    justification: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Business justification"
    )
```

---

## Output Contract

```python
class FinancialApprovalOutput(BaseModel):
    """Output schema for financial approval."""
    
    request_id: str = Field(
        ...,
        description="Request UUID"
    )
    
    approved: bool = Field(
        ...,
        description="Approval decision"
    )
    
    reason: str = Field(
        ...,
        description="Approval/rejection reason"
    )
    
    risk_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Risk assessment (0=low, 1=high)"
    )
    
    approval_signature: str = Field(
        ...,
        description="CFO cryptographic signature"
    )
    
    budget_remaining: dict[str, Decimal] = Field(
        ...,
        description="Remaining budget by period"
    )
    
    conditions: list[str] = Field(
        default=[],
        description="Approval conditions"
    )
```

---

## Approval Rules

### Rule 1: Budget Check
```python
if request_cost > daily_remaining_budget:
    return REJECT("Daily budget exceeded")
```

### Rule 2: ROI Check
```python
MIN_HURDLE_RATE = 1.5

if projected_roi < MIN_HURDLE_RATE:
    return REJECT(f"ROI {projected_roi} below hurdle rate {MIN_HURDLE_RATE}")
```

### Rule 3: Risk Assessment
```python
if risk_score > 0.7:
    return ESCALATE("High risk - requires human approval")
```

### Rule 4: Category Limits
```python
if category_spent + request_cost > category_limit:
    return REJECT(f"Category limit exceeded for {request_type}")
```

---

## Performance Requirements

- **Latency**: <300ms (P95)
- **Success Rate**: >99%
- **Precision**: >99% (no false approvals)
- **Logging**: 100% to immutable ledger
- **Cost**: $0.00 (internal operation)

---

## Error Handling

```python
class FinancialApprovalError(Exception):
    """Base exception for financial approval."""
    pass

class BudgetExceededError(FinancialApprovalError):
    """Raised when budget limit is exceeded."""
    pass

class InvalidROIError(FinancialApprovalError):
    """Raised when ROI is below hurdle rate."""
    pass

class SignatureGenerationError(FinancialApprovalError):
    """Raised when signature generation fails."""
    pass
```

---

## Usage Example

```python
from skills.skill_financial_approval import execute, FinancialApprovalInput
from decimal import Decimal

# Create input
input_data = FinancialApprovalInput(
    request_id="req-123",
    agent_id="agent-456",
    request_type="api_call",
    request_cost=Decimal("15.00"),
    projected_roi=2.5,
    justification="Generate viral video for trending topic"
)

# Execute skill
try:
    result = await execute(input_data)
    
    if result.approved:
        print(f"✅ Approved: {result.reason}")
        print(f"Signature: {result.approval_signature}")
        print(f"Budget remaining: ${result.budget_remaining['daily']}")
    else:
        print(f"❌ Rejected: {result.reason}")
        
except FinancialApprovalError as e:
    logger.error(f"Approval failed: {e}")
```

---

## Implementation Notes

1. **Database-Level Enforcement**: Budget caps enforced via CHECK constraints
2. **Immutable Logging**: Every decision logged to ledger table
3. **Cryptographic Signatures**: Use Ed25519 for approval signatures
4. **Atomic Operations**: Use database transactions for budget updates
5. **Real-time Budget Tracking**: Redis cache for fast budget checks
6. **Audit Trail**: Complete history of all approvals/rejections

---

## Decision Flow

```
1. Validate input schema
   ↓
2. Check daily budget remaining
   ↓ (if sufficient)
3. Check weekly/monthly budgets
   ↓ (if sufficient)
4. Evaluate projected ROI
   ↓ (if >= hurdle rate)
5. Calculate risk score
   ↓ (if < 0.7)
6. Generate approval signature
   ↓
7. Log to ledger (immutable)
   ↓
8. Update budget tracking
   ↓
9. Return approval
```

---

## Budget Limits (Default)

| Period | Limit | Enforcement |
|--------|-------|-------------|
| Daily | $1,000 | Database CHECK |
| Weekly | $5,000 | Database CHECK |
| Monthly | $20,000 | Database CHECK |

---

## Testing Strategy

- Unit tests for each approval rule
- Integration tests with PostgreSQL
- Performance tests to validate <300ms
- Security tests for signature verification
- Load tests with 1000 concurrent requests

---

## Dependencies

- `pydantic`: Schema validation
- `asyncpg`: PostgreSQL async driver
- `cryptography`: Signature generation
- `redis`: Budget caching

---

## References

- Functional Spec: `../../specs/functional.md` (Section 4)
- Technical Spec: `../../specs/technical.md` (Financial Approval)
- Database Schema: `../../specs/technical.md` (ledger, budget_tracking tables)
