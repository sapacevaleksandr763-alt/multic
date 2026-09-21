"""YouTube video downloader"""

import logging
from typing import List, Optional
from datetime import datetime
from .types import YouTubeVideo

logger = logging.getLogger(__name__)

class YouTubeDownloader:
    """Download metadata from YouTube"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._setup_youtube_api()

    def _setup_youtube_api(self):
        """Initialize YouTube API client"""
        try:
            from googleapiclient.discovery import build
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        except ImportError:
            logger.warning("google-api-python-client not installed, using fallback")
            self.youtube = None

    def search(self, query: str, max_results: int = 20) -> List[YouTubeVideo]:
        """Search YouTube for videos matching query"""
        if not self.youtube:
            raise RuntimeError("YouTube API not available")

        videos = []
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=min(max_results, 50),
                order='relevance',
                publishedAfter='2020-01-01T00:00:00Z'
            )

            response = request.execute()

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']

                video = YouTubeVideo(
                    youtube_id=video_id,
                    title=snippet['title'],
                    channel=snippet['channelTitle'],
                    view_count=0,  # Will be fetched separately
                    published_at=datetime.fromisoformat(
                        snippet['publishedAt'].replace('Z', '+00:00')
                    ),
                    duration_seconds=0,  # Will be fetched separately
                    description=snippet['description'],
                    thumbnail_url=snippet['thumbnails'].get('medium', {}).get('url', '')
                )
                videos.append(video)

            # Get detailed statistics
            self._enrich_videos(videos)

        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
            raise

        return videos

    def _enrich_videos(self, videos: List[YouTubeVideo]):
        """Fetch view counts and durations for videos"""
        if not videos or not self.youtube:
            return

        video_ids = [v.youtube_id for v in videos]

        try:
            request = self.youtube.videos().list(
                part='statistics,contentDetails',
                id=','.join(video_ids)
            )
            response = request.execute()

            stats_map = {}
            for item in response.get('items', []):
                video_id = item['id']
                stats = item['statistics']
                duration_str = item['contentDetails']['duration']

                stats_map[video_id] = {
                    'view_count': int(stats.get('viewCount', 0)),
                    'duration_seconds': self._parse_duration(duration_str)
                }

            for video in videos:
                if video.youtube_id in stats_map:
                    stats = stats_map[video.youtube_id]
                    video.view_count = stats['view_count']
                    video.duration_seconds = stats['duration_seconds']

        except Exception as e:
            logger.warning(f"Could not enrich video stats: {e}")

    @staticmethod
    def _parse_duration(duration_str: str) -> int:
        """Parse ISO 8601 duration (PT1H23M45S) to seconds"""
        import re
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)

        if not match:
            return 0

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)

        return hours * 3600 + minutes * 60 + seconds
