"""Commerce Manager logic - TDD Implementation."""
from .contract import CommerceRequest, CommerceResponse


class CommerceManager:
    """TDD: Minimal implementation to make tests fail meaningfully."""
    
    async def approve_transaction(self, request: CommerceRequest) -> CommerceResponse:
        """Approve transaction - NOT IMPLEMENTED YET."""
        raise NotImplementedError("TDD: Commerce approval not implemented")