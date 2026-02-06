"""
Chimera Skill Interface - Base class for all autonomous skills.

This module defines the abstract base class that all Chimera skills must implement,
ensuring strict typing, safety validation, and consistent execution patterns.
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from datetime import datetime
from decimal import Decimal


# Generic type variables for strict input/output enforcement
T_In = TypeVar("T_In", bound=BaseModel)
T_Out = TypeVar("T_Out", bound=BaseModel)


class SkillMetrics(BaseModel):
    """Execution metrics for skill monitoring."""
    
    execution_time_ms: int
    success: bool
    error_message: Optional[str] = None
    cost: Decimal = Decimal("0.00")
    timestamp: datetime


class ChimeraSkill(ABC, Generic[T_In, T_Out]):
    """
    Base class for all autonomous skills in Project Chimera.
    
    Forces strict typing and safety validation for reliable swarm operations.
    All skills must implement:
    - name: Unique skill identifier
    - execute: Core skill logic with MCP tool integration
    - validate_safety: Pre-execution safety checks
    
    Example:
        ```python
        class TrendAnalyzer(ChimeraSkill[TrendAnalyzerInput, TrendAnalyzerOutput]):
            @property
            def name(self) -> str:
                return "trend_analyzer"
            
            async def execute(self, params: TrendAnalyzerInput) -> TrendAnalyzerOutput:
                if not self.validate_safety(params):
                    raise SecurityError("Safety validation failed")
                
                # Skill logic here
                return TrendAnalyzerOutput(...)
        ```
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique skill identifier.
        
        Returns:
            str: Skill name (e.g., "trend_analyzer", "asset_factory")
        """
        pass

    @abstractmethod
    async def execute(self, params: T_In) -> T_Out:
        """
        Execute the skill's core logic.
        
        This method must:
        1. Validate safety via validate_safety()
        2. Interact with MCP tools as needed
        3. Return structured output matching T_Out schema
        4. Handle errors gracefully
        
        Args:
            params: Validated input parameters (Pydantic model)
        
        Returns:
            T_Out: Structured output (Pydantic model)
        
        Raises:
            SkillError: Base exception for skill-specific errors
            SecurityError: When safety validation fails
            TimeoutError: When execution exceeds SLA
        """
        pass

    def validate_safety(self, params: T_In) -> bool:
        """
        Pre-execution safety check (Governance Layer).
        
        Override this method to implement skill-specific safety validations:
        - Whitelist external resources
        - Validate input ranges
        - Check rate limits
        - Verify permissions
        
        Args:
            params: Input parameters to validate
        
        Returns:
            bool: True if safe to execute, False otherwise
        """
        return True
    
    async def execute_with_metrics(self, params: T_In) -> tuple[T_Out, SkillMetrics]:
        """
        Execute skill and capture metrics.
        
        This wrapper method:
        1. Records start time
        2. Executes skill logic
        3. Captures execution metrics
        4. Returns both result and metrics
        
        Args:
            params: Validated input parameters
        
        Returns:
            tuple: (skill_output, execution_metrics)
        """
        from time import time
        
        start_time = time()
        success = False
        error_message = None
        result = None
        
        try:
            result = await self.execute(params)
            success = True
        except Exception as e:
            error_message = str(e)
            raise
        finally:
            execution_time_ms = int((time() - start_time) * 1000)
            
            metrics = SkillMetrics(
                execution_time_ms=execution_time_ms,
                success=success,
                error_message=error_message,
                cost=getattr(result, "production_cost", Decimal("0.00")) if result else Decimal("0.00"),
                timestamp=datetime.utcnow()
            )
        
        return result, metrics


class SkillError(Exception):
    """Base exception for skill errors."""
    pass


class SecurityError(SkillError):
    """Raised when safety validation fails."""
    pass


class SkillTimeoutError(SkillError):
    """Raised when skill execution exceeds timeout."""
    pass


class SkillValidationError(SkillError):
    """Raised when input validation fails."""
    pass
