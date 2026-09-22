"""Video finder - searches for Slavic-Aryan themed content across platforms"""

import logging
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class FoundVideoInfo:
    """Info about found video"""
    title: str
    url: str
    channel_name: str
    platform: str  # youtube, rutube, etc.
    duration_seconds: int
    view_count: int = 0
    upload_date: str = ""
    matched_keywords: List[str] = None

    def __post_init__(self):
        if self.matched_keywords is None:
            self.matched_keywords = []

    @property
    def video_id(self) -> str:
        """Generate unique video ID from URL and title"""
        combined = f"{self.url}_{self.title}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]


class VideoFinder:
    """Finds videos from multiple platforms matching search criteria"""

    def __init__(self, config):
        self.config = config
        self.keywords = config.search_keywords
        self.channels = config.search_channels
        self.hashtags = config.search_hashtags

    def search_all_platforms(self) -> List[FoundVideoInfo]:
        """Search all platforms for matching videos"""
        all_videos = []

        logger.info("Starting video search across all platforms...")

        # YouTube search
        youtube_videos = self._search_youtube()
        all_videos.extend(youtube_videos)
        logger.info(f"Found {len(youtube_videos)} videos on YouTube")

        # RuTube search
        rutube_videos = self._search_rutube()
        all_videos.extend(rutube_videos)
        logger.info(f"Found {len(rutube_videos)} videos on RuTube")

        # Telegram channels search
        telegram_videos = self._search_telegram()
        all_videos.extend(telegram_videos)
        logger.info(f"Found {len(telegram_videos)} videos on Telegram")

        # VK search
        vk_videos = self._search_vk()
        all_videos.extend(vk_videos)
        logger.info(f"Found {len(vk_videos)} videos on VK")

        # Remove duplicates by URL
        unique_videos = {v.url: v for v in all_videos}
        result = list(unique_videos.values())

        logger.info(f"Total unique videos found: {len(result)}")
        return result

    def _search_youtube(self) -> List[FoundVideoInfo]:
        """Search YouTube for Slavic-Aryan content"""
        videos = []

        try:
            from googleapiclient.discovery import build

            youtube = build('youtube', 'v3', developerKey=self.config.youtube_api_key)

            # Search for each keyword
            for keyword in self.keywords[:3]:  # Limit to avoid quota issues
                try:
                    request = youtube.search().list(
                        q=keyword,
                        part='snippet',
                        maxResults=10,
                        type='video',
                        relevanceLanguage='ru',
                        order='relevance'
                    )
                    response = request.execute()

                    for item in response.get('items', []):
                        video_info = FoundVideoInfo(
                            title=item['snippet']['title'],
                            url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                            channel_name=item['snippet']['channelTitle'],
                            platform='youtube',
                            duration_seconds=0,  # Would need video details endpoint
                            upload_date=item['snippet']['publishedAt'],
                            matched_keywords=[keyword]
                        )

                        # Filter by channel if specified
                        if self._channel_matches(video_info.channel_name):
                            videos.append(video_info)

                except Exception as e:
                    logger.warning(f"Error searching YouTube for '{keyword}': {e}")

        except ImportError:
            logger.warning("Google API client not installed. Skipping YouTube search.")

        return videos

    def _search_rutube(self) -> List[FoundVideoInfo]:
        """Search RuTube for Slavic-Aryan content"""
        videos = []

        try:
            import requests

            for keyword in self.keywords[:3]:
                try:
                    # RuTube API endpoint
                    url = "https://rutube.ru/api/v3/search/videos/"
                    params = {
                        'query': keyword,
                        'limit': 10,
                        'language': 'ru'
                    }

                    response = requests.get(url, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                    for item in data.get('results', []):
                        video_info = FoundVideoInfo(
                            title=item.get('title', ''),
                            url=item.get('video_url', ''),
                            channel_name=item.get('author', {}).get('name', ''),
                            platform='rutube',
                            duration_seconds=int(item.get('duration', 0)),
                            view_count=int(item.get('hits', 0)),
                            upload_date=item.get('created_ts', ''),
                            matched_keywords=[keyword]
                        )

                        if self._channel_matches(video_info.channel_name):
                            videos.append(video_info)

                except Exception as e:
                    logger.warning(f"Error searching RuTube for '{keyword}': {e}")

        except ImportError:
            logger.warning("requests library not installed. Skipping RuTube search.")

        return videos

    def _search_telegram(self) -> List[FoundVideoInfo]:
        """Search Telegram channels for Slavic-Aryan content"""
        videos = []

        try:
            # This would require Telegram Bot API integration
            # For now, returning empty list
            logger.info("Telegram search requires separate setup with Telegram Bot API")

        except Exception as e:
            logger.warning(f"Error searching Telegram: {e}")

        return videos

    def _search_vk(self) -> List[FoundVideoInfo]:
        """Search VK for Slavic-Aryan content"""
        videos = []

        try:
            # This would require VK API integration
            # For now, returning empty list
            logger.info("VK search requires VK API token")

        except Exception as e:
            logger.warning(f"Error searching VK: {e}")

        return videos

    def _channel_matches(self, channel_name: str) -> bool:
        """Check if channel name matches our priority list or keywords"""
        if not channel_name:
            return False

        channel_lower = channel_name.lower()

        # Check priority channels
        for channel in self.channels:
            if channel.lower() in channel_lower:
                return True

        # Check keywords in channel name
        for keyword in self.keywords:
            if keyword.lower() in channel_lower:
                return True

        return False

    def filter_by_duration(self, videos: List[FoundVideoInfo],
                          max_seconds: int = 3600) -> List[FoundVideoInfo]:
        """Filter videos by duration"""
        return [v for v in videos if v.duration_seconds <= max_seconds]

    def filter_by_date(self, videos: List[FoundVideoInfo],
                      days_back: int = 30) -> List[FoundVideoInfo]:
        """Filter videos by upload date (last N days)"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.now() - timedelta(days=days_back)
        result = []

        for video in videos:
            try:
                if video.upload_date:
                    upload_date = datetime.fromisoformat(video.upload_date.replace('Z', '+00:00'))
                    if upload_date >= cutoff_date:
                        result.append(video)
            except:
                # If date parsing fails, include the video
                result.append(video)

        return result
