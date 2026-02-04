"""
Test configuration and utilities for Project Chimera.
"""

import pytest
import asyncio
from typing import Dict, Any
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Sample configuration for testing."""
    return {
        "risk_tolerance": "CONSERVATIVE",
        "budget": 10000,
        "max_agents": 100,
        "security_level": "high"
    }

@pytest.fixture
def sample_task() -> Dict[str, Any]:
    """Sample task for testing."""
    return {
        "id": "test_task_001",
        "description": "Test task for unit testing",
        "priority": 1,
        "requirements": {
            "compute": "low",
            "memory": "medium",
            "timeout": 300
        }
    }