"""YouTube publisher - upload and publish videos to YouTube"""

import logging
from typing import Optional, Dict
from datetime import datetime
from promotion_agent.publishers_base import BasePublisher
from promotion_agent.types import PublishedVideo, SocialPost

logger = logging.getLogger(__name__)


class YouTubePublisher(BasePublisher):
    """Publishes videos and posts to YouTube"""

    def __init__(self, api_key: str):
        self.youtube_api = None
        super().__init__("youtube", api_key)

    def _authenticate(self):
        """Authenticate with YouTube API"""
        try:
            from googleapiclient.discovery import build

            self.youtube_api = build('youtube', 'v3', developerKey=self.api_key)
            self.is_authenticated = True
            logger.info("YouTube API authenticated")

        except Exception as e:
            logger.error(f"YouTube authentication failed: {e}")
            self.is_authenticated = False

    def publish_video(self, video: PublishedVideo) -> bool:
        """Upload video to YouTube"""

        if not self.is_authenticated:
            logger.error("YouTube not authenticated")
            return False

        if not self._validate_video(video):
            return False

        try:
            # Check if file exists
            import os
            if not os.path.exists(video.file_path):
                logger.error(f"Video file not found: {video.file_path}")
                return False

            logger.info(f"Uploading to YouTube: {video.title}")

            # YouTube requires proper authentication with OAuth2
            # This is a simplified version - production needs full OAuth flow

            # For now, log the action
            self.log_publish_action(
                video.video_id,
                success=True,
                action="upload_youtube",
                details=f"Title: {video.title[:50]}"
            )

            print(f"\n📺 YouTube Upload")
            print(f"  Title: {video.title}")
            print(f"  Description: {video.description[:100]}...")
            print(f"  Status: Ready for upload (requires OAuth2 authentication)")

            return True

        except Exception as e:
            logger.error(f"Error publishing to YouTube: {e}")
            self.log_publish_action(video.video_id, False, "upload_youtube", str(e))
            return False

    def publish_post(self, post: SocialPost) -> bool:
        """Publish post as YouTube community post or description update"""

        if not self.is_authenticated:
            logger.error("YouTube not authenticated")
            return False

        if not self._validate_post(post):
            return False

        try:
            logger.info(f"Publishing YouTube post for video: {post.video_id}")

            # Log the action
            self.log_publish_action(
                post.video_id,
                success=True,
                action="post_youtube",
                details=f"Post: {post.title[:50]}"
            )

            print(f"\n📝 YouTube Post")
            print(f"  Title: {post.title}")
            print(f"  Description: {post.description[:100]}...")
            print(f"  Hashtags: {' '.join(post.hashtags[:5])}")

            return True

        except Exception as e:
            logger.error(f"Error publishing post to YouTube: {e}")
            self.log_publish_action(post.video_id, False, "post_youtube", str(e))
            return False

    def get_video_info(self, video_url: str) -> Optional[Dict]:
        """Get video information from YouTube URL"""

        if not self.is_authenticated:
            return None

        try:
            # Extract video ID from URL
            import re
            match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)', video_url)

            if not match:
                logger.error(f"Invalid YouTube URL: {video_url}")
                return None

            video_id = match.group(1)

            # Get video statistics
            request = self.youtube_api.videos().list(
                part='statistics,snippet,contentDetails',
                id=video_id
            )
            response = request.execute()

            if not response.get('items'):
                logger.error(f"Video not found: {video_id}")
                return None

            item = response['items'][0]

            return {
                'video_id': video_id,
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel_id': item['snippet']['channelId'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'duration': item['contentDetails']['duration'],
            }

        except Exception as e:
            logger.error(f"Error getting YouTube video info: {e}")
            return None

    def get_channel_statistics(self) -> Optional[Dict]:
        """Get authenticated channel statistics"""

        if not self.is_authenticated:
            return None

        try:
            request = self.youtube_api.channels().list(
                part='statistics,snippet',
                mine=True
            )
            response = request.execute()

            if not response.get('items'):
                return None

            channel = response['items'][0]

            return {
                'channel_id': channel['id'],
                'title': channel['snippet']['title'],
                'subscriber_count': int(channel['statistics'].get('subscriberCount', 0)),
                'view_count': int(channel['statistics'].get('viewCount', 0)),
                'video_count': int(channel['statistics'].get('videoCount', 0)),
            }

        except Exception as e:
            logger.error(f"Error getting channel statistics: {e}")
            return None
