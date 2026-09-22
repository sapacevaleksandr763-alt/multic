"""Trend analysis - identifies viral patterns and optimal content strategy"""

import logging
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from promotion_agent.agent_reach_monitor import AgentReachMonitor, TrendData, CompetitorPost

logger = logging.getLogger(__name__)


@dataclass
class TrendAnalysis:
    """Analysis of trending topics and patterns"""
    trending_keywords: List[Tuple[str, float]]  # (keyword, score)
    trending_hashtags: List[Tuple[str, int]]  # (hashtag, usage_count)
    trending_formats: List[Tuple[str, float]]  # (format, engagement_rate)
    optimal_posting_times: Dict[str, str]  # platform -> time
    competitor_gaps: List[str]  # Content niches competitors miss
    virality_factors: Dict[str, float]  # Key factors driving virality


@dataclass
class ContentStrategy:
    """Recommended strategy based on trends"""
    primary_themes: List[str]
    recommended_hashtags: List[str]
    optimal_platforms: List[str]
    posting_schedule: Dict[str, str]  # platform -> time
    hook_suggestions: List[str]
    content_gaps: List[str]


class TrendAnalyzer:
    """Analyze social media trends and competitor strategies"""

    def __init__(self, monitor: AgentReachMonitor):
        self.monitor = monitor
        self.analysis_cache: Dict = {}

    def analyze_trends(self) -> TrendAnalysis:
        """
        Analyze current trends across platforms

        Returns:
            TrendAnalysis with trending keywords, hashtags, formats, and optimal times
        """
        logger.info("Starting trend analysis...")

        # Search for trends
        trends_by_platform = self.monitor.search_trends()

        # Extract keywords and analyze virality
        trending_keywords = self._extract_trending_keywords(trends_by_platform)
        trending_hashtags = self._extract_trending_hashtags()
        trending_formats = self._identify_trending_formats(trends_by_platform)
        optimal_times = self._calculate_optimal_posting_times()
        virality_factors = self._analyze_virality_factors(trends_by_platform)

        analysis = TrendAnalysis(
            trending_keywords=trending_keywords[:10],  # Top 10
            trending_hashtags=trending_hashtags[:15],  # Top 15
            trending_formats=trending_formats,
            optimal_posting_times=optimal_times,
            competitor_gaps=[],  # Will be filled by competitor analysis
            virality_factors=virality_factors,
        )

        self.analysis_cache["trends"] = analysis
        return analysis

    def analyze_competitor_strategy(self, competitor_names: List[str]) -> Dict:
        """
        Analyze competitor content strategies

        Returns:
            Dictionary with competitor insights and gaps
        """
        logger.info(f"Analyzing {len(competitor_names)} competitors...")

        competitor_data = self.monitor.monitor_competitors(competitor_names)

        analysis = {
            "competitors": {},
            "industry_patterns": {},
            "content_gaps": [],
            "underexploited_platforms": [],
        }

        # Analyze each competitor
        for platform, posts in competitor_data.items():
            for post in posts:
                if post.competitor_name not in analysis["competitors"]:
                    analysis["competitors"][post.competitor_name] = {
                        "platforms": set(),
                        "average_engagement_rate": 0.0,
                        "content_themes": {},
                        "posting_frequency": 0,
                    }

                comp_data = analysis["competitors"][post.competitor_name]
                comp_data["platforms"].add(platform)
                comp_data["posting_frequency"] += 1

        # Identify gaps
        all_platforms = {post.platform for posts in competitor_data.values() for post in posts}
        used_platforms = set()
        for comp_data in analysis["competitors"].values():
            used_platforms.update(comp_data["platforms"])

        analysis["underexploited_platforms"] = list(all_platforms - used_platforms)
        analysis["content_gaps"] = self._identify_content_gaps(competitor_data)

        self.analysis_cache["competitors"] = analysis
        return analysis

    def generate_content_strategy(
        self, trends: TrendAnalysis, competitor_analysis: Dict
    ) -> ContentStrategy:
        """
        Generate recommended content strategy based on trends and competitors

        Returns:
            ContentStrategy with recommendations
        """
        logger.info("Generating content strategy...")

        # Extract top themes from trends
        primary_themes = [kw for kw, score in trends.trending_keywords[:5]]

        # Recommended hashtags
        recommended_hashtags = [tag for tag, count in trends.trending_hashtags[:10]]

        # Determine optimal platforms (where competitors are weak)
        optimal_platforms = self._determine_optimal_platforms(
            trends.optimal_posting_times.keys(),
            competitor_analysis.get("underexploited_platforms", []),
        )

        # Extract gaps from competitor analysis
        content_gaps = competitor_analysis.get("content_gaps", [])

        # Generate hook suggestions based on trends
        hook_suggestions = self._generate_hook_suggestions(trends.trending_keywords[:5])

        strategy = ContentStrategy(
            primary_themes=primary_themes,
            recommended_hashtags=recommended_hashtags,
            optimal_platforms=optimal_platforms,
            posting_schedule=trends.optimal_posting_times,
            hook_suggestions=hook_suggestions,
            content_gaps=content_gaps[:5],
        )

        self.analysis_cache["strategy"] = strategy
        return strategy

    # Private analysis methods

    def _extract_trending_keywords(self, trends_by_platform: Dict) -> List[Tuple[str, float]]:
        """Extract and score trending keywords across platforms"""
        keyword_scores: Dict[str, float] = {}

        for platform, trends in trends_by_platform.items():
            for trend in trends:
                # Extract keywords from title
                words = trend.title.lower().split()
                for word in words:
                    if len(word) > 3:  # Skip short words
                        score = keyword_scores.get(word, 0)
                        keyword_scores[word] = score + trend.score

        # Sort by score
        sorted_keywords = sorted(
            keyword_scores.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_keywords

    def _extract_trending_hashtags(self) -> List[Tuple[str, int]]:
        """Get trending hashtags from all monitored platforms"""
        all_hashtags: Dict[str, int] = {}

        for platform in ["x_twitter", "telegram", "reddit"]:
            hashtags = self.monitor.get_trending_hashtags(platform, count=10)
            for tag, count in hashtags:
                all_hashtags[tag] = all_hashtags.get(tag, 0) + count

        return sorted(all_hashtags.items(), key=lambda x: x[1], reverse=True)

    def _identify_trending_formats(self, trends_by_platform: Dict) -> List[Tuple[str, float]]:
        """Identify trending content formats"""
        format_engagement: Dict[str, List[float]] = {
            "short_form_video": [],
            "long_form_video": [],
            "text_post": [],
            "image_carousel": [],
            "live_stream": [],
        }

        # Mock analysis - would parse actual content types
        format_engagement["short_form_video"].append(0.85)
        format_engagement["text_post"].append(0.45)
        format_engagement["image_carousel"].append(0.60)

        # Calculate average engagement per format
        format_scores = [
            (fmt, sum(scores) / len(scores) if scores else 0.0)
            for fmt, scores in format_engagement.items()
            if scores
        ]

        return sorted(format_scores, key=lambda x: x[1], reverse=True)

    def _calculate_optimal_posting_times(self) -> Dict[str, str]:
        """Calculate optimal posting times per platform"""
        optimal_times = {}

        for platform in ["youtube", "telegram", "x_twitter", "reddit", "rutube", "vk"]:
            patterns = self.monitor.get_engagement_patterns(platform)
            optimal_times[platform] = patterns.get("best_posting_time", "18:00")

        return optimal_times

    def _analyze_virality_factors(self, trends_by_platform: Dict) -> Dict[str, float]:
        """Analyze what factors drive virality"""
        factors = {
            "emotional_hook": 0.8,
            "trending_hashtags": 0.75,
            "optimal_timing": 0.7,
            "visual_appeal": 0.85,
            "call_to_action": 0.6,
            "relatability": 0.8,
            "novelty": 0.7,
            "community_engagement": 0.75,
        }
        return factors

    def _identify_content_gaps(self, competitor_data: Dict) -> List[str]:
        """Identify content niches competitors are missing"""
        gaps = [
            "Deep educational content on Slavic traditions",
            "Interactive polls and community discussions",
            "Behind-the-scenes content creation",
            "Expert interviews and collaborations",
            "Seasonal/holiday-specific content",
        ]
        return gaps

    def _determine_optimal_platforms(
        self, available_platforms: List[str], underexploited: List[str]
    ) -> List[str]:
        """Determine optimal platforms for new content"""
        # Prioritize underexploited platforms
        optimal = list(underexploited)

        # Add well-performing platforms
        platform_priority = {
            "youtube": 0.95,
            "telegram": 0.85,
            "x_twitter": 0.75,
            "reddit": 0.70,
            "rutube": 0.65,
            "vk": 0.60,
        }

        for platform in available_platforms:
            if platform not in optimal and platform_priority.get(platform, 0) > 0.5:
                optimal.append(platform)

        return optimal[:5]  # Top 5 platforms

    def _generate_hook_suggestions(self, trending_keywords: List[Tuple[str, float]]) -> List[str]:
        """Generate hook suggestions based on trending topics"""
        hooks = []

        for keyword, score in trending_keywords[:3]:
            hooks.append(f"Did you know about {keyword}?")
            hooks.append(f"The truth about {keyword}...")
            hooks.append(f"Why {keyword} is trending now")

        return hooks[:5]
