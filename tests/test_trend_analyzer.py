"""Tests for trend analysis module"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from promotion_agent.trend_analyzer import TrendAnalyzer, TrendAnalysis, ContentStrategy
from promotion_agent.agent_reach_monitor import AgentReachMonitor, TrendData


@pytest.fixture
def mock_monitor():
    """Create mock Agent-Reach monitor"""
    monitor = Mock(spec=AgentReachMonitor)
    monitor.search_trends.return_value = {
        "reddit": [],
        "youtube": [],
        "x_twitter": [],
        "github": [],
    }
    monitor.monitor_competitors.return_value = {
        "youtube": [],
        "x_twitter": [],
        "reddit": [],
    }
    monitor.get_trending_hashtags.return_value = [("#test", 100), ("#demo", 80)]
    monitor.get_engagement_patterns.return_value = {
        "platform": "youtube",
        "peak_hours": [9, 18],
        "best_posting_time": "18:00",
    }
    return monitor


def test_analyzer_init(mock_monitor):
    """Should initialize trend analyzer"""
    analyzer = TrendAnalyzer(mock_monitor)

    assert analyzer.monitor == mock_monitor
    assert isinstance(analyzer.analysis_cache, dict)


def test_analyze_trends(mock_monitor):
    """Should analyze trends across platforms"""
    analyzer = TrendAnalyzer(mock_monitor)

    trends = analyzer.analyze_trends()

    assert isinstance(trends, TrendAnalysis)
    assert isinstance(trends.trending_keywords, list)
    assert isinstance(trends.trending_hashtags, list)
    assert isinstance(trends.trending_formats, list)
    assert isinstance(trends.optimal_posting_times, dict)


def test_analyze_trends_caches_result(mock_monitor):
    """Should cache analysis result"""
    analyzer = TrendAnalyzer(mock_monitor)

    analyzer.analyze_trends()

    assert "trends" in analyzer.analysis_cache


def test_analyze_competitor_strategy(mock_monitor):
    """Should analyze competitor strategies"""
    analyzer = TrendAnalyzer(mock_monitor)
    competitors = ["competitor1", "competitor2"]

    analysis = analyzer.analyze_competitor_strategy(competitors)

    assert isinstance(analysis, dict)
    assert "competitors" in analysis
    assert "industry_patterns" in analysis
    assert "content_gaps" in analysis


def test_analyze_competitor_strategy_caches_result(mock_monitor):
    """Should cache competitor analysis"""
    analyzer = TrendAnalyzer(mock_monitor)

    analyzer.analyze_competitor_strategy(["comp1"])

    assert "competitors" in analyzer.analysis_cache


def test_generate_content_strategy(mock_monitor):
    """Should generate content strategy"""
    analyzer = TrendAnalyzer(mock_monitor)

    trends = TrendAnalysis(
        trending_keywords=[("keyword1", 0.9), ("keyword2", 0.8)],
        trending_hashtags=[("#tag1", 100)],
        trending_formats=[("short_video", 0.85)],
        optimal_posting_times={"youtube": "18:00"},
        competitor_gaps=["niche1"],
        virality_factors={"hook": 0.8},
    )

    competitor_analysis = {
        "competitors": {},
        "industry_patterns": {},
        "content_gaps": ["gap1"],
        "underexploited_platforms": ["telegram"],
    }

    strategy = analyzer.generate_content_strategy(trends, competitor_analysis)

    assert isinstance(strategy, ContentStrategy)
    assert isinstance(strategy.primary_themes, list)
    assert isinstance(strategy.recommended_hashtags, list)
    assert isinstance(strategy.optimal_platforms, list)
    assert isinstance(strategy.posting_schedule, dict)
    assert isinstance(strategy.hook_suggestions, list)


def test_generate_content_strategy_caches_result(mock_monitor):
    """Should cache generated strategy"""
    analyzer = TrendAnalyzer(mock_monitor)

    trends = TrendAnalysis(
        trending_keywords=[],
        trending_hashtags=[],
        trending_formats=[],
        optimal_posting_times={},
        competitor_gaps=[],
        virality_factors={},
    )

    analyzer.generate_content_strategy(trends, {})

    assert "strategy" in analyzer.analysis_cache


def test_extract_trending_keywords(mock_monitor):
    """Should extract trending keywords from trends"""
    analyzer = TrendAnalyzer(mock_monitor)

    trends_by_platform = {
        "youtube": [
            TrendData(
                platform="youtube",
                title="Python programming tutorial",
                content="Test",
                engagement_count=100,
                timestamp=datetime.now(),
                url="https://example.com",
                source="YouTube",
                score=80.0,
            )
        ]
    }

    keywords = analyzer._extract_trending_keywords(trends_by_platform)

    assert isinstance(keywords, list)


def test_extract_trending_hashtags(mock_monitor):
    """Should extract trending hashtags"""
    analyzer = TrendAnalyzer(mock_monitor)

    hashtags = analyzer._extract_trending_hashtags()

    assert isinstance(hashtags, list)


def test_identify_trending_formats(mock_monitor):
    """Should identify trending content formats"""
    analyzer = TrendAnalyzer(mock_monitor)

    formats = analyzer._identify_trending_formats({})

    assert isinstance(formats, list)
    # Formats should include video, text, images


def test_calculate_optimal_posting_times(mock_monitor):
    """Should calculate optimal posting times"""
    analyzer = TrendAnalyzer(mock_monitor)

    times = analyzer._calculate_optimal_posting_times()

    assert isinstance(times, dict)
    assert "youtube" in times
    assert "telegram" in times


def test_analyze_virality_factors(mock_monitor):
    """Should analyze virality factors"""
    analyzer = TrendAnalyzer(mock_monitor)

    factors = analyzer._analyze_virality_factors({})

    assert isinstance(factors, dict)
    assert "emotional_hook" in factors
    assert "trending_hashtags" in factors
    assert "visual_appeal" in factors


def test_identify_content_gaps(mock_monitor):
    """Should identify content gaps"""
    analyzer = TrendAnalyzer(mock_monitor)

    gaps = analyzer._identify_content_gaps({})

    assert isinstance(gaps, list)
    assert len(gaps) > 0


def test_determine_optimal_platforms(mock_monitor):
    """Should determine optimal platforms"""
    analyzer = TrendAnalyzer(mock_monitor)

    platforms = analyzer._determine_optimal_platforms(
        ["youtube", "telegram", "x_twitter"],
        ["reddit"]
    )

    assert isinstance(platforms, list)
    assert "reddit" in platforms  # Underexploited should be prioritized


def test_generate_hook_suggestions(mock_monitor):
    """Should generate hook suggestions"""
    analyzer = TrendAnalyzer(mock_monitor)

    suggestions = analyzer._generate_hook_suggestions([
        ("technology", 0.9),
        ("innovation", 0.8),
    ])

    assert isinstance(suggestions, list)
    assert len(suggestions) > 0


def test_trend_analysis_dataclass():
    """Should create TrendAnalysis instance"""
    analysis = TrendAnalysis(
        trending_keywords=[("keyword", 0.9)],
        trending_hashtags=[("#tag", 100)],
        trending_formats=[("video", 0.85)],
        optimal_posting_times={"youtube": "18:00"},
        competitor_gaps=["gap1"],
        virality_factors={"hook": 0.8},
    )

    assert len(analysis.trending_keywords) == 1
    assert len(analysis.trending_hashtags) == 1
    assert analysis.optimal_posting_times["youtube"] == "18:00"


def test_content_strategy_dataclass():
    """Should create ContentStrategy instance"""
    strategy = ContentStrategy(
        primary_themes=["theme1"],
        recommended_hashtags=["#tag1"],
        optimal_platforms=["youtube"],
        posting_schedule={"youtube": "18:00"},
        hook_suggestions=["hook1"],
        content_gaps=["gap1"],
    )

    assert strategy.primary_themes[0] == "theme1"
    assert strategy.optimal_platforms[0] == "youtube"
    assert strategy.posting_schedule["youtube"] == "18:00"
