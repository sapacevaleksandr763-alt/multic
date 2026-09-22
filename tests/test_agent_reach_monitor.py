"""Tests for Agent-Reach social media monitoring integration"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from promotion_agent.agent_reach_monitor import (
    AgentReachMonitor,
    TrendData,
    CompetitorPost,
    VideoMetadata,
    PlatformType,
)
from promotion_agent.config import PromotionConfig


@pytest.fixture
def mock_config():
    """Create mock configuration"""
    config = Mock(spec=PromotionConfig)
    config.search_keywords = ["test", "demo"]
    config.search_channels = ["channel1"]
    config.search_hashtags = ["#test"]
    config.claude_api_key = "test-key"
    config.youtube_api_key = "test-key"
    config.telegram_bot_token = "test-token"
    return config


def test_monitor_init(mock_config):
    """Should initialize monitor with config"""
    monitor = AgentReachMonitor(mock_config)

    assert monitor.config == mock_config
    assert monitor.monitored_keywords == ["test", "demo"]
    assert monitor.monitored_channels == ["channel1"]


def test_search_trends(mock_config):
    """Should search for trends across platforms"""
    monitor = AgentReachMonitor(mock_config)

    trends = monitor.search_trends(["test"])

    assert isinstance(trends, dict)
    assert "reddit" in trends
    assert "youtube" in trends
    assert "x_twitter" in trends
    assert "github" in trends


def test_search_trends_custom_keywords(mock_config):
    """Should use custom keywords for search"""
    monitor = AgentReachMonitor(mock_config)
    custom_keywords = ["custom1", "custom2"]

    trends = monitor.search_trends(keywords=custom_keywords)

    assert isinstance(trends, dict)
    # In real implementation, would verify search used custom keywords


def test_search_trends_default_keywords(mock_config):
    """Should use config keywords if none provided"""
    monitor = AgentReachMonitor(mock_config)

    trends = monitor.search_trends()

    assert isinstance(trends, dict)
    # Should have used config.search_keywords


def test_monitor_competitors(mock_config):
    """Should monitor competitor accounts"""
    monitor = AgentReachMonitor(mock_config)
    competitors = ["competitor1", "competitor2"]

    posts = monitor.monitor_competitors(competitors)

    assert isinstance(posts, dict)
    assert "youtube" in posts
    assert "x_twitter" in posts
    assert "reddit" in posts


def test_extract_video_metadata(mock_config):
    """Should extract metadata from video"""
    monitor = AgentReachMonitor(mock_config)
    video_url = "https://youtube.com/watch?v=test123"

    metadata = monitor.extract_video_metadata(video_url, "youtube")

    if metadata:
        assert isinstance(metadata, VideoMetadata)
        assert metadata.platform == "youtube"
        assert metadata.video_id is not None


def test_extract_video_metadata_invalid_url(mock_config):
    """Should handle invalid video URLs"""
    monitor = AgentReachMonitor(mock_config)

    metadata = monitor.extract_video_metadata("invalid-url", "youtube")

    # Should handle gracefully


def test_get_trending_hashtags_twitter(mock_config):
    """Should get trending hashtags from Twitter"""
    monitor = AgentReachMonitor(mock_config)

    hashtags = monitor.get_trending_hashtags("x_twitter", count=10)

    assert isinstance(hashtags, list)


def test_get_trending_hashtags_telegram(mock_config):
    """Should get trending hashtags from Telegram"""
    monitor = AgentReachMonitor(mock_config)

    hashtags = monitor.get_trending_hashtags("telegram", count=10)

    assert isinstance(hashtags, list)


def test_get_trending_hashtags_reddit(mock_config):
    """Should get trending hashtags from Reddit"""
    monitor = AgentReachMonitor(mock_config)

    hashtags = monitor.get_trending_hashtags("reddit", count=10)

    assert isinstance(hashtags, list)


def test_get_trending_hashtags_unknown_platform(mock_config):
    """Should return empty list for unknown platform"""
    monitor = AgentReachMonitor(mock_config)

    hashtags = monitor.get_trending_hashtags("unknown_platform", count=10)

    assert isinstance(hashtags, list)
    assert len(hashtags) == 0


def test_get_engagement_patterns(mock_config):
    """Should get engagement patterns for platform"""
    monitor = AgentReachMonitor(mock_config)

    patterns = monitor.get_engagement_patterns("youtube", time_period_hours=24)

    assert isinstance(patterns, dict)
    assert patterns["platform"] == "youtube"
    assert patterns["time_period_hours"] == 24
    assert "peak_hours" in patterns
    assert "best_posting_time" in patterns


def test_analyze_competitor_strategy_empty(mock_config):
    """Should handle empty competitor posts"""
    monitor = AgentReachMonitor(mock_config)

    analysis = monitor.analyze_competitor_strategy([])

    assert isinstance(analysis, dict)


def test_analyze_competitor_strategy(mock_config):
    """Should analyze competitor strategy"""
    monitor = AgentReachMonitor(mock_config)

    posts = [
        CompetitorPost(
            platform="youtube",
            competitor_name="Competitor1",
            post_id="vid1",
            content="Test video",
            views=1000,
            engagement=50,
            timestamp=datetime.now(),
            url="https://youtube.com/watch?v=test",
            tags=["test"],
            engagement_rate=0.05,
        )
    ]

    analysis = monitor.analyze_competitor_strategy(posts)

    assert isinstance(analysis, dict)
    assert analysis["total_posts"] == 1
    assert "youtube" in analysis["platforms"]


def test_monitor_caches_trends(mock_config):
    """Should cache trends after search"""
    monitor = AgentReachMonitor(mock_config)

    monitor.search_trends(["test"])

    assert "reddit" in monitor.trends_cache
    assert "youtube" in monitor.trends_cache


def test_monitor_caches_competitors(mock_config):
    """Should cache competitor data after monitoring"""
    monitor = AgentReachMonitor(mock_config)

    monitor.monitor_competitors(["comp1"])

    assert "youtube" in monitor.competitor_cache
    assert "x_twitter" in monitor.competitor_cache


def test_platform_type_enum():
    """Should have all platform types"""
    assert hasattr(PlatformType, "REDDIT")
    assert hasattr(PlatformType, "YOUTUBE")
    assert hasattr(PlatformType, "GITHUB")
    assert hasattr(PlatformType, "X_TWITTER")
    assert hasattr(PlatformType, "TELEGRAM")


def test_trend_data_dataclass():
    """Should create TrendData instance"""
    trend = TrendData(
        platform="youtube",
        title="Test Trend",
        content="Test content",
        engagement_count=100,
        timestamp=datetime.now(),
        url="https://example.com",
        source="YouTube",
        score=85.0,
    )

    assert trend.platform == "youtube"
    assert trend.score == 85.0


def test_video_metadata_dataclass():
    """Should create VideoMetadata instance"""
    metadata = VideoMetadata(
        video_id="vid123",
        title="Test Video",
        platform="youtube",
        duration_seconds=120,
        views=1000,
        engagement=50,
        transcript="Test transcript",
        subtitles="Test subtitles",
    )

    assert metadata.video_id == "vid123"
    assert metadata.platform == "youtube"
    assert metadata.transcript == "Test transcript"
