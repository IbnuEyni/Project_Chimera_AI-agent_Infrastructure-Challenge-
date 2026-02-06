"""
Optimistic Concurrency Control (OCC) Tests

Tests for race conditions and version conflicts per SRS Section 3.1.3.
Prevents "Ghost Updates" where two agents act on stale data.
"""

import pytest
import asyncio
from typing import Optional
from pydantic import BaseModel, Field


class VersionConflictError(Exception):
    """Raised when optimistic concurrency check fails."""
    
    def __init__(self, resource_id: str, expected_version: int, actual_version: int):
        self.resource_id = resource_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Version conflict on {resource_id}: expected v{expected_version}, got v{actual_version}"
        )


class InfluencerState(BaseModel):
    """Influencer state with version tracking for OCC."""
    
    id: str
    version: int = Field(default=1, description="Version for optimistic locking")
    current_trend: Optional[str] = None
    last_post_time: Optional[str] = None
    engagement_score: float = 0.0


class TestOptimisticConcurrencyControl:
    """Test OCC to prevent ghost updates."""
    
    @pytest.mark.asyncio
    async def test_concurrent_update_race_condition(self):
        """Test that concurrent updates trigger VersionConflictError.
        
        Scenario: Two Planner agents try to update influencer_state simultaneously.
        Expected: Second update fails with VersionConflictError.
        """
        # Simulate shared state
        state = InfluencerState(
            id="influencer-1",
            version=1,
            current_trend="AI Regulation"
        )
        
        async def update_state(agent_id: str, new_trend: str, expected_version: int):
            """Simulate agent updating state."""
            await asyncio.sleep(0.01)  # Simulate processing
            
            # Check version (OCC)
            if state.version != expected_version:
                raise VersionConflictError(
                    resource_id=state.id,
                    expected_version=expected_version,
                    actual_version=state.version
                )
            
            # Update state
            state.current_trend = new_trend
            state.version += 1
            return state.version
        
        # Agent 1 reads state (version=1)
        agent1_version = state.version
        
        # Agent 2 reads state (version=1) - same version!
        agent2_version = state.version
        
        # Agent 1 updates successfully
        new_version = await update_state("agent-1", "Crypto Trends", agent1_version)
        assert new_version == 2
        assert state.current_trend == "Crypto Trends"
        
        # Agent 2 tries to update with stale version - should fail
        with pytest.raises(VersionConflictError) as exc_info:
            await update_state("agent-2", "Tech News", agent2_version)
        
        assert exc_info.value.expected_version == 1
        assert exc_info.value.actual_version == 2
        assert "Version conflict" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_sequential_updates_succeed(self):
        """Test that sequential updates with correct versions succeed."""
        state = InfluencerState(id="influencer-2", version=1)
        
        # Update 1
        state.current_trend = "AI"
        state.version += 1
        assert state.version == 2
        
        # Update 2 with correct version
        state.current_trend = "Blockchain"
        state.version += 1
        assert state.version == 3
    
    @pytest.mark.asyncio
    async def test_retry_on_version_conflict(self):
        """Test retry logic after version conflict."""
        state = InfluencerState(id="influencer-3", version=1)
        
        async def update_with_retry(new_trend: str, max_retries: int = 3):
            """Update with automatic retry on conflict."""
            for attempt in range(max_retries):
                try:
                    current_version = state.version
                    
                    # Simulate another agent updating
                    if attempt == 0:
                        state.version += 1  # Simulate concurrent update
                    
                    # Check version
                    if state.version != current_version:
                        raise VersionConflictError(
                            state.id, current_version, state.version
                        )
                    
                    # Update
                    state.current_trend = new_trend
                    state.version += 1
                    return state.version
                    
                except VersionConflictError:
                    if attempt == max_retries - 1:
                        raise
                    await asyncio.sleep(0.01)  # Brief delay before retry
        
        # Should succeed after retry
        final_version = await update_with_retry("New Trend")
        assert final_version >= 2
