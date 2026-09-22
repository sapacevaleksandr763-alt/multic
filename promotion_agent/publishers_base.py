"""Base publisher interface - common logic for all platforms"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict
from promotion_agent.types import PublishedVideo, SocialPost, PostStatus

logger = logging.getLogger(__name__)


class BasePublisher(ABC):
    """Abstract base class for platform publishers"""

    def __init__(self, platform_name: str, api_key: str):
        self.platform_name = platform_name
        self.api_key = api_key
        self.is_authenticated = False
        self._authenticate()

    @abstractmethod
    def _authenticate(self):
        """Authenticate with platform API"""
        pass

    @abstractmethod
    def publish_video(self, video: PublishedVideo) -> bool:
        """
        Publish video to platform

        Args:
            video: PublishedVideo object with metadata

        Returns:
            True if published successfully
        """
        pass

    @abstractmethod
    def publish_post(self, post: SocialPost) -> bool:
        """
        Publish social media post to platform

        Args:
            post: SocialPost object

        Returns:
            True if published successfully
        """
        pass

    @abstractmethod
    def get_video_info(self, video_url: str) -> Optional[Dict]:
        """Get video information from platform"""
        pass

    def log_publish_action(self, video_id: str, success: bool,
                          action: str = "publish", details: str = ""):
        """Log publishing action for tracking"""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        timestamp = datetime.now().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "platform": self.platform_name,
            "video_id": video_id,
            "action": action,
            "status": status,
            "details": details
        }

        logger.info(f"{status} [{self.platform_name}] {action}: {video_id} - {details}")
        return log_entry

    def _validate_video(self, video: PublishedVideo) -> bool:
        """Validate video before publishing"""
        if not video.title or not video.title.strip():
            logger.error("Video title is empty")
            return False

        if not video.description or not video.description.strip():
            logger.error("Video description is empty")
            return False

        if not video.original_url:
            logger.error("Video URL is missing")
            return False

        return True

    def _validate_post(self, post: SocialPost) -> bool:
        """Validate post before publishing"""
        if not post.title or not post.title.strip():
            logger.error("Post title is empty")
            return False

        if not post.description or not post.description.strip():
            logger.error("Post description is empty")
            return False

        if not post.video_id:
            logger.error("Post video ID is missing")
            return False

        return True


class PublisherRegistry:
    """Registry for managing all platform publishers"""

    def __init__(self):
        self.publishers: Dict[str, BasePublisher] = {}
        self.publish_log = []

    def register(self, publisher: BasePublisher):
        """Register a platform publisher"""
        self.publishers[publisher.platform_name] = publisher
        logger.info(f"Registered publisher: {publisher.platform_name}")

    def get_publisher(self, platform: str) -> Optional[BasePublisher]:
        """Get publisher for platform"""
        return self.publishers.get(platform)

    def publish_to_all(self, video: PublishedVideo) -> Dict[str, bool]:
        """
        Publish video to all registered platforms

        Args:
            video: PublishedVideo object

        Returns:
            Dict mapping platform -> success status
        """
        results = {}

        for platform, publisher in self.publishers.items():
            try:
                success = publisher.publish_video(video)
                results[platform] = success

                if success:
                    # Update video with publish date
                    video.platforms_published[platform] = datetime.now()
                    print(f"✅ Published to {platform}")
                else:
                    print(f"❌ Failed to publish to {platform}")

            except Exception as e:
                logger.error(f"Error publishing to {platform}: {e}")
                results[platform] = False

        return results

    def publish_posts_to_all(self, posts: list) -> Dict[str, bool]:
        """
        Publish multiple posts to their respective platforms

        Args:
            posts: List of SocialPost objects

        Returns:
            Dict mapping platform -> success status
        """
        results = {}

        for post in posts:
            publisher = self.get_publisher(post.platform)
            if not publisher:
                logger.warning(f"No publisher for platform: {post.platform}")
                results[post.platform] = False
                continue

            try:
                success = publisher.publish_post(post)
                results[post.platform] = success

                if success:
                    post.status = PostStatus.PUBLISHED
                    post.published_at = datetime.now()
                    print(f"✅ Published post to {post.platform}")
                else:
                    print(f"❌ Failed to publish post to {post.platform}")

            except Exception as e:
                logger.error(f"Error publishing post to {post.platform}: {e}")
                results[post.platform] = False

        return results

    def get_statistics(self) -> Dict:
        """Get publishing statistics"""
        return {
            "total_platforms": len(self.publishers),
            "active_platforms": list(self.publishers.keys()),
            "total_publishes": len(self.publish_log),
        }
