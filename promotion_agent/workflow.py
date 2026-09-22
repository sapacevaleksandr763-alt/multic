"""Unified workflow - orchestrates entire promotion process"""

import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from promotion_agent.agent import PromotionAgent
from promotion_agent.database import PromotionDatabase
from promotion_agent.video_finder import VideoFinder, FoundVideoInfo
from promotion_agent.video_downloader import VideoDownloader, DownloadedVideo
from promotion_agent.review_generator import ReviewGenerator
from promotion_agent.post_generator import PostGenerator
from promotion_agent.subtitle_generator import SubtitleGenerator
from promotion_agent.publishers_base import PublisherRegistry
from promotion_agent.publishers_youtube import YouTubePublisher
from promotion_agent.publishers_telegram import TelegramPublisher
from promotion_agent.types import PendingReview, PublishedVideo, VideoStatus, SocialPost
from promotion_agent.config import PromotionConfig
from promotion_agent.agent_reach_monitor import AgentReachMonitor

logger = logging.getLogger(__name__)


class PromotionWorkflow:
    """
    Orchestrates entire promotion workflow:
    1. Find videos (Wed/Sat)
    2. User review & approval
    3. Download & process
    4. Publish to 7 platforms
    5. Generate posts (1 day later)
    6. Track & republish
    """

    def __init__(self, config: PromotionConfig):
        self.config = config
        self.agent = PromotionAgent(config)
        self.db = PromotionDatabase(config.base_download_path)

        # Initialize components
        self.finder = VideoFinder(config)
        self.downloader = VideoDownloader(config.found_videos_path)
        self.review_gen = ReviewGenerator(config.found_videos_path)
        self.post_gen = PostGenerator(config.claude_api_key)
        self.subtitle_gen = SubtitleGenerator()

        # Initialize Agent-Reach monitor for trend detection & competitor analysis
        self.reach_monitor = AgentReachMonitor(config)

        # Initialize publishers
        self.publishers = PublisherRegistry()
        self._setup_publishers()

        logger.info("PromotionWorkflow initialized with Agent-Reach monitoring")

    def _setup_publishers(self):
        """Setup all platform publishers"""
        try:
            # YouTube
            youtube_pub = YouTubePublisher(self.config.youtube_api_key)
            self.publishers.register(youtube_pub)

            # Telegram
            telegram_pub = TelegramPublisher(self.config.telegram_bot_token)
            self.publishers.register(telegram_pub)

            # Placeholder for other publishers
            logger.info("Publishers initialized: YouTube, Telegram")

        except Exception as e:
            logger.error(f"Error setting up publishers: {e}")

    # ============================================================
    # PHASE 1: DISCOVERY (Wednesday & Saturday)
    # ============================================================

    def discover_videos(self) -> List[PendingReview]:
        """
        Search for Slavic-Aryan videos
        Runs automatically Wed/Sat
        """
        logger.info("Starting video discovery phase...")
        print(f"\n{'='*70}")
        print(f"🔍 PHASE 1: VIDEO DISCOVERY")
        print(f"{'='*70}")

        # Find videos from all platforms
        found_videos = self.finder.search_all_platforms()

        # Filter by duration (max 60 min default)
        found_videos = self.finder.filter_by_duration(
            found_videos,
            self.config.max_video_duration_seconds
        )

        # Filter by date (last 30 days)
        found_videos = self.finder.filter_by_date(found_videos, days_back=30)

        if not found_videos:
            print("❌ No videos found matching criteria")
            return []

        print(f"✅ Found {len(found_videos)} videos")

        # Convert to PendingReview objects
        pending_videos = []
        for video in found_videos:
            pending = PendingReview(
                video_id=video.video_id,
                title=video.title,
                description="",  # Will be filled during download
                original_url=video.url,
                platform=video.platform,
                duration_seconds=video.duration_seconds,
                file_path="",  # Will be set after download
                file_size_mb=0,  # Will be set after download
                issues=[]
            )
            pending_videos.append(pending)

        return pending_videos

    # ============================================================
    # PHASE 2: REVIEW & APPROVAL
    # ============================================================

    def generate_review(self, videos: List[PendingReview]) -> Path:
        """
        Generate PDF & JSON for user review
        Returns path to pending_review.json
        """
        logger.info(f"Generating review for {len(videos)} videos...")
        print(f"\n{'='*70}")
        print(f"📋 PHASE 2: REVIEW & APPROVAL")
        print(f"{'='*70}")

        # Generate PDF
        pdf_path = self.review_gen.generate_review_document(videos)
        print(f"\n📄 PDF Review: {pdf_path}")

        # Generate JSON
        json_path = self.agent.generate_pending_review_file(videos)
        print(f"📊 JSON Data: {json_path}")

        print(f"\n✅ Review documents ready")
        print(f"📝 Waiting for your commands:")
        print(f"   /approve <index>")
        print(f"   /reject <index> 'Reason'")
        print(f"   /edit <index> 'Changes'")

        return json_path

    def process_user_command(self, command: str, video_id: str,
                            details: str = "") -> bool:
        """
        Process user commands: /approve, /reject, /edit
        Logs action and updates pending_review.json
        """
        logger.info(f"Processing command: {command} for video: {video_id}")

        if command == "approve":
            print(f"\n✅ APPROVED: {video_id}")
            print(f"📥 Queuing for download and processing...")
            return self.agent.approve_video(video_id) is not None

        elif command == "reject":
            print(f"\n❌ REJECTED: {video_id}")
            print(f"📝 Feedback: {details}")
            return self.agent.reject_video(video_id, details)

        elif command == "edit":
            print(f"\n✏️  EDITING: {video_id}")
            print(f"📝 Changes: {details}")
            print(f"🔄 Reprocessing with new parameters...")
            return True

        return False

    # ============================================================
    # PHASE 3: DOWNLOAD & PROCESS
    # ============================================================

    def download_and_process(self, video_id: str, video_url: str) -> Optional[DownloadedVideo]:
        """
        Download video from URL
        Extract metadata
        Prepare for publishing
        """
        logger.info(f"Downloading video: {video_url}")
        print(f"\n{'='*70}")
        print(f"⬇️  PHASE 3: DOWNLOAD & PROCESSING")
        print(f"{'='*70}")

        # Get video info first
        info = self.downloader.get_video_info(video_url)
        if not info:
            print("❌ Could not fetch video information")
            return None

        title = info.get('title', 'Unknown')
        print(f"\n📹 Title: {title}")
        print(f"⏱️  Duration: {info.get('duration', 'Unknown')}")
        print(f"👁️  Views: {info.get('view_count', 0):,}")

        # Download video
        print(f"\n⬇️  Downloading...")
        downloaded = self.downloader.download_video(
            video_url,
            title,
            video_id
        )

        if not downloaded:
            print("❌ Download failed")
            return None

        print(f"✅ Downloaded: {downloaded.file_path}")
        print(f"📊 Size: {downloaded.file_size_mb:.1f} MB")
        print(f"⏱️  Duration: {downloaded.duration_seconds} seconds")

        return downloaded

    # ============================================================
    # PHASE 4: PUBLISHING
    # ============================================================

    def publish_to_all_platforms(self, video: PublishedVideo) -> Dict[str, bool]:
        """
        Publish approved video to 7 platforms
        Respects 3-day interval between publishes
        """
        logger.info(f"Publishing video to all platforms: {video.video_id}")
        print(f"\n{'='*70}")
        print(f"🚀 PHASE 4: MULTI-PLATFORM PUBLISHING")
        print(f"{'='*70}")

        # Check 3-day interval
        platforms_ready = []
        platforms_waiting = []

        for platform in ['youtube', 'telegram', 'tiktok', 'instagram', 'rutube', 'vk', 'okru']:
            if video.can_publish_to_platform(platform, days_interval=3):
                platforms_ready.append(platform)
            else:
                last_date = video.platforms_published.get(platform)
                if last_date:
                    days_until = 3 - (datetime.now() - last_date).days
                    platforms_waiting.append(f"{platform} ({days_until}d)")

        print(f"\n✅ Ready to publish ({len(platforms_ready)}):")
        for p in platforms_ready:
            print(f"   • {p.upper()}")

        if platforms_waiting:
            print(f"\n⏳ Waiting (3-day interval):")
            for p in platforms_waiting:
                print(f"   • {p}")

        # Publish to all platforms
        print(f"\n📤 Publishing...")
        results = self.publishers.publish_to_all(video)

        # Update video in database
        video.status = VideoStatus.PUBLISHED
        self.db.update_video(video)

        # Summary
        success_count = sum(1 for v in results.values() if v)
        print(f"\n{'='*70}")
        print(f"📊 PUBLISHING SUMMARY")
        print(f"✅ Success: {success_count}/{len(results)}")
        print(f"❌ Failed: {len(results) - success_count}/{len(results)}")
        print(f"{'='*70}")

        return results

    # ============================================================
    # PHASE 5: SOCIAL POSTS (1 day after video publication)
    # ============================================================

    def generate_and_publish_posts(self, video: PublishedVideo) -> List[SocialPost]:
        """
        Generate platform-specific posts
        Schedule for 1 day after video publication
        """
        logger.info(f"Generating posts for video: {video.video_id}")
        print(f"\n{'='*70}")
        print(f"📱 PHASE 5: SOCIAL MEDIA POSTS")
        print(f"{'='*70}")

        # Check if 1 day has passed since publication
        if not video.platforms_published:
            print("❌ Video not yet published to any platform")
            return []

        oldest_publish = min(video.platforms_published.values())
        hours_since = (datetime.now() - oldest_publish).total_seconds() / 3600

        if hours_since < 24:
            hours_remaining = 24 - hours_since
            print(f"⏳ Waiting for 24h after publication...")
            print(f"   Ready in {hours_remaining:.1f} hours")
            return []

        print(f"✅ 24 hours passed since publication")

        # Generate posts
        print(f"\n📝 Generating posts...")
        posts = self.post_gen.generate_posts(video)

        print(f"✅ Generated {len(posts)} platform-specific posts")
        for post in posts:
            print(f"   • {post.platform}: {post.title[:50]}...")
            self.db.add_post(post)

        # Publish posts
        print(f"\n📤 Publishing posts...")
        self.publishers.publish_posts_to_all(posts)

        return posts

    # ============================================================
    # PHASE 6: REPUBLISHING
    # ============================================================

    def republish_video(self, video_id: str) -> bool:
        """
        Republish existing video on demand
        Tracks republish count and history
        """
        logger.info(f"Republishing video: {video_id}")
        print(f"\n{'='*70}")
        print(f"🔄 PHASE 6: REPUBLISHING")
        print(f"{'='*70}")

        video = self.db.get_video(video_id)
        if not video:
            print(f"❌ Video not found: {video_id}")
            return False

        print(f"\n📹 Video: {video.title}")
        print(f"📊 Republish count: {video.republish_count}")

        # Publish to all platforms
        results = self.publishers.publish_to_all(video)

        # Update video
        self.agent.republish_video(video_id)

        success = sum(1 for v in results.values() if v)
        print(f"✅ Republished to {success} platforms")

        return True

    # ============================================================
    # UTILITIES
    # ============================================================

    def get_workflow_status(self) -> Dict:
        """Get current workflow status"""
        all_videos = self.db.get_all_videos()

        return {
            "total_videos": len(all_videos),
            "published": sum(1 for v in all_videos if v.status == VideoStatus.PUBLISHED),
            "approved": sum(1 for v in all_videos if v.status == VideoStatus.APPROVED),
            "platforms_active": self.publishers.get_statistics()['active_platforms'],
        }

    def print_status(self):
        """Print workflow status"""
        status = self.get_workflow_status()

        print(f"\n{'='*70}")
        print(f"📊 WORKFLOW STATUS")
        print(f"{'='*70}")
        print(f"Videos in Database:")
        print(f"  Total: {status['total_videos']}")
        print(f"  Published: {status['published']}")
        print(f"  Approved: {status['approved']}")
        print(f"\nActive Platforms: {', '.join(status['platforms_active'])}")
        print(f"{'='*70}")
