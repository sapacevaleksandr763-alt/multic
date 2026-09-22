"""Main Promotion Agent - interactive workflow for video publishing"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from promotion_agent.config import PromotionConfig
from promotion_agent.database import PromotionDatabase
from promotion_agent.types import PendingReview, PublishedVideo, VideoStatus, SocialPost

logger = logging.getLogger(__name__)


class PromotionAgent:
    """
    Promotion Agent: Manages video publishing workflow with user approval

    Workflow:
    1. Find videos (Wed/Sat)
    2. Generate pending_review.json
    3. User reviews and approves/rejects
    4. Auto-publish approved videos to 7 platforms
    5. Create posts 1 day after video publication
    6. Track republishing capability
    """

    def __init__(self, config: Optional[PromotionConfig] = None):
        if config is None:
            config = PromotionConfig.from_env()

        self.config = config
        self.db = PromotionDatabase(config.base_download_path)

        logger.info("PromotionAgent initialized")

    def generate_pending_review_file(self, found_videos: List[PendingReview]) -> Path:
        """
        Generate pending_review.json for user to review

        Args:
            found_videos: List of videos found and waiting for review

        Returns:
            Path to generated JSON file
        """
        pending_file = Path(self.config.found_videos_path) / "pending_review.json"

        videos_data = []
        for i, video in enumerate(found_videos, 1):
            videos_data.append({
                "index": i,
                "video_id": video.video_id,
                "title": video.title,
                "description": video.description,
                "original_url": video.original_url,
                "platform": video.platform,
                "duration_seconds": video.duration_seconds,
                "duration_formatted": self._format_duration(video.duration_seconds),
                "file_path": video.file_path,
                "file_size_mb": round(video.file_size_mb, 2),
                "issues": video.issues,
                "created_at": video.created_at.isoformat(),
            })

        pending_data = {
            "total_videos": len(found_videos),
            "generated_at": datetime.now().isoformat(),
            "instructions": "Review videos and run: /approve or /reject <video_index> <reason>",
            "videos": videos_data,
        }

        pending_file.write_text(
            json.dumps(pending_data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        logger.info(f"Generated pending_review.json with {len(found_videos)} videos")
        print(f"\n{'='*70}")
        print(f"📋 PENDING REVIEW: {len(found_videos)} videos found")
        print(f"{'='*70}")
        print(json.dumps(pending_data, ensure_ascii=False, indent=2))
        print(f"\n✅ Waiting for your command:")
        print(f"   /approve <index> - Approve video")
        print(f"   /reject <index> - Reject with reason")
        print(f"   /edit <index> 'Сократи на 50 символов' - Edit and resubmit")
        print(f"{'='*70}\n")

        return pending_file

    def approve_video(self, video_id: str) -> PublishedVideo:
        """
        Approve a video for publishing

        Args:
            video_id: ID of video to approve

        Returns:
            PublishedVideo object ready for publishing
        """
        video = PublishedVideo(
            video_id=video_id,
            title="",
            description="",
            original_url="",
            original_platform="",
            status=VideoStatus.APPROVED,
            approved_at=datetime.now(),
        )

        self.db.add_video(video)
        logger.info(f"Approved video: {video_id}")

        print(f"✅ Video {video_id} APPROVED")
        print(f"📅 Will be published to 7 platforms")

        return video

    def reject_video(self, video_id: str, reason: str) -> bool:
        """
        Reject a video with feedback

        Args:
            video_id: ID of video to reject
            reason: Reason for rejection (e.g., "Сократи на 50 символов")

        Returns:
            True if rejected successfully
        """
        logger.info(f"Rejected video {video_id}: {reason}")

        print(f"❌ Video {video_id} REJECTED")
        print(f"📝 Feedback: {reason}")
        print(f"🔄 Waiting for fixes and resubmission...")

        return True

    def republish_video(self, video_id: str) -> bool:
        """
        Republish existing video to all platforms

        Args:
            video_id: ID of video to republish

        Returns:
            True if republish initiated
        """
        video = self.db.get_video(video_id)

        if not video:
            logger.error(f"Video not found: {video_id}")
            print(f"❌ Video {video_id} not found in database")
            return False

        video.last_republished = datetime.now()
        video.republish_count += 1

        self.db.update_video(video)
        logger.info(f"Initiated republish for video: {video_id}")

        print(f"🔄 Republishing video: {video.title}")
        print(f"📊 Republish count: {video.republish_count}")
        print(f"📅 Publishing to all 7 platforms...")

        return True

    def get_videos_ready_for_posting(self) -> List[PublishedVideo]:
        """
        Get videos published more than 1 day ago (ready for social posts)

        Returns:
            List of videos ready for posting
        """
        all_videos = self.db.get_all_videos()
        ready = []

        for video in all_videos:
            if video.status != VideoStatus.PUBLISHED:
                continue

            # Find oldest publish date
            if not video.platforms_published:
                continue

            oldest_publish = min(video.platforms_published.values())
            hours_since = (datetime.now() - oldest_publish).total_seconds() / 3600

            if hours_since >= self.config.post_delay_hours:
                ready.append(video)

        return ready

    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Format seconds to HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
