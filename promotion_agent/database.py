"""JSON-based database for published videos and posts"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
from promotion_agent.types import PublishedVideo, SocialPost, VideoStatus, PostStatus


class PromotionDatabase:
    """Manages published videos and posts with JSON storage"""

    def __init__(self, base_path: str = "C:\\Users\\Alex\\Downloads\\rutube-videos"):
        self.base_path = Path(base_path)
        self.published_dir = self.base_path / "Опубликовано"
        self.found_dir = self.base_path / "found"

        # Create directories if not exist
        self.published_dir.mkdir(parents=True, exist_ok=True)
        self.found_dir.mkdir(parents=True, exist_ok=True)

        # Database files
        self.videos_file = self.published_dir / "videos.json"
        self.posts_file = self.published_dir / "posts.json"

        # Load or initialize
        self._ensure_databases()

    def _ensure_databases(self):
        """Create database files if they don't exist"""
        if not self.videos_file.exists():
            self.videos_file.write_text(json.dumps({"videos": []}, ensure_ascii=False, indent=2))

        if not self.posts_file.exists():
            self.posts_file.write_text(json.dumps({"posts": []}, ensure_ascii=False, indent=2))

    def _load_videos(self) -> List[Dict]:
        """Load all videos from database"""
        try:
            content = self.videos_file.read_text(encoding='utf-8')
            data = json.loads(content)
            return data.get("videos", [])
        except Exception as e:
            print(f"Error loading videos: {e}")
            return []

    def _save_videos(self, videos: List[Dict]):
        """Save all videos to database"""
        try:
            self.videos_file.write_text(
                json.dumps({"videos": videos}, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
        except Exception as e:
            print(f"Error saving videos: {e}")

    def _load_posts(self) -> List[Dict]:
        """Load all posts from database"""
        try:
            content = self.posts_file.read_text(encoding='utf-8')
            data = json.loads(content)
            return data.get("posts", [])
        except Exception as e:
            print(f"Error loading posts: {e}")
            return []

    def _save_posts(self, posts: List[Dict]):
        """Save all posts to database"""
        try:
            self.posts_file.write_text(
                json.dumps({"posts": posts}, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
        except Exception as e:
            print(f"Error saving posts: {e}")

    def add_video(self, video: PublishedVideo) -> bool:
        """Add published video to database"""
        try:
            videos = self._load_videos()

            # Convert to dict
            video_dict = {
                "video_id": video.video_id,
                "title": video.title,
                "description": video.description,
                "original_url": video.original_url,
                "original_platform": video.original_platform,
                "status": video.status.value,
                "approved_at": video.approved_at.isoformat() if video.approved_at else None,
                "platforms_published": {
                    k: v.isoformat() for k, v in video.platforms_published.items()
                },
                "duration_seconds": video.duration_seconds,
                "file_path": video.file_path,
                "was_trimmed": video.was_trimmed,
                "subtitles_added": video.subtitles_added,
                "created_at": video.created_at.isoformat(),
                "last_republished": video.last_republished.isoformat() if video.last_republished else None,
                "republish_count": video.republish_count,
            }

            videos.append(video_dict)
            self._save_videos(videos)
            return True
        except Exception as e:
            print(f"Error adding video: {e}")
            return False

    def get_video(self, video_id: str) -> Optional[PublishedVideo]:
        """Get video by ID"""
        videos = self._load_videos()
        for v in videos:
            if v["video_id"] == video_id:
                return self._dict_to_video(v)
        return None

    def get_all_videos(self) -> List[PublishedVideo]:
        """Get all published videos"""
        videos = self._load_videos()
        return [self._dict_to_video(v) for v in videos]

    def update_video(self, video: PublishedVideo) -> bool:
        """Update existing video"""
        try:
            videos = self._load_videos()
            for i, v in enumerate(videos):
                if v["video_id"] == video.video_id:
                    video_dict = {
                        "video_id": video.video_id,
                        "title": video.title,
                        "description": video.description,
                        "original_url": video.original_url,
                        "original_platform": video.original_platform,
                        "status": video.status.value,
                        "approved_at": video.approved_at.isoformat() if video.approved_at else None,
                        "platforms_published": {
                            k: v.isoformat() for k, v in video.platforms_published.items()
                        },
                        "duration_seconds": video.duration_seconds,
                        "file_path": video.file_path,
                        "was_trimmed": video.was_trimmed,
                        "subtitles_added": video.subtitles_added,
                        "created_at": video.created_at.isoformat(),
                        "last_republished": video.last_republished.isoformat() if video.last_republished else None,
                        "republish_count": video.republish_count,
                    }
                    videos[i] = video_dict
                    self._save_videos(videos)
                    return True
            return False
        except Exception as e:
            print(f"Error updating video: {e}")
            return False

    def add_post(self, post: SocialPost) -> bool:
        """Add social media post"""
        try:
            posts = self._load_posts()
            post_dict = {
                "post_id": post.post_id,
                "video_id": post.video_id,
                "platform": post.platform,
                "title": post.title,
                "description": post.description,
                "hashtags": post.hashtags,
                "cta": post.cta,
                "status": post.status.value,
                "scheduled_publish_at": post.scheduled_publish_at.isoformat(),
                "published_at": post.published_at.isoformat() if post.published_at else None,
                "created_at": post.created_at.isoformat(),
            }
            posts.append(post_dict)
            self._save_posts(posts)
            return True
        except Exception as e:
            print(f"Error adding post: {e}")
            return False

    def get_pending_posts(self) -> List[SocialPost]:
        """Get all pending posts"""
        posts = self._load_posts()
        pending = [p for p in posts if p["status"] == PostStatus.PENDING.value]
        return [self._dict_to_post(p) for p in pending]

    @staticmethod
    def _dict_to_video(d: Dict) -> PublishedVideo:
        """Convert dict to PublishedVideo"""
        platforms_published = {}
        for k, v in d.get("platforms_published", {}).items():
            platforms_published[k] = datetime.fromisoformat(v)

        return PublishedVideo(
            video_id=d["video_id"],
            title=d["title"],
            description=d["description"],
            original_url=d["original_url"],
            original_platform=d["original_platform"],
            status=VideoStatus(d["status"]),
            approved_at=datetime.fromisoformat(d["approved_at"]) if d.get("approved_at") else None,
            platforms_published=platforms_published,
            duration_seconds=d.get("duration_seconds", 0),
            file_path=d.get("file_path"),
            was_trimmed=d.get("was_trimmed", False),
            subtitles_added=d.get("subtitles_added", False),
            created_at=datetime.fromisoformat(d["created_at"]),
            last_republished=datetime.fromisoformat(d["last_republished"]) if d.get("last_republished") else None,
            republish_count=d.get("republish_count", 0),
        )

    @staticmethod
    def _dict_to_post(d: Dict) -> SocialPost:
        """Convert dict to SocialPost"""
        return SocialPost(
            post_id=d["post_id"],
            video_id=d["video_id"],
            platform=d["platform"],
            title=d["title"],
            description=d["description"],
            hashtags=d["hashtags"],
            cta=d["cta"],
            status=PostStatus(d["status"]),
            scheduled_publish_at=datetime.fromisoformat(d["scheduled_publish_at"]),
            published_at=datetime.fromisoformat(d["published_at"]) if d.get("published_at") else None,
            created_at=datetime.fromisoformat(d["created_at"]),
        )
