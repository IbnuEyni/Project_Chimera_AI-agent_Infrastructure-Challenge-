"""
Pytest configuration and fixtures for Project Chimera.

Provides Mock MCP clients to simulate external service responses without
requiring actual MCP servers (Twitter, Coinbase, etc.) to be running.

This elevates TDD from "failing because code is missing" to 
"passing against a simulated environment."
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal


# ============================================================================
# Mock MCP Client Fixtures
# ============================================================================

class MockMCPResponse:
    """Simulates MCP server response."""
    
    def __init__(self, success: bool = True, data: Any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error


class MockTwitterMCP:
    """Mock Twitter MCP server for trend analysis."""
    
    async def get_trends(self, keywords: List[str], timeframe: str) -> MockMCPResponse:
        """Simulate Twitter trends API response."""
        if not keywords:
            return MockMCPResponse(success=False, error="Keywords required")
        
        # Simulate successful trend data
        trends = [
            {
                "topic": f"{keyword} Innovation",
                "volume": 15000 + i * 1000,
                "sentiment_score": 0.75,
                "rising_velocity": 2.3,
                "platforms": ["twitter"],
                "metadata": {"top_posts": [f"url_{i}"]}
            }
            for i, keyword in enumerate(keywords[:3])
        ]
        
        return MockMCPResponse(success=True, data={"trends": trends})
    
    async def search(self, query: str) -> MockMCPResponse:
        """Simulate Twitter search."""
        return MockMCPResponse(
            success=True,
            data={"results": [{"text": f"Mock tweet about {query}"}]}
        )


class MockCoinbaseMCP:
    """Mock Coinbase AgentKit MCP server for commerce."""
    
    def __init__(self):
        self.balance = Decimal("1000.00")
        self.transactions = []
    
    async def get_balance(self) -> MockMCPResponse:
        """Simulate balance check."""
        return MockMCPResponse(
            success=True,
            data={"balance_usdc": float(self.balance)}
        )
    
    async def transfer(self, recipient: str, amount: Decimal) -> MockMCPResponse:
        """Simulate USDC transfer."""
        if amount > self.balance:
            return MockMCPResponse(
                success=False,
                error="Insufficient balance"
            )
        
        if not recipient.startswith("0x"):
            return MockMCPResponse(
                success=False,
                error="Invalid recipient address"
            )
        
        # Simulate successful transfer
        self.balance -= amount
        tx_hash = f"0x{'a' * 64}"
        self.transactions.append({
            "recipient": recipient,
            "amount": amount,
            "tx_hash": tx_hash
        })
        
        return MockMCPResponse(
            success=True,
            data={
                "tx_hash": tx_hash,
                "new_balance": float(self.balance),
                "status": "CONFIRMED_ON_BASE"
            }
        )


class MockRunwayMCP:
    """Mock Runway Gen-2 MCP server for video generation."""
    
    async def generate_video(
        self,
        prompt: str,
        duration: int = 30
    ) -> MockMCPResponse:
        """Simulate video generation."""
        if duration > 120:
            return MockMCPResponse(
                success=False,
                error="Duration exceeds 120s limit"
            )
        
        return MockMCPResponse(
            success=True,
            data={
                "video_url": f"s3://mock-bucket/video_{hash(prompt)}.mp4",
                "thumbnail_url": f"s3://mock-bucket/thumb_{hash(prompt)}.jpg",
                "duration_seconds": duration,
                "file_size_bytes": duration * 500000,  # ~500KB per second
                "quality_score": 0.92
            }
        )


class MockDALLEMCP:
    """Mock DALL-E 3 MCP server for image generation."""
    
    async def generate_image(self, prompt: str) -> MockMCPResponse:
        """Simulate image generation."""
        return MockMCPResponse(
            success=True,
            data={
                "image_url": f"s3://mock-bucket/image_{hash(prompt)}.png",
                "size_bytes": 2048000,  # 2MB
                "quality_score": 0.95
            }
        )


# ============================================================================
# Pytest Fixtures
# ============================================================================

@pytest.fixture
def mock_twitter_mcp():
    """Provide mock Twitter MCP client."""
    return MockTwitterMCP()


@pytest.fixture
def mock_coinbase_mcp():
    """Provide mock Coinbase MCP client."""
    return MockCoinbaseMCP()


@pytest.fixture
def mock_runway_mcp():
    """Provide mock Runway MCP client."""
    return MockRunwayMCP()


@pytest.fixture
def mock_dalle_mcp():
    """Provide mock DALL-E MCP client."""
    return MockDALLEMCP()


@pytest.fixture
def mock_mcp_registry():
    """Provide registry of all mock MCP clients."""
    return {
        "twitter": MockTwitterMCP(),
        "coinbase": MockCoinbaseMCP(),
        "runway": MockRunwayMCP(),
        "dalle": MockDALLEMCP()
    }


@pytest.fixture
def mock_database():
    """Provide mock database connection."""
    db = MagicMock()
    db.execute = AsyncMock(return_value=None)
    db.fetch = AsyncMock(return_value=[])
    db.fetchrow = AsyncMock(return_value=None)
    return db


@pytest.fixture
def mock_redis():
    """Provide mock Redis connection."""
    redis = MagicMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    redis.delete = AsyncMock(return_value=1)
    return redis


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_trend_data():
    """Provide sample trend data for testing."""
    return {
        "trend_id": "test-trend-123",
        "topic": "AI Regulation",
        "volume": 15000,
        "sentiment_score": 0.75,
        "rising_velocity": 2.3,
        "platforms": ["twitter", "tiktok"],
        "metadata": {"top_posts": ["url1", "url2"]}
    }


@pytest.fixture
def sample_content_brief():
    """Provide sample content brief for testing."""
    return {
        "brief_id": "test-brief-456",
        "trend_id": "test-trend-123",
        "format": "video",
        "script": "Explore the future of AI regulation...",
        "visual_prompts": [
            "Futuristic tech lab with neon lights",
            "AI chip glowing with energy"
        ],
        "tone_guidelines": "Informative but engaging",
        "target_platforms": ["youtube", "tiktok"],
        "estimated_cost": 12.5,
        "projected_engagement": 0.035
    }


@pytest.fixture
def sample_budget_limits():
    """Provide sample budget limits for testing."""
    return {
        "daily": Decimal("1000.00"),
        "weekly": Decimal("5000.00"),
        "monthly": Decimal("20000.00"),
        "min_roi_hurdle": 1.5
    }


# ============================================================================
# Environment Configuration
# ============================================================================

@pytest.fixture
def test_env_vars(monkeypatch):
    """Set test environment variables."""
    test_vars = {
        "DATABASE_URL": "postgresql://test:test@localhost:5432/test_chimera",
        "REDIS_URL": "redis://localhost:6379/1",
        "DAILY_BUDGET_LIMIT": "1000.00",
        "WEEKLY_BUDGET_LIMIT": "5000.00",
        "MONTHLY_BUDGET_LIMIT": "20000.00",
        "MIN_ROI_HURDLE_RATE": "1.5",
        "OPENAI_API_KEY": "test-key",
        "CDP_API_KEY_NAME": "test-cdp-key",
        "CDP_API_KEY_PRIVATE_KEY": "test-private-key"
    }
    
    for key, value in test_vars.items():
        monkeypatch.setenv(key, value)
    
    return test_vars


# ============================================================================
# Test Markers
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "security: mark test as security-related"
    )
    config.addinivalue_line(
        "markers", "financial: mark test as financial safety test"
    )
