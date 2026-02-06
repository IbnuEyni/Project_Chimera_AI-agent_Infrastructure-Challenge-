"""Commerce Manager logic - TDD Implementation."""
from .contract import FinancialApprovalInput, FinancialApprovalOutput


class CommerceManager:
    """TDD: Minimal implementation to make tests fail meaningfully."""
    
    async def approve_transaction(self, request: FinancialApprovalInput) -> FinancialApprovalOutput:
        """Approve transaction - NOT IMPLEMENTED YET."""
        raise NotImplementedError("TDD: Finance approval not implemented")