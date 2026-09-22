"""Analytics collector - gathers metrics from all platforms"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from promotion_agent.database import PromotionDatabase
from dashboard_agent.types import (
    PlatformMetrics, VideoAnalytics, DashboardStats, TimeSeriesData,
    DashboardEvent, DashboardMetricType
)

logger = logging.getLogger(__name__)


class AnalyticsCollector:
    """Collects and aggregates metrics from all platforms"""

    def __init__(self, db: PromotionDatabase):
        self.db = db
        self.stats = DashboardStats()
        self.events = []
        self.time_series = []

    def collect_all_metrics(self) -> DashboardStats:
        """
        Collect all metrics from database
        Aggregate by platform and video
        """
        logger.info("Collecting all metrics...")

        # Get all videos from database
        all_videos = self.db.get_all_videos()

        self.stats.total_videos_found = len(all_videos)
        self.stats.total_videos_published = sum(1 for v in all_videos if v.status.value == "published")
        self.stats.total_videos_pending = sum(1 for v in all_videos if v.status.value == "approved")

        # Initialize platform metrics
        platforms = set()
        for video in all_videos:
            platforms.update(video.platforms_published.keys())

        for platform in platforms:
            self.stats.platforms[platform] = PlatformMetrics(platform=platform)

        # Aggregate metrics per video and platform
        total_views = 0
        total_engagement = 0

        for video in all_videos:
            video_analytics = self._create_video_analytics(video)
            self.stats.videos[video.video_id] = video_analytics

            total_views += video_analytics.total_views
            total_engagement += video_analytics.total_engagement

            # Update platform metrics
            for platform in video_analytics.platform_metrics.keys():
                if platform in self.stats.platforms:
                    platform_data = video_analytics.platform_metrics[platform]
                    metrics = self.stats.platforms[platform]
                    metrics.total_videos += 1
                    metrics.total_views += platform_data.get('views', 0)
                    metrics.total_likes += platform_data.get('likes', 0)
                    metrics.total_comments += platform_data.get('comments', 0)

        self.stats.total_views_all_platforms = total_views
        self.stats.total_engagement_all_platforms = total_engagement

        if self.stats.total_videos_published > 0:
            self.stats.average_engagement_rate = (
                total_engagement / self.stats.total_videos_published / 1000
            )  # Normalize

        self.stats.last_updated = datetime.now()

        logger.info(f"Collected metrics: {self.stats.total_videos_published} published videos")
        return self.stats

    def _create_video_analytics(self, video) -> VideoAnalytics:
        """Create analytics for single video"""
        analytics = VideoAnalytics(
            video_id=video.video_id,
            title=video.title,
            original_platform=video.original_platform,
            published_at=video.approved_at,
        )

        # Mock metrics (will be replaced with actual API calls)
        for platform in video.platforms_published.keys():
            analytics.platform_metrics[platform] = {
                'views': self._estimate_views(platform, video),
                'likes': self._estimate_likes(platform, video),
                'comments': self._estimate_comments(platform, video),
                'shares': self._estimate_shares(platform, video),
                'engagement_rate': self._estimate_engagement_rate(platform, video),
            }

            platform_views = analytics.platform_metrics[platform]['views']
            if platform_views > analytics.top_platform_views:
                analytics.top_platform = platform
                analytics.top_platform_views = platform_views

        analytics.total_views = sum(
            m.get('views', 0) for m in analytics.platform_metrics.values()
        )
        analytics.total_engagement = sum(
            m.get('likes', 0) + m.get('comments', 0) + m.get('shares', 0)
            for m in analytics.platform_metrics.values()
        )

        return analytics

    def _estimate_views(self, platform: str, video) -> int:
        """Estimate views based on platform and video age"""
        base_views = {
            'youtube': 5000,
            'telegram': 2000,
            'tiktok': 8000,
            'instagram': 3000,
            'rutube': 1500,
            'vk': 2000,
            'okru': 1000,
        }

        base = base_views.get(platform, 1000)

        # Scale by video age (days since publication)
        if video.approved_at:
            days_old = (datetime.now() - video.approved_at).days
            age_multiplier = 1 + (days_old * 0.1)  # 10% growth per day
            base = int(base * age_multiplier)

        # Scale by republishes
        base = int(base * (1 + video.republish_count * 0.5))

        return base

    def _estimate_likes(self, platform: str, video) -> int:
        """Estimate likes based on platform"""
        engagement_rates = {
            'youtube': 0.05,  # 5%
            'telegram': 0.08,  # 8%
            'tiktok': 0.12,  # 12%
            'instagram': 0.06,  # 6%
            'rutube': 0.04,  # 4%
            'vk': 0.07,  # 7%
            'okru': 0.03,  # 3%
        }

        rate = engagement_rates.get(platform, 0.05)
        views = self._estimate_views(platform, video)
        return int(views * rate)

    def _estimate_comments(self, platform: str, video) -> int:
        """Estimate comments based on platform"""
        comment_rates = {
            'youtube': 0.02,  # 2%
            'telegram': 0.05,  # 5%
            'tiktok': 0.08,  # 8%
            'instagram': 0.03,  # 3%
            'rutube': 0.01,  # 1%
            'vk': 0.04,  # 4%
            'okru': 0.01,  # 1%
        }

        rate = comment_rates.get(platform, 0.01)
        views = self._estimate_views(platform, video)
        return int(views * rate)

    def _estimate_shares(self, platform: str, video) -> int:
        """Estimate shares based on platform"""
        share_rates = {
            'youtube': 0.01,  # 1%
            'telegram': 0.03,  # 3%
            'tiktok': 0.05,  # 5%
            'instagram': 0.02,  # 2%
            'rutube': 0.005,  # 0.5%
            'vk': 0.02,  # 2%
            'okru': 0.005,  # 0.5%
        }

        rate = share_rates.get(platform, 0.01)
        views = self._estimate_views(platform, video)
        return int(views * rate)

    def _estimate_engagement_rate(self, platform: str, video) -> float:
        """Calculate engagement rate"""
        views = self._estimate_views(platform, video)
        if views == 0:
            return 0.0

        engagement = (
            self._estimate_likes(platform, video) +
            self._estimate_comments(platform, video) +
            self._estimate_shares(platform, video)
        )

        return round((engagement / views) * 100, 2)

    def get_platform_stats(self, platform: str) -> Optional[PlatformMetrics]:
        """Get metrics for single platform"""
        return self.stats.platforms.get(platform)

    def get_video_stats(self, video_id: str) -> Optional[VideoAnalytics]:
        """Get metrics for single video"""
        return self.stats.videos.get(video_id)

    def add_event(self, event_type: str, video_id: str, title: str, details: str):
        """Log an event"""
        event = DashboardEvent(
            event_type=event_type,
            video_id=video_id,
            title=title,
            details=details,
        )
        self.events.append(event)
        logger.info(f"Event: {event_type} - {video_id}")

    def get_recent_events(self, limit: int = 10) -> list:
        """Get recent events"""
        return self.events[-limit:]

    def get_top_videos_by_views(self, limit: int = 10) -> list:
        """Get top performing videos"""
        sorted_videos = sorted(
            self.stats.videos.values(),
            key=lambda v: v.total_views,
            reverse=True
        )
        return sorted_videos[:limit]

    def get_top_platforms_by_reach(self) -> list:
        """Get top platforms by reach"""
        sorted_platforms = sorted(
            self.stats.platforms.values(),
            key=lambda p: p.total_reach,
            reverse=True
        )
        return sorted_platforms
