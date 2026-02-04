"""
Unit tests for the core swarm coordination system.
"""

import pytest
from chimera.core import ChimeraSwarm, Task


class TestChimeraSwarm:
    """Test cases for ChimeraSwarm class."""
    
    @pytest.mark.asyncio
    async def test_swarm_initialization(self, sample_config):
        """Test swarm initialization."""
        swarm = ChimeraSwarm(sample_config)
        assert swarm.config == sample_config
        assert not swarm.running
        assert len(swarm.tasks) == 0
    
    @pytest.mark.asyncio
    async def test_swarm_start_stop(self, sample_config):
        """Test swarm start and stop functionality."""
        swarm = ChimeraSwarm(sample_config)
        
        await swarm.start()
        assert swarm.running
        
        await swarm.stop()
        assert not swarm.running
    
    @pytest.mark.asyncio
    async def test_task_submission(self, sample_config, sample_task):
        """Test task submission to swarm."""
        swarm = ChimeraSwarm(sample_config)
        
        task = Task(
            id=sample_task["id"],
            description=sample_task["description"],
            priority=sample_task["priority"],
            requirements=sample_task["requirements"]
        )
        
        task_id = await swarm.submit_task(task)
        assert task_id == sample_task["id"]
        assert task_id in swarm.tasks
        
        status = await swarm.get_task_status(task_id)
        assert status == "pending"
    
    @pytest.mark.asyncio
    async def test_task_status_tracking(self, sample_config):
        """Test task status tracking."""
        swarm = ChimeraSwarm(sample_config)
        
        task = Task(
            id="test_status",
            description="Test status tracking",
            priority=1,
            requirements={}
        )
        
        task_id = await swarm.submit_task(task)
        
        # Test initial status
        status = await swarm.get_task_status(task_id)
        assert status == "pending"
        
        # Test non-existent task
        status = await swarm.get_task_status("non_existent")
        assert status is None