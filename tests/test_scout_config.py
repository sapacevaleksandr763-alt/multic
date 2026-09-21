"""Tests for Scout Agent configuration"""

import pytest
import os
from scout_agent.config import ScoutConfig


class TestScoutConfig:
    """Tests for ScoutConfig"""

    def test_default_config(self):
        """Test creating config with defaults"""
        config = ScoutConfig()
        assert config.youtube_api_key == ""
        assert config.youtube_max_results == 20
        assert config.whisper_model == "base"
        assert config.language == "en"
        assert config.min_viral_score == 0.6
        assert config.max_results == 5

    def test_from_env(self, monkeypatch):
        """Test loading config from environment"""
        monkeypatch.setenv("YOUTUBE_API_KEY", "test_key_123")
        monkeypatch.setenv("WHISPER_MODEL", "small")
        monkeypatch.setenv("MAX_RESULTS", "10")

        config = ScoutConfig.from_env()

        assert config.youtube_api_key == "test_key_123"
        assert config.whisper_model == "small"
        assert config.max_results == 10

    def test_custom_config(self):
        """Test creating config with custom values"""
        config = ScoutConfig(
            youtube_api_key="my_key",
            max_results=3,
            min_viral_score=0.8
        )
        assert config.youtube_api_key == "my_key"
        assert config.max_results == 3
        assert config.min_viral_score == 0.8

    def test_config_validation(self):
        """Test config validation"""
        config = ScoutConfig(
            max_results=100,  # Should still work
            min_viral_score=1.5  # Could be out of range
        )
        # Config allows any value, validation happens at runtime
        assert config.max_results == 100
