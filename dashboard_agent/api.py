"""API endpoints for Dashboard"""

import json
import logging
from pathlib import Path
from datetime import datetime
from promotion_agent.database import PromotionDatabase
from dashboard_agent.analytics import AnalyticsCollector
from dashboard_agent.types import DashboardStats

logger = logging.getLogger(__name__)


class DashboardAPI:
    """API server for Dashboard - provides JSON endpoints"""

    def __init__(self, db: PromotionDatabase, base_path: str = None):
        self.db = db
        self.collector = AnalyticsCollector(db)
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.cache_file = self.base_path / "dashboard_cache.json"

    def get_dashboard_stats(self, use_cache: bool = True) -> dict:
        """
        Get all dashboard statistics
        Returns: Dictionary with complete dashboard data
        """
        logger.info("Getting dashboard statistics...")

        # Check cache first
        if use_cache and self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    # Validate cache is recent (< 5 minutes)
                    cache_time = datetime.fromisoformat(cache.get('cached_at', ''))
                    if (datetime.now() - cache_time).total_seconds() < 300:
                        logger.info("Using cached dashboard data")
                        return cache
            except Exception as e:
                logger.warning(f"Cache invalid: {e}")

        # Collect fresh metrics
        stats = self.collector.collect_all_metrics()

        # Convert to dict
        data = stats.to_dict()
        data['cached_at'] = datetime.now().isoformat()

        # Cache result
        self._save_cache(data)

        return data

    def get_platform_stats(self, platform: str) -> dict:
        """Get statistics for single platform"""
        stats = self.collector.collect_all_metrics()
        platform_stats = stats.platforms.get(platform)

        if not platform_stats:
            return {'error': f'Platform not found: {platform}'}

        return platform_stats.to_dict()

    def get_video_stats(self, video_id: str) -> dict:
        """Get statistics for single video"""
        stats = self.collector.collect_all_metrics()
        video_stats = stats.videos.get(video_id)

        if not video_stats:
            return {'error': f'Video not found: {video_id}'}

        return video_stats.to_dict()

    def get_top_videos(self, limit: int = 10) -> list:
        """Get top performing videos"""
        stats = self.collector.collect_all_metrics()
        top_videos = stats.videos.items()

        sorted_videos = sorted(
            top_videos,
            key=lambda x: x[1].total_views,
            reverse=True
        )[:limit]

        return [
            {
                'video_id': vid,
                'title': video.title,
                'total_views': video.total_views,
                'total_engagement': video.total_engagement,
                'top_platform': video.top_platform,
            }
            for vid, video in sorted_videos
        ]

    def get_platform_ranking(self) -> list:
        """Get platforms ranked by reach"""
        stats = self.collector.collect_all_metrics()
        ranked = sorted(
            stats.platforms.values(),
            key=lambda p: p.total_views,
            reverse=True
        )

        return [
            {
                'platform': p.platform,
                'total_views': p.total_views,
                'total_engagement': p.total_likes + p.total_comments + p.total_shares,
                'engagement_rate': p.average_engagement_rate,
                'total_videos': p.total_videos,
            }
            for p in ranked
        ]

    def get_overview_summary(self) -> dict:
        """Get KPI summary for dashboard header"""
        stats = self.collector.collect_all_metrics()

        return {
            'total_videos': stats.total_videos_published,
            'total_views': stats.total_views_all_platforms,
            'total_engagement': stats.total_engagement_all_platforms,
            'average_engagement_rate': round(stats.average_engagement_rate, 2),
            'active_platforms': len(stats.platforms),
            'total_posts': stats.total_posts_published,
            'republish_count': stats.republish_count,
            'last_updated': stats.last_updated.isoformat(),
        }

    def log_event(self, event_type: str, video_id: str, title: str, details: str) -> dict:
        """Log an event"""
        self.collector.add_event(event_type, video_id, title, details)

        return {
            'success': True,
            'event_type': event_type,
            'video_id': video_id,
            'timestamp': datetime.now().isoformat(),
        }

    def get_recent_events(self, limit: int = 20) -> list:
        """Get recent events"""
        events = self.collector.get_recent_events(limit)
        return [e.to_dict() for e in events]

    def get_time_series_data(self, platform: str = None, metric_type: str = None,
                            days: int = 30) -> list:
        """Get time series data for charts"""
        # This would aggregate historical data
        # For now, return empty as we need time-series storage
        return []

    def export_analytics_csv(self, filename: str = None) -> str:
        """Export analytics as CSV"""
        import csv

        if not filename:
            filename = f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        filepath = self.base_path / filename

        stats = self.collector.collect_all_metrics()

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Video ID', 'Title', 'Platform', 'Views', 'Likes', 'Comments',
                'Shares', 'Engagement Rate', 'Published Date'
            ])

            # Data
            for video_id, video in stats.videos.items():
                for platform, metrics in video.platform_metrics.items():
                    writer.writerow([
                        video_id,
                        video.title,
                        platform,
                        metrics.get('views', 0),
                        metrics.get('likes', 0),
                        metrics.get('comments', 0),
                        metrics.get('shares', 0),
                        metrics.get('engagement_rate', 0),
                        video.published_at.isoformat() if video.published_at else '',
                    ])

        logger.info(f"Analytics exported to {filepath}")
        return str(filepath)

    def _save_cache(self, data: dict):
        """Save data to cache file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")

    def clear_cache(self) -> bool:
        """Clear dashboard cache"""
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
            logger.info("Dashboard cache cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return False
