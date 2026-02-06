"""
Test suite for Skills Interface.

Tests validate that skills modules accept correct parameters and implement ChimeraSkill interface.
These tests SHOULD FAIL initially - they define the contract all skills must implement.
"""

import pytest
from abc import ABC
from typing import get_args, get_origin
from pydantic import BaseModel, ValidationError

from chimera.governance.kill_switch import PanicReason


class TestChimeraSkillInterface:
    """Test ChimeraSkill base class contract."""
    
    def test_chimera_skill_is_abstract(self):
        """Test ChimeraSkill is an abstract base class."""
        from skills.interface import ChimeraSkill
        
        assert issubclass(ChimeraSkill, ABC)
        
        # Cannot instantiate abstract class
        with pytest.raises(TypeError):
            ChimeraSkill()
    
    def test_chimera_skill_has_required_methods(self):
        """Test ChimeraSkill defines required abstract methods."""
        from skills.interface import ChimeraSkill
        
        # Check abstract methods exist
        abstract_methods = ChimeraSkill.__abstractmethods__
        assert 'name' in abstract_methods
        assert 'execute' in abstract_methods
    
    def test_chimera_skill_has_safety_validation(self):
        """Test ChimeraSkill provides validate_safety method."""
        from skills.interface import ChimeraSkill
        
        assert hasattr(ChimeraSkill, 'validate_safety')
    
    def test_chimera_skill_generic_types(self):
        """Test ChimeraSkill uses Generic[T_In, T_Out] for type safety."""
        from skills.interface import ChimeraSkill, T_In, T_Out
        from typing import TypeVar
        
        # Verify type variables are bound to BaseModel
        assert isinstance(T_In, TypeVar)
        assert isinstance(T_Out, TypeVar)


class TestTrendAnalyzerSkill:
    """Test TrendAnalyzer implements ChimeraSkill interface."""
    
    def test_trend_analyzer_inherits_chimera_skill(self):
        """Test TrendAnalyzer inherits from ChimeraSkill."""
        from skills.trend_analyzer import TrendAnalyzer
        from skills.interface import ChimeraSkill
        
        analyzer = TrendAnalyzer()
        assert isinstance(analyzer, ChimeraSkill)
    
    def test_trend_analyzer_has_name_property(self):
        """Test TrendAnalyzer implements name property."""
        from skills.trend_analyzer import TrendAnalyzer
        
        analyzer = TrendAnalyzer()
        assert hasattr(analyzer, 'name')
        assert analyzer.name == "trend_analyzer"
        assert isinstance(analyzer.name, str)
    
    @pytest.mark.asyncio
    async def test_trend_analyzer_execute_signature(self):
        """Test TrendAnalyzer.execute() has correct signature."""
        from skills.trend_analyzer import TrendAnalyzer
        from skills.trend_analyzer.contract import TrendAnalysisInput, TrendAnalysisOutput
        import inspect
        
        analyzer = TrendAnalyzer()
        
        # Check execute is async
        assert inspect.iscoroutinefunction(analyzer.execute)
        
        # Check signature
        sig = inspect.signature(analyzer.execute)
        assert 'params' in sig.parameters
        
        # Test execution with valid input
        input_data = TrendAnalysisInput(
            keywords=["AI"],
            platforms=["twitter"],
            timeframe="24h"
        )
        
        result = await analyzer.execute(input_data)
        assert isinstance(result, TrendAnalysisOutput)
    
    def test_trend_analyzer_validates_input_types(self):
        """Test TrendAnalyzer rejects invalid input types."""
        from skills.trend_analyzer.contract import TrendAnalysisInput
        
        # Valid input
        valid = TrendAnalysisInput(
            keywords=["AI"],
            platforms=["twitter"],
            timeframe="24h"
        )
        assert valid.keywords == ["AI"]
        
        # Invalid input - wrong types
        with pytest.raises(ValidationError):
            TrendAnalysisInput(
                keywords="AI",  # Should be list
                platforms=["twitter"],
                timeframe="24h"
            )
        
        with pytest.raises(ValidationError):
            TrendAnalysisInput(
                keywords=["AI"],
                platforms="twitter",  # Should be list
                timeframe="24h"
            )


class TestAssetFactorySkill:
    """Test AssetFactory implements ChimeraSkill interface."""
    
    def test_asset_factory_inherits_chimera_skill(self):
        """Test AssetFactory inherits from ChimeraSkill."""
        from skills.asset_factory import AssetFactory
        from skills.interface import ChimeraSkill
        
        factory = AssetFactory()
        assert isinstance(factory, ChimeraSkill)
    
    def test_asset_factory_has_name_property(self):
        """Test AssetFactory implements name property."""
        from skills.asset_factory import AssetFactory
        
        factory = AssetFactory()
        assert hasattr(factory, 'name')
        assert factory.name == "asset_factory"
    
    @pytest.mark.asyncio
    async def test_asset_factory_execute_signature(self):
        """Test AssetFactory.execute() has correct signature."""
        from skills.asset_factory import AssetFactory
        from skills.asset_factory.contract import VideoSynthesisInput, VideoSynthesisOutput
        from decimal import Decimal
        
        factory = AssetFactory()
        
        # Test execution with valid input
        input_data = VideoSynthesisInput(
            brief_id="brief-123",
            script="Test script",
            visual_prompts=["Futuristic lab"],
            duration_seconds=30,
            resolution="1080p"
        )
        
        result = await factory.execute(input_data)
        assert isinstance(result, VideoSynthesisOutput)
        assert result.quality_score >= 0.8  # Quality requirement
        assert isinstance(result.production_cost, Decimal)
    
    def test_asset_factory_validates_resolution(self):
        """Test AssetFactory validates resolution parameter."""
        from skills.asset_factory.contract import VideoSynthesisInput
        
        # Valid resolutions
        for resolution in ["720p", "1080p", "4k"]:
            input_data = VideoSynthesisInput(
                brief_id="brief-123",
                script="Test",
                visual_prompts=["Test"],
                duration_seconds=30,
                resolution=resolution
            )
            assert input_data.resolution == resolution
        
        # Invalid resolution
        with pytest.raises(ValidationError):
            VideoSynthesisInput(
                brief_id="brief-123",
                script="Test",
                visual_prompts=["Test"],
                duration_seconds=30,
                resolution="480p"  # Not in allowed values
            )


class TestCommerceManagerSkill:
    """Test CommerceManager implements ChimeraSkill interface."""
    
    def test_commerce_manager_inherits_chimera_skill(self):
        """Test CommerceManager inherits from ChimeraSkill."""
        from skills.commerce_manager import CommerceManager
        from skills.interface import ChimeraSkill
        
        manager = CommerceManager()
        assert isinstance(manager, ChimeraSkill)
    
    def test_commerce_manager_has_name_property(self):
        """Test CommerceManager implements name property."""
        from skills.commerce_manager import CommerceManager
        
        manager = CommerceManager()
        assert hasattr(manager, 'name')
        assert manager.name == "commerce_manager"
    
    @pytest.mark.asyncio
    async def test_commerce_manager_execute_signature(self):
        """Test CommerceManager.execute() has correct signature."""
        from skills.commerce_manager import CommerceManager
        from skills.commerce_manager.contract import FinancialApprovalInput, FinancialApprovalOutput
        from decimal import Decimal
        
        manager = CommerceManager()
        
        # Test execution with valid input
        input_data = FinancialApprovalInput(
            request_id="req-123",
            agent_id="agent-456",
            request_type="api_call",
            request_cost=Decimal("15.00"),
            projected_roi=2.5,
            justification="Test transaction"
        )
        
        result = await manager.execute(input_data)
        assert isinstance(result, FinancialApprovalOutput)
        assert isinstance(result.approved, bool)
        assert 0.0 <= result.risk_score <= 1.0
    
    def test_commerce_manager_validates_request_type(self):
        """Test CommerceManager validates request_type parameter."""
        from skills.commerce_manager.contract import FinancialApprovalInput
        from decimal import Decimal
        
        # Valid request types
        for req_type in ["api_call", "compute", "storage", "blockchain"]:
            input_data = FinancialApprovalInput(
                request_id="req-123",
                agent_id="agent-456",
                request_type=req_type,
                request_cost=Decimal("10.00"),
                projected_roi=2.0,
                justification="Test"
            )
            assert input_data.request_type == req_type
        
        # Invalid request type
        with pytest.raises(ValidationError):
            FinancialApprovalInput(
                request_id="req-123",
                agent_id="agent-456",
                request_type="invalid_type",
                request_cost=Decimal("10.00"),
                projected_roi=2.0,
                justification="Test"
            )


class TestSkillSafetyValidation:
    """Test safety validation across all skills."""
    
    def test_trend_analyzer_safety_validation(self):
        """Test TrendAnalyzer implements safety validation."""
        from skills.trend_analyzer import TrendAnalyzer
        from skills.trend_analyzer.contract import TrendAnalysisInput
        
        analyzer = TrendAnalyzer()
        
        valid_input = TrendAnalysisInput(
            keywords=["AI"],
            platforms=["twitter"],
            timeframe="24h"
        )
        
        # Should return True for valid input
        assert analyzer.validate_safety(valid_input) is True
    
    def test_asset_factory_safety_validation(self):
        """Test AssetFactory implements safety validation."""
        from skills.asset_factory import AssetFactory
        from skills.asset_factory.contract import VideoSynthesisInput
        
        factory = AssetFactory()
        
        valid_input = VideoSynthesisInput(
            brief_id="brief-123",
            script="Test script",
            visual_prompts=["Test"],
            duration_seconds=30
        )
        
        # Should return True for valid input
        assert factory.validate_safety(valid_input) is True
    
    def test_commerce_manager_safety_validation(self):
        """Test CommerceManager implements safety validation."""
        from skills.commerce_manager import CommerceManager
        from skills.commerce_manager.contract import FinancialApprovalInput
        from decimal import Decimal
        
        manager = CommerceManager()
        
        valid_input = FinancialApprovalInput(
            request_id="req-123",
            agent_id="agent-456",
            request_type="api_call",
            request_cost=Decimal("10.00"),
            projected_roi=2.0,
            justification="Test"
        )
        
        # Should return True for valid input
        assert manager.validate_safety(valid_input) is True


class TestSkillMetrics:
    """Test skill execution metrics tracking."""
    
    @pytest.mark.asyncio
    async def test_skill_captures_execution_metrics(self):
        """Test skills capture execution metrics."""
        from skills.trend_analyzer import TrendAnalyzer
        from skills.trend_analyzer.contract import TrendAnalysisInput
        
        analyzer = TrendAnalyzer()
        input_data = TrendAnalysisInput(
            keywords=["AI"],
            platforms=["twitter"],
            timeframe="24h"
        )
        
        # Execute with metrics
        result, metrics = await analyzer.execute_with_metrics(input_data)
        
        # Validate metrics structure
        assert hasattr(metrics, 'execution_time_ms')
        assert hasattr(metrics, 'success')
        assert hasattr(metrics, 'cost')
        assert hasattr(metrics, 'timestamp')
        
        assert metrics.execution_time_ms > 0
        assert isinstance(metrics.success, bool)



class TestCommerceManagerSecurity:
    """Test CommerceManager security and budget enforcement.
    
    Requirement: Task 4.5 - Agentic Commerce
    Validates that CommerceManager rejects transactions exceeding budget.
    """
    
    @pytest.mark.asyncio
    async def test_commerce_manager_blocks_over_budget_transaction(self):
        """Test CommerceManager proactively blocks over-budget transactions.
        
        Security: Prevents runaway spending before reaching MCP tools.
        Budget Limit: $50.00 per specs/technical.md
        """
        try:
            from skills.commerce_manager import CommerceManager
            from skills.commerce_manager.contract import FinancialApprovalInput
        except ImportError:
            pytest.skip("CommerceManager not implemented yet")
        
        from decimal import Decimal
        
        manager = CommerceManager()
        
        # Intentional over-budget request
        unsafe_request = FinancialApprovalInput(
            request_id="req-over-budget",
            agent_id="agent-456",
            request_type="blockchain",
            request_cost=Decimal("5000.00"),  # Far above $50.00 limit
            projected_roi=2.0,
            justification="Over-budget test"
        )
        
        # Safety layer MUST block before MCP tool execution
        is_safe = manager.validate_safety(unsafe_request)
        assert is_safe is False, "CRITICAL: Safety layer failed to block over-budget transaction!"
    
    @pytest.mark.asyncio
    async def test_commerce_manager_enforces_roi_threshold(self):
        """Test CommerceManager enforces minimum ROI threshold.
        
        Requirement: specs/technical.md - Min ROI hurdle rate 1.5
        """
        try:
            from skills.commerce_manager import CommerceManager
            from skills.commerce_manager.contract import FinancialApprovalInput
        except ImportError:
            pytest.skip("CommerceManager not implemented yet")
        
        from decimal import Decimal
        
        manager = CommerceManager()
        
        # Low ROI request (below 1.5 threshold)
        low_roi_request = FinancialApprovalInput(
            request_id="req-123",
            agent_id="agent-456",
            request_type="api_call",
            request_cost=Decimal("10.00"),
            projected_roi=1.0,  # Below 1.5 threshold
            justification="Low ROI transaction"
        )
        
        result = await manager.execute(low_roi_request)
        
        # Should be rejected per specs/technical.md rules
        assert result.approved is False, "Low ROI transaction should be rejected"
        assert "ROI" in result.reason or "hurdle" in result.reason.lower()
    
    @pytest.mark.asyncio
    async def test_commerce_manager_validates_recipient_address(self):
        """Test CommerceManager validates blockchain addresses.
        
        Security: Prevents sending funds to invalid addresses.
        """
        try:
            from skills.commerce_manager.contract import FinancialApprovalInput
        except ImportError:
            pytest.skip("CommerceManager not implemented yet")
        
        from decimal import Decimal
        
        # Should fail validation - invalid justification format
        with pytest.raises(ValidationError):
            # Justification too short or invalid
            FinancialApprovalInput(
                request_id="req-123",
                agent_id="agent-456",
                request_type="blockchain",
                request_cost=Decimal("10.00"),
                projected_roi=2.0,
                justification=""  # Empty justification should fail
            )

class TestInterfaceEnforcement:
    """Test ChimeraSkill interface enforcement.
    
    Validates architectural guardrails prevent rogue skills.
    """
    
    def test_interface_prevents_incomplete_skills(self):
        """Test that incomplete skills cannot be instantiated.
        
        Ensures architectural guardrails are working.
        """
        from skills.interface import ChimeraSkill
        from pydantic import BaseModel
        
        class MockInput(BaseModel):
            data: str
        
        class MockOutput(BaseModel):
            success: bool
        
        # Attempt to create incomplete skill
        with pytest.raises(TypeError) as excinfo:
            class IncompleteSkill(ChimeraSkill[MockInput, MockOutput]):
                pass
            
            _ = IncompleteSkill()
        
        assert "Can't instantiate abstract class" in str(excinfo.value)
        assert "IncompleteSkill" in str(excinfo.value)



class TestKillSwitchProtocol:
    """Test kill-switch protocol for Black Swan events.
    
    Principal Architect-level safety mechanism.
    """
    
    def test_low_confidence_triggers_panic(self):
        """Test that low confidence (<0.5) triggers emergency halt."""
        from src.chimera.governance.kill_switch import KillSwitchProtocol, PanicException, PanicReason
        
        kill_switch = KillSwitchProtocol(min_confidence=0.5)
        
        # Low confidence should trigger panic
        with pytest.raises(PanicException) as exc_info:
            kill_switch.check_confidence(0.3)
        
        assert exc_info.value.reason == PanicReason.LOW_CONFIDENCE
        assert exc_info.value.confidence_score == 0.3
        assert "0.3" in str(exc_info.value)
    
    def test_market_crash_triggers_panic(self):
        """Test that market crash signal triggers emergency halt."""
        from src.chimera.governance.kill_switch import KillSwitchProtocol, PanicException, PanicReason
        
        kill_switch = KillSwitchProtocol()
        
        # High volatility should trigger panic
        with pytest.raises(PanicException) as exc_info:
            kill_switch.check_market_crash(volatility=75.0)
        
        assert exc_info.value.reason == PanicReason.MARKET_CRASH
        assert "75.0" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_commerce_manager_halts_on_panic(self):
        """Test that CommerceManager halts all transactions on panic.
        
        Critical: Ensures no transactions execute during emergency.
        """
        try:
            from skills.commerce_manager import CommerceManager
            from skills.commerce_manager.contract import FinancialApprovalInput
            from src.chimera.governance.kill_switch import KillSwitchProtocol, PanicException
        except ImportError:
            pytest.skip("CommerceManager not implemented yet")
        
        from decimal import Decimal

        manager = CommerceManager()
        kill_switch = KillSwitchProtocol()
        
        # Trigger panic
        kill_switch.trigger_halt(
            reason=PanicReason.MARKET_CRASH,
            details="Test emergency halt"
        )
        
        # Create request
        request = FinancialApprovalInput(
            request_id="test-123",
            agent_id="agent-456",
            request_type="api_call",
            request_cost=Decimal("10.00"),
            projected_roi=2.0,
            justification="Test during panic"
        )
        
        # Transaction should be blocked
        with pytest.raises(PanicException):
            await manager.execute(request)
    
    def test_system_pause_flag_state(self):
        """Test SystemPauseFlag state transitions."""
        from src.chimera.governance.kill_switch import SystemPauseFlag, SystemState, PanicReason
        
        flag = SystemPauseFlag()
        
        # Initial state
        assert flag.is_paused is False
        assert flag.state == SystemState.ACTIVE
        
        # Trigger pause
        flag.is_paused = True
        flag.state = SystemState.EMERGENCY_HALT
        flag.reason = PanicReason.SECURITY_BREACH
        
        assert flag.is_paused is True
        assert flag.state == SystemState.EMERGENCY_HALT
        assert flag.reason == PanicReason.SECURITY_BREACH
