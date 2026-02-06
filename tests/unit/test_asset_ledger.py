"""
Tests for Asset Ledger and P&L Auto-Reporting

Validates reasoning hash and explainable P&L.
"""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta


class TestAssetLedger:
    """Test AssetLedger with reasoning hash."""
    
    def test_reasoning_hash_generation(self):
        """Test that reasoning hash is generated correctly."""
        from skills.commerce_manager.asset_ledger import ReasoningContext
        
        reasoning = ReasoningContext(
            trend_id="trend-123",
            trend_topic="AI Regulation",
            projected_roi=2.5,
            confidence_score=0.92,
            justification="High engagement trend",
            agent_id="agent-456"
        )
        
        hash1 = reasoning.to_hash()
        hash2 = reasoning.to_hash()
        
        # Same context should produce same hash
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex length
    
    def test_reasoning_hash_changes_with_context(self):
        """Test that different contexts produce different hashes."""
        from skills.commerce_manager.asset_ledger import ReasoningContext
        
        reasoning1 = ReasoningContext(
            trend_id="trend-123",
            trend_topic="AI",
            projected_roi=2.5,
            confidence_score=0.92,
            justification="Test",
            agent_id="agent-1"
        )
        
        reasoning2 = ReasoningContext(
            trend_id="trend-456",  # Different trend
            trend_topic="AI",
            projected_roi=2.5,
            confidence_score=0.92,
            justification="Test",
            agent_id="agent-1"
        )
        
        assert reasoning1.to_hash() != reasoning2.to_hash()
    
    def test_asset_ledger_links_transaction_to_trend(self):
        """Test that AssetLedger links transaction to justifying trend."""
        from skills.commerce_manager.asset_ledger import create_ledger_entry
        
        entry = create_ledger_entry(
            tx_id="tx-789",
            agent_id="agent-123",
            amount=Decimal("15.00"),
            trend_id="trend-abc",
            trend_topic="Crypto Adoption",
            projected_roi=3.0,
            confidence=0.95,
            justification="Viral trend with high engagement potential"
        )
        
        # Verify linkage
        assert entry.reasoning_context.trend_id == "trend-abc"
        assert entry.reasoning_context.trend_topic == "Crypto Adoption"
        assert entry.reasoning_context.projected_roi == 3.0
        assert entry.amount == Decimal("15.00")
        
        # Verify reasoning hash
        assert entry.verify_reasoning_hash() is True
    
    def test_asset_ledger_calculates_roi(self):
        """Test ROI calculation from actual revenue."""
        from skills.commerce_manager.asset_ledger import create_ledger_entry
        
        entry = create_ledger_entry(
            tx_id="tx-001",
            agent_id="agent-001",
            amount=Decimal("10.00"),
            trend_id="trend-001",
            trend_topic="Test",
            projected_roi=2.0,
            confidence=0.9,
            justification="Test"
        )
        
        # Set actual revenue
        entry.actual_revenue = Decimal("25.00")
        
        # Calculate ROI: (25 - 10) / 10 = 1.5 (150%)
        roi = entry.calculate_roi()
        assert roi == 1.5
    
    def test_pnl_report_generation(self):
        """Test P&L report generation with multiple transactions."""
        from skills.commerce_manager.asset_ledger import PLReport, create_ledger_entry
        
        report = PLReport(
            period_start=datetime.utcnow() - timedelta(days=7),
            period_end=datetime.utcnow()
        )
        
        # Add transactions
        entry1 = create_ledger_entry(
            tx_id="tx-001",
            agent_id="agent-001",
            amount=Decimal("10.00"),
            trend_id="trend-001",
            trend_topic="AI Trends",
            projected_roi=2.0,
            confidence=0.9,
            justification="High engagement"
        )
        entry1.actual_revenue = Decimal("25.00")
        
        entry2 = create_ledger_entry(
            tx_id="tx-002",
            agent_id="agent-002",
            amount=Decimal("15.00"),
            trend_id="trend-002",
            trend_topic="Crypto News",
            projected_roi=1.8,
            confidence=0.85,
            justification="Viral potential"
        )
        entry2.actual_revenue = Decimal("30.00")
        
        report.add_transaction(entry1)
        report.add_transaction(entry2)
        report.calculate_summary()
        
        # Verify calculations
        assert report.total_spend == Decimal("25.00")
        assert report.total_revenue == Decimal("55.00")
        assert report.net_profit == Decimal("30.00")
        assert report.roi_average > 0
        
        # Generate report
        report_dict = report.to_report()
        assert report_dict["summary"]["transaction_count"] == 2
        assert report_dict["summary"]["net_profit"] == 30.0
    
    def test_explainable_pnl_includes_justification(self):
        """Test that P&L report includes full justification."""
        from skills.commerce_manager.asset_ledger import create_ledger_entry
        
        entry = create_ledger_entry(
            tx_id="tx-003",
            agent_id="agent-003",
            amount=Decimal("20.00"),
            trend_id="trend-003",
            trend_topic="Tech Innovation",
            projected_roi=2.5,
            confidence=0.92,
            justification="Trending topic with 15K volume, sentiment 0.85"
        )
        
        pnl_entry = entry.to_pnl_report()
        
        # Verify explainability
        assert "justification" in pnl_entry
        assert "Trending topic" in pnl_entry["justification"]
        assert "trend" in pnl_entry
        assert pnl_entry["trend"] == "Tech Innovation"
        assert "reasoning_hash" in pnl_entry
        assert len(pnl_entry["reasoning_hash"]) == 64
