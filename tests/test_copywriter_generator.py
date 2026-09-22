"""Tests for content generation - simplified version focusing on interfaces"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from copywriter_agent.generator import ContentGenerator
from copywriter_agent.config import CopywriterConfig
from copywriter_agent.types import PersonaType


@pytest.fixture
def mock_config():
    """Create mock configuration"""
    config = Mock(spec=CopywriterConfig)
    config.claude_api_key = "sk-test"
    config.model = "claude-opus-5"
    config.temperature = 0.8
    config.max_variations = 15
    return config


def test_generator_init(mock_config):
    """Should initialize with config"""
    with patch('copywriter_agent.generator.Anthropic'):
        generator = ContentGenerator(mock_config)
        assert generator.config == mock_config


def test_parse_response_valid_json(mock_config):
    """Should parse valid JSON from Claude response"""
    with patch('copywriter_agent.generator.Anthropic'):
        generator = ContentGenerator(mock_config)

        response_text = '{"title": "Test Title", "hook": "Attention", "description": "Full description", "hashtags": ["test", "demo"], "cta": "Watch"}'
        result = generator._parse_response(response_text)

        assert result["title"] == "Test Title"
        assert result["hook"] == "Attention"
        assert result["description"] == "Full description"
        assert result["hashtags"] == ["test", "demo"]


def test_parse_response_json_in_text(mock_config):
    """Should extract JSON from text with surrounding content"""
    with patch('copywriter_agent.generator.Anthropic'):
        generator = ContentGenerator(mock_config)

        response_text = 'Here is the JSON: {"title": "Test", "hook": "Hook", "description": "Desc", "hashtags": [], "cta": "Watch"} End of JSON'
        result = generator._parse_response(response_text)

        assert result["title"] == "Test"
        assert result["hook"] == "Hook"


def test_parse_response_hashtags_as_string(mock_config):
    """Should convert hashtag string to list"""
    with patch('copywriter_agent.generator.Anthropic'):
        generator = ContentGenerator(mock_config)

        response_text = '{"title": "Test", "hook": "Hook", "description": "Desc", "hashtags": "tag1, tag2, tag3", "cta": "Watch"}'
        result = generator._parse_response(response_text)

        assert isinstance(result["hashtags"], list)
        assert "tag1" in result["hashtags"]
        assert "tag2" in result["hashtags"]


def test_get_aspect_ratio(mock_config):
    """Should return correct aspect ratios for platforms"""
    with patch('copywriter_agent.generator.Anthropic'):
        generator = ContentGenerator(mock_config)

        assert generator._get_aspect_ratio("youtube") == "16:9"
        assert generator._get_aspect_ratio("tiktok") == "9:16"
        assert generator._get_aspect_ratio("instagram") == "9:16"
        assert generator._get_aspect_ratio("telegram") == "9:16"
        assert generator._get_aspect_ratio("rutube") == "16:9"
        assert generator._get_aspect_ratio("unknown") == "1:1"
