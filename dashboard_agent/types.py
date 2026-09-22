"""Data types for Master Dashboard"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class DashboardMetricType(Enum):
    """Types of dashboard metrics"""
    VIEWS = "views"
    LIKES = "likes"
    COMMENTS = "comments"
    SHARES = "shares"
    ENGAGEMENT_RATE = "engagement_rate"
    REACH = "reach"
    IMPRESSIONS = "impressions"


@dataclass
class PlatformMetrics:
    """Metrics for single platform"""
    platform: str
    total_videos: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    average_engagement_rate: float = 0.0
    total_reach: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            'platform': self.platform,
            'total_videos': self.total_videos,
            'total_views': self.total_views,
            'total_likes': self.total_likes,
            'total_comments': self.total_comments,
            'total_shares': self.total_shares,
            'average_engagement_rate': round(self.average_engagement_rate, 4),
            'total_reach': self.total_reach,
            'last_updated': self.last_updated.isoformat(),
        }


@dataclass
class VideoAnalytics:
    """Analytics for single published video"""
    video_id: str
    title: str
    original_platform: str

    # Metrics per platform
    platform_metrics: Dict[str, Dict] = field(default_factory=dict)  # {platform: {views, likes, etc}}

    # Engagement
    total_views: int = 0
    total_engagement: int = 0
    top_platform: str = ""
    top_platform_views: int = 0

    # Timing
    published_at: Optional[datetime] = None
    last_fetched: datetime = field(default_factory=datetime.now)

    # Post performance
    posts_generated: int = 0
    posts_published: int = 0
    average_post_engagement: float = 0.0

    def to_dict(self) -> Dict:
        return {
            'video_id': self.video_id,
            'title': self.title,
            'original_platform': self.original_platform,
            'platform_metrics': self.platform_metrics,
            'total_views': self.total_views,
            'total_engagement': self.total_engagement,
            'top_platform': self.top_platform,
            'top_platform_views': self.top_platform_views,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'last_fetched': self.last_fetched.isoformat(),
            'posts_generated': self.posts_generated,
            'posts_published': self.posts_published,
            'average_post_engagement': round(self.average_post_engagement, 4),
        }


@dataclass
class DashboardStats:
    """Overall dashboard statistics"""
    total_videos_found: int = 0
    total_videos_published: int = 0
    total_videos_pending: int = 0

    total_views_all_platforms: int = 0
    total_engagement_all_platforms: int = 0
    average_engagement_rate: float = 0.0

    platforms: Dict[str, PlatformMetrics] = field(default_factory=dict)
    videos: Dict[str, VideoAnalytics] = field(default_factory=dict)

    total_posts_created: int = 0
    total_posts_published: int = 0

    republish_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            'total_videos_found': self.total_videos_found,
            'total_videos_published': self.total_videos_published,
            'total_videos_pending': self.total_videos_pending,
            'total_views_all_platforms': self.total_views_all_platforms,
            'total_engagement_all_platforms': self.total_engagement_all_platforms,
            'average_engagement_rate': round(self.average_engagement_rate, 4),
            'platforms': {k: v.to_dict() for k, v in self.platforms.items()},
            'videos': {k: v.to_dict() for k, v in self.videos.items()},
            'total_posts_created': self.total_posts_created,
            'total_posts_published': self.total_posts_published,
            'republish_count': self.republish_count,
            'last_updated': self.last_updated.isoformat(),
        }


@dataclass
class TimeSeriesData:
    """Time series data for charts"""
    timestamp: datetime
    metric_type: DashboardMetricType
    platform: str
    value: int

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'metric_type': self.metric_type.value,
            'platform': self.platform,
            'value': self.value,
        }


@dataclass
class DashboardEvent:
    """Event log for dashboard"""
    event_type: str  # "published", "republished", "approved", etc.
    video_id: str
    title: str
    details: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            'event_type': self.event_type,
            'video_id': self.video_id,
            'title': self.title,
            'details': self.details,
            'timestamp': self.timestamp.isoformat(),
        }
