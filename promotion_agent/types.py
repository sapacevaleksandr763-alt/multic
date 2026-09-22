"""Data types for Promotion Agent (Phase 2C)"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class PlatformType(Enum):
    """Supported platforms for video promotion"""
    YOUTUBE = "youtube"
    TELEGRAM = "telegram"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    RUTUBE = "rutube"
    VK = "vk"
    OKRU = "okru"


class VideoStatus(Enum):
    """Status of video in workflow"""
    FOUND = "found"  # Found, waiting for review
    APPROVED = "approved"  # User approved
    REJECTED = "rejected"  # User rejected, waiting for fixes
    PUBLISHING = "publishing"  # Currently publishing
    PUBLISHED = "published"  # Published to at least one platform
    FAILED = "failed"  # Publication failed


class PostStatus(Enum):
    """Status of social media post"""
    PENDING = "pending"  # Waiting to publish
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class VideoMetadata:
    """Video metadata for found content"""
    video_id: str  # Unique ID (hash of URL or channel+title)
    title: str
    description: str
    channel_name: str
    url: str
    platform: str  # Where found (youtube, rutube, etc.)
    duration_seconds: int
    view_count: int = 0
    like_count: int = 0
    upload_date: str = ""
    thumbnai_url: Optional[str] = None
    keywords: List[str] = field(default_factory=list)  # Search keywords it matched
    found_at: datetime = field(default_factory=datetime.now)


@dataclass
class PublishedVideo:
    """Video approved and published"""
    video_id: str
    title: str
    description: str
    original_url: str  # Source URL
    original_platform: str  # Where found

    # Publishing history
    status: VideoStatus = VideoStatus.APPROVED
    approved_at: Optional[datetime] = None
    approved_by: str = "user"  # Who approved

    # Published platforms (track dates for 3-day interval)
    platforms_published: Dict[str, datetime] = field(default_factory=dict)  # {platform: publish_date}

    # Metadata
    duration_seconds: int = 0
    file_path: Optional[str] = None  # Local copy path
    local_file_hash: Optional[str] = None

    # Modifications
    was_trimmed: bool = False
    trim_duration: Optional[int] = None
    subtitles_added: bool = False
    subtitles_lang: str = "ru"

    # Tracking
    created_at: datetime = field(default_factory=datetime.now)
    last_republished: Optional[datetime] = None
    republish_count: int = 0

    @property
    def id(self) -> str:
        """Composite ID"""
        return self.video_id

    def can_publish_to_platform(self, platform: str, days_interval: int = 3) -> bool:
        """Check if platform can be published to (respects 3-day interval)"""
        if platform not in self.platforms_published:
            return True  # Never published

        last_publish = self.platforms_published[platform]
        days_since = (datetime.now() - last_publish).days
        return days_since >= days_interval


@dataclass
class SocialPost:
    """Social media post derived from video"""
    post_id: str  # Unique ID
    video_id: str  # Reference to published video
    platform: str  # Which platform

    # Content
    title: str
    description: str
    hashtags: List[str]
    cta: str  # Call-to-action

    # Scheduling
    status: PostStatus = PostStatus.PENDING
    scheduled_publish_at: datetime = field(default_factory=datetime.now)
    published_at: Optional[datetime] = None

    # Tracking
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def id(self) -> str:
        return self.post_id


@dataclass
class PendingReview:
    """Video waiting for user approval"""
    video_id: str
    title: str
    description: str
    original_url: str
    platform: str  # Where found
    duration_seconds: int
    file_path: str  # Local file path for review
    file_size_mb: float

    # What needs review
    issues: List[str] = field(default_factory=list)  # [e.g., "description too long"]

    created_at: datetime = field(default_factory=datetime.now)

    @property
    def id(self) -> str:
        return self.video_id


@dataclass
class PromotionResult:
    """Result of promotion workflow"""
    videos_found: int = 0
    videos_approved: int = 0
    videos_published: int = 0
    posts_created: int = 0
    posts_published: int = 0
    errors: List[str] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.now)
