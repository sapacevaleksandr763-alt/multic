"""Tests for main Copywriter Agent"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from copywriter_agent.agent import CopywriterAgent
from copywriter_agent.config import CopywriterConfig


def test_agent_init_with_config():
    """Should initialize with provided config"""
    config = Mock(spec=CopywriterConfig)

    with patch('copywriter_agent.agent.CopywriterPipeline'):
        agent = CopywriterAgent(config=config)
        assert agent.config == config


def test_agent_init_from_env():
    """Should load config from environment if not provided"""
    original = os.getenv("CLAUDE_API_KEY")

    try:
        os.environ["CLAUDE_API_KEY"] = "sk-test-env"

        with patch('copywriter_agent.agent.CopywriterPipeline'):
            agent = CopywriterAgent()
            assert agent.config is not None
    finally:
        if original:
            os.environ["CLAUDE_API_KEY"] = original
        elif "CLAUDE_API_KEY" in os.environ:
            del os.environ["CLAUDE_API_KEY"]


def test_agent_has_run_interactive_method():
    """Should have interactive mode method"""
    config = Mock(spec=CopywriterConfig)
    config.model = "claude-opus-5"
    config.temperature = 0.8
    config.max_variations = 15

    with patch('copywriter_agent.agent.CopywriterPipeline'):
        agent = CopywriterAgent(config=config)

        # Should not raise
        agent.run_interactive()
