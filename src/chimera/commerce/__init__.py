"""
Agentic Commerce System for Project Chimera.

This module implements economic sovereignty for AI agents through blockchain
integration, autonomous transactions, and CFO-level financial intelligence.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import asyncio
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TransactionStatus(Enum):
    """Transaction status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTED = "executed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RiskLevel(Enum):
    """Risk assessment levels."""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class Transaction:
    """Transaction representation."""
    id: str
    agent_id: str
    amount: Decimal
    recipient: str
    purpose: str
    timestamp: datetime
    status: TransactionStatus
    risk_level: RiskLevel
    metadata: Dict[str, Any]


@dataclass
class Budget:
    """Budget allocation for agents."""
    agent_id: str
    total_allocation: Decimal
    spent: Decimal
    remaining: Decimal
    period_start: datetime
    period_end: datetime
    categories: Dict[str, Decimal]


class AutonomousWallet:
    """
    Autonomous wallet for AI agents with blockchain integration.
    
    Provides secure, autonomous transaction capabilities with built-in
    risk management and compliance features.
    """
    
    def __init__(self, agent_id: str, initial_balance: Decimal = Decimal('0')):
        self.agent_id = agent_id
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
        self.locked_funds: Decimal = Decimal('0')
        
        logger.info(f"AutonomousWallet created for agent {agent_id}")
    
    async def get_balance(self) -> Decimal:
        """Get current wallet balance."""
        return self.balance - self.locked_funds
    
    async def lock_funds(self, amount: Decimal, purpose: str) -> bool:
        """Lock funds for a pending transaction."""
        available = await self.get_balance()
        if amount <= available:
            self.locked_funds += amount
            logger.info(f"Locked {amount} for {purpose}")
            return True
        return False
    
    async def unlock_funds(self, amount: Decimal) -> None:
        """Unlock previously locked funds."""
        self.locked_funds = max(Decimal('0'), self.locked_funds - amount)
    
    async def execute_transaction(self, transaction: Transaction) -> bool:
        """Execute a transaction."""
        try:
            # Simulate blockchain transaction
            await asyncio.sleep(0.1)
            
            if transaction.amount <= await self.get_balance():
                self.balance -= transaction.amount
                transaction.status = TransactionStatus.EXECUTED
                self.transactions.append(transaction)
                
                logger.info(f"Transaction {transaction.id} executed: {transaction.amount} to {transaction.recipient}")
                return True
            else:
                transaction.status = TransactionStatus.FAILED
                logger.warning(f"Transaction {transaction.id} failed: insufficient funds")
                return False
                
        except Exception as e:
            transaction.status = TransactionStatus.FAILED
            logger.error(f"Transaction {transaction.id} failed: {e}")
            return False
    
    async def get_transaction_history(self, days: int = 30) -> List[Transaction]:
        """Get transaction history for the specified period."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return [t for t in self.transactions if t.timestamp >= cutoff_date]


class CFOAgent:
    """
    Chief Financial Officer AI agent for financial decision making.
    
    Provides sophisticated financial analysis, risk assessment, and
    budget management for autonomous agents.
    """
    
    def __init__(self, risk_tolerance: str = "CONSERVATIVE"):
        self.risk_tolerance = risk_tolerance
        self.budget_limits = {
            "daily": Decimal('1000'),
            "weekly": Decimal('5000'),
            "monthly": Decimal('20000')
        }
        self.category_limits = {
            "compute": Decimal('500'),
            "storage": Decimal('200'),
            "api_calls": Decimal('300'),
            "marketing": Decimal('1000'),
            "research": Decimal('500')
        }
        
        logger.info(f"CFOAgent initialized with {risk_tolerance} risk tolerance")
    
    async def analyze_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a financial opportunity and calculate ROI."""
        cost = Decimal(str(opportunity.get("cost", 0)))
        expected_revenue = Decimal(str(opportunity.get("expected_revenue", 0)))
        duration_days = opportunity.get("duration_days", 30)
        
        # Calculate ROI metrics
        roi = ((expected_revenue - cost) / cost * 100) if cost > 0 else Decimal('0')
        daily_roi = roi / duration_days if duration_days > 0 else Decimal('0')
        
        # Risk assessment based on various factors
        risk_factors = {
            "market_volatility": opportunity.get("market_risk", 0.1),
            "execution_complexity": opportunity.get("complexity", 0.2),
            "time_sensitivity": opportunity.get("urgency", 0.1),
            "resource_requirements": min(float(cost) / 10000, 1.0)
        }
        
        overall_risk = sum(risk_factors.values()) / len(risk_factors)
        risk_level = self._calculate_risk_level(overall_risk)
        
        return {
            "cost": cost,
            "expected_revenue": expected_revenue,
            "roi_percentage": roi,
            "daily_roi": daily_roi,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendation": self._make_recommendation(roi, risk_level),
            "confidence": self._calculate_confidence(roi, risk_level)
        }
    
    async def evaluate_risk(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate risk for a financial opportunity."""
        analysis = await self.analyze_opportunity(opportunity)
        
        risk_assessment = {
            "risk_level": analysis["risk_level"],
            "risk_score": sum(analysis["risk_factors"].values()),
            "mitigation_strategies": self._suggest_mitigations(analysis["risk_factors"]),
            "approval_required": analysis["risk_level"] in [RiskLevel.HIGH, RiskLevel.VERY_HIGH],
            "max_exposure": self._calculate_max_exposure(analysis["risk_level"])
        }
        
        return risk_assessment
    
    async def review_transaction(self, amount: Decimal, recipient: str, purpose: str) -> Dict[str, Any]:
        """Review a transaction for approval."""
        # Simulate transaction analysis
        risk_score = min(float(amount) / 1000, 1.0)  # Higher amounts = higher risk
        
        # Check against budget limits
        within_budget = amount <= self.budget_limits.get("daily", Decimal('1000'))
        
        # Category-based approval
        category = self._categorize_transaction(purpose)
        within_category_limit = amount <= self.category_limits.get(category, Decimal('100'))
        
        approved = within_budget and within_category_limit and risk_score < 0.8
        
        return {
            "approved": approved,
            "amount": amount,
            "recipient": recipient,
            "purpose": purpose,
            "category": category,
            "risk_score": risk_score,
            "within_budget": within_budget,
            "within_category_limit": within_category_limit,
            "reason": self._get_approval_reason(approved, within_budget, within_category_limit, risk_score)
        }
    
    def _calculate_risk_level(self, risk_score: float) -> RiskLevel:
        """Calculate risk level from risk score."""
        if risk_score < 0.2:
            return RiskLevel.VERY_LOW
        elif risk_score < 0.4:
            return RiskLevel.LOW
        elif risk_score < 0.6:
            return RiskLevel.MEDIUM
        elif risk_score < 0.8:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH
    
    def _make_recommendation(self, roi: Decimal, risk_level: RiskLevel) -> str:
        """Make investment recommendation based on ROI and risk."""
        if roi > 50 and risk_level in [RiskLevel.VERY_LOW, RiskLevel.LOW]:
            return "STRONG_BUY"
        elif roi > 20 and risk_level in [RiskLevel.VERY_LOW, RiskLevel.LOW, RiskLevel.MEDIUM]:
            return "BUY"
        elif roi > 10 and risk_level in [RiskLevel.VERY_LOW, RiskLevel.LOW]:
            return "HOLD"
        else:
            return "AVOID"
    
    def _calculate_confidence(self, roi: Decimal, risk_level: RiskLevel) -> float:
        """Calculate confidence in the analysis."""
        base_confidence = 0.7
        
        # Adjust based on ROI clarity
        if roi > 30:
            base_confidence += 0.2
        elif roi < 5:
            base_confidence -= 0.2
        
        # Adjust based on risk level
        risk_adjustments = {
            RiskLevel.VERY_LOW: 0.2,
            RiskLevel.LOW: 0.1,
            RiskLevel.MEDIUM: 0.0,
            RiskLevel.HIGH: -0.1,
            RiskLevel.VERY_HIGH: -0.2
        }
        
        base_confidence += risk_adjustments.get(risk_level, 0)
        return max(0.1, min(0.95, base_confidence))
    
    def _suggest_mitigations(self, risk_factors: Dict[str, float]) -> List[str]:
        """Suggest risk mitigation strategies."""
        mitigations = []
        
        if risk_factors.get("market_volatility", 0) > 0.3:
            mitigations.append("Consider hedging strategies")
        
        if risk_factors.get("execution_complexity", 0) > 0.4:
            mitigations.append("Break down into smaller phases")
        
        if risk_factors.get("time_sensitivity", 0) > 0.3:
            mitigations.append("Establish clear deadlines and milestones")
        
        if risk_factors.get("resource_requirements", 0) > 0.5:
            mitigations.append("Secure additional resources or reduce scope")
        
        return mitigations
    
    def _calculate_max_exposure(self, risk_level: RiskLevel) -> Decimal:
        """Calculate maximum exposure based on risk level."""
        exposure_limits = {
            RiskLevel.VERY_LOW: Decimal('10000'),
            RiskLevel.LOW: Decimal('5000'),
            RiskLevel.MEDIUM: Decimal('2000'),
            RiskLevel.HIGH: Decimal('500'),
            RiskLevel.VERY_HIGH: Decimal('100')
        }
        
        return exposure_limits.get(risk_level, Decimal('100'))
    
    def _categorize_transaction(self, purpose: str) -> str:
        """Categorize transaction based on purpose."""
        purpose_lower = purpose.lower()
        
        if any(word in purpose_lower for word in ["compute", "cpu", "gpu", "processing"]):
            return "compute"
        elif any(word in purpose_lower for word in ["storage", "database", "backup"]):
            return "storage"
        elif any(word in purpose_lower for word in ["api", "service", "integration"]):
            return "api_calls"
        elif any(word in purpose_lower for word in ["marketing", "advertising", "promotion"]):
            return "marketing"
        elif any(word in purpose_lower for word in ["research", "analysis", "study"]):
            return "research"
        else:
            return "other"
    
    def _get_approval_reason(self, approved: bool, within_budget: bool, 
                           within_category_limit: bool, risk_score: float) -> str:
        """Get reason for approval or rejection."""
        if approved:
            return "Transaction approved within all limits"
        
        reasons = []
        if not within_budget:
            reasons.append("exceeds daily budget limit")
        if not within_category_limit:
            reasons.append("exceeds category limit")
        if risk_score >= 0.8:
            reasons.append("risk score too high")
        
        return f"Transaction rejected: {', '.join(reasons)}"


class AgenticCommerce:
    """
    Main agentic commerce system that orchestrates economic activities.
    
    This class integrates autonomous wallets, CFO intelligence, and blockchain
    transactions to enable true economic sovereignty for AI agents.
    """
    
    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.config = config or {}
        
        # Initialize components
        self.wallet = AutonomousWallet(agent_id)
        self.cfo_agent = CFOAgent(risk_tolerance=config.get("risk_tolerance", "CONSERVATIVE"))
        
        # Budget management
        self.budget = Budget(
            agent_id=agent_id,
            total_allocation=Decimal(str(config.get("budget", 10000))),
            spent=Decimal('0'),
            remaining=Decimal(str(config.get("budget", 10000))),
            period_start=datetime.utcnow(),
            period_end=datetime.utcnow() + timedelta(days=30),
            categories={}
        )
        
        logger.info(f"AgenticCommerce initialized for agent {agent_id}")
    
    async def make_economic_decision(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Make an economic decision about an opportunity."""
        # Analyze the opportunity
        roi_analysis = await self.cfo_agent.analyze_opportunity(opportunity)
        risk_assessment = await self.cfo_agent.evaluate_risk(opportunity)
        
        # Check budget constraints
        cost = Decimal(str(opportunity.get("cost", 0)))
        can_afford = cost <= self.budget.remaining
        
        # Make decision
        should_proceed = (
            roi_analysis["recommendation"] in ["STRONG_BUY", "BUY"] and
            risk_assessment["risk_level"] in [RiskLevel.VERY_LOW, RiskLevel.LOW, RiskLevel.MEDIUM] and
            can_afford and
            roi_analysis["confidence"] > 0.6
        )
        
        decision = {
            "opportunity_id": opportunity.get("id", "unknown"),
            "decision": "PROCEED" if should_proceed else "DECLINE",
            "roi_analysis": roi_analysis,
            "risk_assessment": risk_assessment,
            "budget_check": {
                "cost": cost,
                "remaining_budget": self.budget.remaining,
                "can_afford": can_afford
            },
            "confidence": roi_analysis["confidence"],
            "reasoning": self._generate_reasoning(should_proceed, roi_analysis, risk_assessment, can_afford)
        }
        
        return decision
    
    async def execute_transaction(self, amount: Decimal, recipient: str, purpose: str) -> Dict[str, Any]:
        """Execute a financial transaction with CFO approval."""
        # Get CFO approval
        approval = await self.cfo_agent.review_transaction(amount, recipient, purpose)
        
        if not approval["approved"]:
            return {
                "success": False,
                "transaction_id": None,
                "reason": approval["reason"],
                "approval_details": approval
            }
        
        # Create transaction
        transaction = Transaction(
            id=f"tx_{int(time.time())}_{self.agent_id[:8]}",
            agent_id=self.agent_id,
            amount=amount,
            recipient=recipient,
            purpose=purpose,
            timestamp=datetime.utcnow(),
            status=TransactionStatus.PENDING,
            risk_level=self.cfo_agent._calculate_risk_level(approval["risk_score"]),
            metadata={"approval": approval}
        )
        
        # Execute transaction
        success = await self.wallet.execute_transaction(transaction)
        
        if success:
            # Update budget
            self.budget.spent += amount
            self.budget.remaining -= amount
            
            # Update category spending
            category = approval["category"]
            if category not in self.budget.categories:
                self.budget.categories[category] = Decimal('0')
            self.budget.categories[category] += amount
        
        return {
            "success": success,
            "transaction_id": transaction.id,
            "amount": amount,
            "recipient": recipient,
            "purpose": purpose,
            "approval_details": approval,
            "new_balance": await self.wallet.get_balance()
        }
    
    async def get_financial_status(self) -> Dict[str, Any]:
        """Get comprehensive financial status."""
        balance = await self.wallet.get_balance()
        recent_transactions = await self.wallet.get_transaction_history(days=7)
        
        return {
            "agent_id": self.agent_id,
            "wallet_balance": balance,
            "locked_funds": self.wallet.locked_funds,
            "budget": {
                "total_allocation": self.budget.total_allocation,
                "spent": self.budget.spent,
                "remaining": self.budget.remaining,
                "utilization_rate": float(self.budget.spent / self.budget.total_allocation * 100)
            },
            "recent_activity": {
                "transactions_7d": len(recent_transactions),
                "total_spent_7d": sum(t.amount for t in recent_transactions),
                "avg_transaction": sum(t.amount for t in recent_transactions) / len(recent_transactions) if recent_transactions else Decimal('0')
            },
            "category_spending": dict(self.budget.categories)
        }
    
    def _generate_reasoning(self, should_proceed: bool, roi_analysis: Dict[str, Any], 
                          risk_assessment: Dict[str, Any], can_afford: bool) -> str:
        """Generate human-readable reasoning for the decision."""
        if should_proceed:
            return f"Proceeding with opportunity: ROI of {roi_analysis['roi_percentage']:.1f}% with {risk_assessment['risk_level'].value} risk level and {roi_analysis['confidence']:.0%} confidence"
        else:
            reasons = []
            if roi_analysis["recommendation"] not in ["STRONG_BUY", "BUY"]:
                reasons.append(f"poor ROI ({roi_analysis['roi_percentage']:.1f}%)")
            if risk_assessment["risk_level"] in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]:
                reasons.append(f"high risk ({risk_assessment['risk_level'].value})")
            if not can_afford:
                reasons.append("insufficient budget")
            if roi_analysis["confidence"] <= 0.6:
                reasons.append(f"low confidence ({roi_analysis['confidence']:.0%})")
            
            return f"Declining opportunity due to: {', '.join(reasons)}"