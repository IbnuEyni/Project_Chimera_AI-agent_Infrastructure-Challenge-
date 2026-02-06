"""Commerce Manager contract definitions."""
from pydantic import BaseModel
from typing import Literal
from decimal import Decimal


class FinancialApprovalInput(BaseModel):
    """Input schema for financial approval."""
    request_id: str
    agent_id: str
    request_type: Literal["api_call", "compute", "storage", "blockchain"]
    request_cost: Decimal
    projected_roi: float
    justification: str = Field(..., min_length=1)


class FinancialApprovalOutput(BaseModel):
    """Output schema for financial approval."""
    request_id: str
    approved: bool
    reason: str
    risk_score: float
    approval_signature: str
    budget_remaining: dict[str, Decimal]
    conditions: list[str] = []
