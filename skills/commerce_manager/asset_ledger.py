"""Asset Ledger - Production Implementation.

Implements reasoning hash and explainable P&L reporting.
"""

import hashlib
import json
from decimal import Decimal
from datetime import datetime
from typing import List, Optional


class ReasoningContext:
    """Reasoning context for financial decisions with cryptographic hash."""
    
    def __init__(self, **kwargs):
        self.trend_id = kwargs.get('trend_id', '')
        self.trend_topic = kwargs.get('trend_topic', '')
        self.projected_roi = kwargs.get('projected_roi', 0.0)
        self.confidence_score = kwargs.get('confidence_score', 0.0)
        self.justification = kwargs.get('justification', '')
        self.agent_id = kwargs.get('agent_id', '')

    def to_hash(self) -> str:
        """Generate SHA256 hash of reasoning context.
        
        Returns:
            64-character hex string (SHA256)
        """
        context_data = {
            'trend_id': self.trend_id,
            'trend_topic': self.trend_topic,
            'projected_roi': self.projected_roi,
            'confidence_score': self.confidence_score,
            'justification': self.justification,
            'agent_id': self.agent_id
        }
        # Create deterministic JSON string
        json_str = json.dumps(context_data, sort_keys=True)
        # Generate SHA256 hash
        return hashlib.sha256(json_str.encode()).hexdigest()


class LedgerEntry:
    """Ledger entry with reasoning context and ROI tracking."""
    
    def __init__(self, **kwargs):
        self.tx_id = kwargs.get('tx_id', '')
        self.agent_id = kwargs.get('agent_id', '')
        self.amount = kwargs.get('amount', Decimal('0.00'))
        self.actual_revenue = Decimal('0.00')
        
        # Create reasoning context
        self.reasoning_context = ReasoningContext(
            trend_id=kwargs.get('trend_id', ''),
            trend_topic=kwargs.get('trend_topic', ''),
            projected_roi=kwargs.get('projected_roi', 0.0),
            confidence=kwargs.get('confidence', 0.0),
            justification=kwargs.get('justification', ''),
            agent_id=kwargs.get('agent_id', '')
        )
        
        # Store original hash for verification
        self._original_hash = self.reasoning_context.to_hash()

    def verify_reasoning_hash(self) -> bool:
        """Verify reasoning hash integrity.
        
        Returns:
            True if hash matches original, False otherwise
        """
        current_hash = self.reasoning_context.to_hash()
        return current_hash == self._original_hash

    def calculate_roi(self) -> float:
        """Calculate ROI from actual revenue.
        
        Returns:
            ROI as decimal (e.g., 1.5 = 150% return)
        """
        if self.amount == 0:
            return 0.0
        return float((self.actual_revenue - self.amount) / self.amount)
    
    def to_pnl_report(self) -> dict:
        """Convert to P&L report entry.
        
        Returns:
            Dictionary with transaction details and justification
        """
        return {
            'tx_id': self.tx_id,
            'agent_id': self.agent_id,
            'amount': float(self.amount),
            'revenue': float(self.actual_revenue),
            'roi': self.calculate_roi(),
            'trend': self.reasoning_context.trend_topic,
            'justification': self.reasoning_context.justification,
            'reasoning_hash': self.reasoning_context.to_hash()
        }


class PLReport:
    """P&L report generator with transaction aggregation."""
    
    def __init__(self, period_start: datetime, period_end: datetime):
        self.period_start = period_start
        self.period_end = period_end
        self.transactions: List[LedgerEntry] = []
        self.total_spend = Decimal('0.00')
        self.total_revenue = Decimal('0.00')
        self.net_profit = Decimal('0.00')
        self.roi_average = 0.0

    def add_transaction(self, entry: LedgerEntry):
        """Add transaction to report.
        
        Args:
            entry: LedgerEntry to include in report
        """
        self.transactions.append(entry)

    def calculate_summary(self):
        """Calculate summary statistics from transactions."""
        self.total_spend = sum(t.amount for t in self.transactions)
        self.total_revenue = sum(t.actual_revenue for t in self.transactions)
        self.net_profit = self.total_revenue - self.total_spend
        
        # Calculate average ROI
        if self.transactions:
            roi_sum = sum(t.calculate_roi() for t in self.transactions)
            self.roi_average = roi_sum / len(self.transactions)

    def to_report(self) -> dict:
        """Generate comprehensive P&L report.
        
        Returns:
            Dictionary with summary and transaction details
        """
        return {
            'period': {
                'start': self.period_start.isoformat(),
                'end': self.period_end.isoformat()
            },
            'summary': {
                'transaction_count': len(self.transactions),
                'total_spend': float(self.total_spend),
                'total_revenue': float(self.total_revenue),
                'net_profit': float(self.net_profit),
                'roi_average': self.roi_average
            },
            'transactions': [t.to_pnl_report() for t in self.transactions]
        }


def create_ledger_entry(*args, **kwargs) -> LedgerEntry:
    """Create ledger entry with reasoning context.
    
    Args:
        **kwargs: Transaction parameters including trend context
        
    Returns:
        Initialized LedgerEntry
    """
    return LedgerEntry(**kwargs)