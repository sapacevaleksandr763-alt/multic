"""Tests for Copywriter pipeline"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from copywriter_agent.pipeline import CopywriterPipeline
from copywriter_agent.config import CopywriterConfig
from copywriter_agent.types import PublishTimeOptimal


@pytest.fixture
def mock_config():
    """Create mock configuration"""
    config = Mock(spec=CopywriterConfig)
    config.claude_api_key = "sk-test"
    config.model = "claude-opus-5"
    config.temperature = 0.8
    config.max_variations = 15
    return config


def test_pipeline_init(mock_config):
    """Should initialize pipeline with config"""
    with patch('copywriter_agent.pipeline.ContentGenerator'):
        pipeline = CopywriterPipeline(mock_config)
        assert pipeline.config == mock_config


def test_optimal_publish_time_youtube():
    """Should return MORNING for YouTube"""
    pipeline = Mock(spec=CopywriterPipeline)
    time = CopywriterPipeline._optimal_publish_time("youtube", Mock())
    assert time == PublishTimeOptimal.MORNING


def test_optimal_publish_time_tiktok():
    """Should return MIDDAY for TikTok"""
    pipeline = Mock(spec=CopywriterPipeline)
    time = CopywriterPipeline._optimal_publish_time("tiktok", Mock())
    assert time == PublishTimeOptimal.MIDDAY


def test_optimal_publish_time_telegram():
    """Should return EVENING for Telegram"""
    pipeline = Mock(spec=CopywriterPipeline)
    time = CopywriterPipeline._optimal_publish_time("telegram", Mock())
    assert time == PublishTimeOptimal.EVENING


def test_estimate_reach():
    """Should estimate reach based on platform and viral score"""
    pipeline = Mock(spec=CopywriterPipeline)
    video = Mock()
    video.overall_viral_score = 85

    reach = CopywriterPipeline._estimate_reach("youtube", video)
    assert isinstance(reach, int)
    assert reach > 0


def test_estimate_reach_scales_with_viral_score():
    """Should increase reach with higher viral score"""
    pipeline = Mock(spec=CopywriterPipeline)
    video_low = Mock()
    video_low.overall_viral_score = 40
    video_high = Mock()
    video_high.overall_viral_score = 95

    reach_low = CopywriterPipeline._estimate_reach("youtube", video_low)
    reach_high = CopywriterPipeline._estimate_reach("youtube", video_high)
    assert reach_high > reach_low


def test_estimate_engagement():
    """Should estimate engagement rate"""
    pipeline = Mock(spec=CopywriterPipeline)
    video = Mock()
    video.overall_viral_score = 85

    engagement = CopywriterPipeline._estimate_engagement("youtube", video)
    assert isinstance(engagement, float)
    assert 0 <= engagement <= 0.30


def test_recommendation_confidence():
    """Should calculate recommendation confidence"""
    pipeline = Mock(spec=CopywriterPipeline)
    video = Mock()
    video.overall_viral_score = 85

    confidence = CopywriterPipeline._recommendation_confidence("youtube", video)
    assert isinstance(confidence, float)
    assert 0.5 <= confidence <= 0.95


def test_recommendation_confidence_high_viral_score():
    """Should boost confidence for high viral scores"""
    pipeline = Mock(spec=CopywriterPipeline)
    video = Mock()
    video.overall_viral_score = 95

    confidence = CopywriterPipeline._recommendation_confidence("youtube", video)
    assert confidence > 0.75  # Default base
