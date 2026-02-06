"""
Asset Ledger with Reasoning Hash

Provides fully explainable P&L by linking transactions to justifications.
Each transaction records WHY it was made, not just WHAT was done.
"""

from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
import hashlib
import json


class ReasoningContext(BaseModel):
    """Context explaining why a transaction was made."""
    
    trend_id: Optional[str] = Field(None, description="Trend that justified this spend")
    trend_topic: Optional[str] = Field(None, description="Trend topic")
    projected_roi: float = Field(..., description="Expected ROI")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Agent confidence")
    justification: str = Field(..., description="Human-readable justification")
    agent_id: str = Field(..., description="Agent that made decision")
    
    def to_hash(self) -> str:
        """Generate reasoning hash for audit trail."""
        data = self.model_dump_json(sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()


class AssetLedger(BaseModel):
    """
    Enhanced ledger entry with reasoning hash.
    
    Links every transaction to its business justification,
    making P&L fully explainable and auditable.
    """
    
    # Transaction Details
    tx_id: str = Field(..., description="Transaction UUID")
    tx_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    agent_id: str = Field(..., description="Agent that initiated transaction")
    
    # Financial Details
    amount: Decimal = Field(..., gt=0, description="Transaction amount in USD")
    currency: str = Field(default="USDC", description="Currency")
    transaction_type: str = Field(..., description="Type: api_call, compute, storage, blockchain")
    
    # Reasoning & Justification
    reasoning_hash: str = Field(..., description="SHA256 hash of reasoning context")
    reasoning_context: ReasoningContext = Field(..., description="Full reasoning context")
    
    # Approval & Governance
    approved: bool = Field(..., description="CFO approval status")
    approval_signature: str = Field(..., description="CFO cryptographic signature")
    cfo_agent_id: str = Field(..., description="CFO agent that approved")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk assessment")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
    
    # P&L Tracking
    expected_revenue: Optional[Decimal] = Field(None, description="Expected revenue from this spend")
    actual_revenue: Optional[Decimal] = Field(None, description="Actual revenue realized")
    roi_actual: Optional[float] = Field(None, description="Actual ROI achieved")
    
    def calculate_roi(self) -> Optional[float]:
        """Calculate actual ROI if revenue is recorded."""
        if self.actual_revenue is not None and self.amount > 0:
            return float((self.actual_revenue - self.amount) / self.amount)
        return None
    
    def verify_reasoning_hash(self) -> bool:
        """Verify reasoning hash matches context."""
        expected_hash = self.reasoning_context.to_hash()
        return self.reasoning_hash == expected_hash
    
    def to_pnl_report(self) -> dict:
        """Generate P&L report entry."""
        return {
            "tx_id": self.tx_id,
            "date": self.created_at.isoformat(),
            "spend": float(self.amount),
            "expected_revenue": float(self.expected_revenue) if self.expected_revenue else None,
            "actual_revenue": float(self.actual_revenue) if self.actual_revenue else None,
            "roi_projected": self.reasoning_context.projected_roi,
            "roi_actual": self.calculate_roi(),
            "trend": self.reasoning_context.trend_topic,
            "justification": self.reasoning_context.justification,
            "agent": self.agent_id,
            "reasoning_hash": self.reasoning_hash
        }


class PLReport(BaseModel):
    """Profit & Loss report with full traceability."""
    
    period_start: datetime
    period_end: datetime
    total_spend: Decimal = Decimal("0.00")
    total_revenue: Decimal = Decimal("0.00")
    net_profit: Decimal = Decimal("0.00")
    roi_average: float = 0.0
    transactions: list[AssetLedger] = []
    
    def add_transaction(self, ledger_entry: AssetLedger):
        """Add transaction to P&L report."""
        self.transactions.append(ledger_entry)
        self.total_spend += ledger_entry.amount
        
        if ledger_entry.actual_revenue:
            self.total_revenue += ledger_entry.actual_revenue
    
    def calculate_summary(self):
        """Calculate P&L summary."""
        self.net_profit = self.total_revenue - self.total_spend
        
        # Calculate average ROI
        rois = [t.calculate_roi() for t in self.transactions if t.calculate_roi() is not None]
        self.roi_average = sum(rois) / len(rois) if rois else 0.0
    
    def to_report(self) -> dict:
        """Generate human-readable P&L report."""
        return {
            "period": {
                "start": self.period_start.isoformat(),
                "end": self.period_end.isoformat()
            },
            "summary": {
                "total_spend": float(self.total_spend),
                "total_revenue": float(self.total_revenue),
                "net_profit": float(self.net_profit),
                "roi_average": self.roi_average,
                "transaction_count": len(self.transactions)
            },
            "transactions": [t.to_pnl_report() for t in self.transactions]
        }


# Example usage
def create_ledger_entry(
    tx_id: str,
    agent_id: str,
    amount: Decimal,
    trend_id: str,
    trend_topic: str,
    projected_roi: float,
    confidence: float,
    justification: str
) -> AssetLedger:
    """Create ledger entry with reasoning hash."""
    
    # Create reasoning context
    reasoning = ReasoningContext(
        trend_id=trend_id,
        trend_topic=trend_topic,
        projected_roi=projected_roi,
        confidence_score=confidence,
        justification=justification,
        agent_id=agent_id
    )
    
    # Generate reasoning hash
    reasoning_hash = reasoning.to_hash()
    
    # Create ledger entry
    return AssetLedger(
        tx_id=tx_id,
        agent_id=agent_id,
        amount=amount,
        transaction_type="api_call",
        reasoning_hash=reasoning_hash,
        reasoning_context=reasoning,
        approved=True,
        approval_signature="0x" + "a" * 64,
        cfo_agent_id="cfo-001",
        risk_score=0.25,
        expected_revenue=amount * Decimal(str(projected_roi))
    )
