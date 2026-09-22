"""Tests for Copywriter Agent configuration"""

import os
import pytest
from copywriter_agent.config import CopywriterConfig


class TestCopywriterConfig:
    """Configuration validation tests"""

    def test_init_with_valid_api_key(self):
        """Should initialize with valid API key"""
        config = CopywriterConfig(claude_api_key="sk-test-key")
        assert config.claude_api_key == "sk-test-key"

    def test_default_values(self):
        """Should use correct default values"""
        config = CopywriterConfig(claude_api_key="sk-test")
        assert config.model == "claude-opus-5"
        assert config.temperature == 0.8
        assert config.max_variations == 15
        assert config.min_quality_score == 0.7

    def test_validate_missing_api_key(self):
        """Should raise ValueError for missing API key"""
        config = CopywriterConfig(claude_api_key="")
        with pytest.raises(ValueError, match="CLAUDE_API_KEY required"):
            config.validate()

    def test_validate_whitespace_api_key(self):
        """Should raise ValueError for whitespace-only API key"""
        config = CopywriterConfig(claude_api_key="   ")
        with pytest.raises(ValueError, match="CLAUDE_API_KEY required"):
            config.validate()

    def test_validate_temperature_too_low(self):
        """Should raise ValueError for temperature < 0"""
        config = CopywriterConfig(claude_api_key="sk-test", temperature=-0.1)
        with pytest.raises(ValueError, match="temperature must be 0-1"):
            config.validate()

    def test_validate_temperature_too_high(self):
        """Should raise ValueError for temperature > 1"""
        config = CopywriterConfig(claude_api_key="sk-test", temperature=1.1)
        with pytest.raises(ValueError, match="temperature must be 0-1"):
            config.validate()

    def test_validate_temperature_boundaries(self):
        """Should accept temperature at 0 and 1 boundaries"""
        config_zero = CopywriterConfig(claude_api_key="sk-test", temperature=0.0)
        config_zero.validate()  # Should not raise

        config_one = CopywriterConfig(claude_api_key="sk-test", temperature=1.0)
        config_one.validate()  # Should not raise

    def test_validate_wrong_max_variations(self):
        """Should raise ValueError if max_variations != 15"""
        config = CopywriterConfig(claude_api_key="sk-test", max_variations=10)
        with pytest.raises(ValueError, match="max_variations must be exactly 15"):
            config.validate()

        config = CopywriterConfig(claude_api_key="sk-test", max_variations=20)
        with pytest.raises(ValueError, match="max_variations must be exactly 15"):
            config.validate()

    def test_validate_quality_score_boundaries(self):
        """Should validate quality score range"""
        config_low = CopywriterConfig(claude_api_key="sk-test", min_quality_score=-0.1)
        with pytest.raises(ValueError, match="min_quality_score must be 0-1"):
            config_low.validate()

        config_high = CopywriterConfig(claude_api_key="sk-test", min_quality_score=1.1)
        with pytest.raises(ValueError, match="min_quality_score must be 0-1"):
            config_high.validate()

    def test_from_env_missing_key(self):
        """Should raise ValueError if CLAUDE_API_KEY not in environment"""
        # Save original env
        original = os.getenv("CLAUDE_API_KEY")

        try:
            # Unset the key
            if "CLAUDE_API_KEY" in os.environ:
                del os.environ["CLAUDE_API_KEY"]

            with pytest.raises(ValueError, match="CLAUDE_API_KEY environment variable not set"):
                CopywriterConfig.from_env()
        finally:
            # Restore original
            if original:
                os.environ["CLAUDE_API_KEY"] = original

    def test_from_env_with_valid_key(self):
        """Should load configuration from environment"""
        # Save original env
        original_key = os.getenv("CLAUDE_API_KEY")

        try:
            os.environ["CLAUDE_API_KEY"] = "sk-env-test"
            os.environ["COPYWRITER_TEMPERATURE"] = "0.5"

            config = CopywriterConfig.from_env()

            assert config.claude_api_key == "sk-env-test"
            assert config.temperature == 0.5
            assert config.max_variations == 15  # Default
        finally:
            # Restore originals
            if original_key:
                os.environ["CLAUDE_API_KEY"] = original_key
            elif "CLAUDE_API_KEY" in os.environ:
                del os.environ["CLAUDE_API_KEY"]

            if "COPYWRITER_TEMPERATURE" in os.environ:
                del os.environ["COPYWRITER_TEMPERATURE"]

    def test_from_env_with_all_customizations(self):
        """Should load all customizable environment variables"""
        original_key = os.getenv("CLAUDE_API_KEY")

        try:
            os.environ["CLAUDE_API_KEY"] = "sk-custom"
            os.environ["COPYWRITER_MODEL"] = "claude-opus-4"
            os.environ["COPYWRITER_TEMPERATURE"] = "0.9"
            os.environ["COPYWRITER_MAX_VARIATIONS"] = "15"
            os.environ["COPYWRITER_MIN_QUALITY"] = "0.8"

            config = CopywriterConfig.from_env()

            assert config.claude_api_key == "sk-custom"
            assert config.model == "claude-opus-4"
            assert config.temperature == 0.9
            assert config.max_variations == 15
            assert config.min_quality_score == 0.8
        finally:
            if original_key:
                os.environ["CLAUDE_API_KEY"] = original_key
            elif "CLAUDE_API_KEY" in os.environ:
                del os.environ["CLAUDE_API_KEY"]

            for key in ["COPYWRITER_MODEL", "COPYWRITER_TEMPERATURE",
                       "COPYWRITER_MAX_VARIATIONS", "COPYWRITER_MIN_QUALITY"]:
                if key in os.environ:
                    del os.environ[key]
