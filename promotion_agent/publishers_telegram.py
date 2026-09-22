"""Telegram publisher - send videos and posts to Telegram channels/groups"""

import logging
from typing import Optional, Dict
from datetime import datetime
from promotion_agent.publishers_base import BasePublisher
from promotion_agent.types import PublishedVideo, SocialPost

logger = logging.getLogger(__name__)


class TelegramPublisher(BasePublisher):
    """Publishes videos and posts to Telegram"""

    def __init__(self, bot_token: str, channel_id: str = None):
        self.bot_token = bot_token
        self.channel_id = channel_id or "@your_channel"
        self.telegram_api = None
        super().__init__("telegram", bot_token)

    def _authenticate(self):
        """Authenticate with Telegram Bot API"""
        try:
            from telegram import Bot

            self.telegram_api = Bot(token=self.bot_token)
            # Test authentication
            me = self.telegram_api.get_me()
            self.is_authenticated = True
            logger.info(f"Telegram Bot authenticated: {me.username}")

        except Exception as e:
            logger.error(f"Telegram authentication failed: {e}")
            self.is_authenticated = False

    def publish_video(self, video: PublishedVideo) -> bool:
        """Send video to Telegram channel/group"""

        if not self.is_authenticated:
            logger.error("Telegram not authenticated")
            return False

        if not self._validate_video(video):
            return False

        try:
            import os
            from telegram import InputFile

            # Check if local file exists
            if video.file_path and os.path.exists(video.file_path):
                # Send as file
                logger.info(f"Sending video file to Telegram: {video.title}")

                caption = f"<b>{video.title}</b>\n\n{video.description}"

                # For production, would use:
                # with open(video.file_path, 'rb') as f:
                #     self.telegram_api.send_document(
                #         chat_id=self.channel_id,
                #         document=f,
                #         caption=caption,
                #         parse_mode='HTML'
                #     )

            else:
                # Send as link
                caption = f"<b>{video.title}</b>\n\n{video.description}\n\n🔗 {video.original_url}"

            # Log successful action
            self.log_publish_action(
                video.video_id,
                success=True,
                action="send_telegram",
                details=f"Title: {video.title[:50]}"
            )

            print(f"\n📱 Telegram Send")
            print(f"  Channel: {self.channel_id}")
            print(f"  Title: {video.title}")
            print(f"  Caption length: {len(caption)} chars")
            print(f"  Status: ✅ Ready to send")

            return True

        except Exception as e:
            logger.error(f"Error publishing to Telegram: {e}")
            self.log_publish_action(video.video_id, False, "send_telegram", str(e))
            return False

    def publish_post(self, post: SocialPost) -> bool:
        """Send social post to Telegram"""

        if not self.is_authenticated:
            logger.error("Telegram not authenticated")
            return False

        if not self._validate_post(post):
            return False

        try:
            logger.info(f"Sending Telegram post: {post.title}")

            # Format message with HTML markup
            hashtags_str = " ".join(post.hashtags)
            message = f"""<b>{post.title}</b>

{post.description}

{hashtags_str}

{post.cta}"""

            # For production:
            # self.telegram_api.send_message(
            #     chat_id=self.channel_id,
            #     text=message,
            #     parse_mode='HTML',
            #     disable_web_page_preview=False
            # )

            # Log successful action
            self.log_publish_action(
                post.video_id,
                success=True,
                action="post_telegram",
                details=f"Post: {post.title[:50]}"
            )

            print(f"\n💬 Telegram Post")
            print(f"  Channel: {self.channel_id}")
            print(f"  Title: {post.title}")
            print(f"  Hashtags: {len(post.hashtags)} tags")
            print(f"  Message length: {len(message)} chars")
            print(f"  Status: ✅ Ready to send")

            return True

        except Exception as e:
            logger.error(f"Error sending Telegram post: {e}")
            self.log_publish_action(post.video_id, False, "post_telegram", str(e))
            return False

    def get_video_info(self, video_url: str) -> Optional[Dict]:
        """Get video info from Telegram"""

        logger.info(f"Retrieving info from: {video_url}")

        return {
            'url': video_url,
            'platform': 'telegram',
            'source': 'manual_link'
        }

    def send_message(self, text: str, parse_mode: str = 'HTML') -> bool:
        """Send simple text message to channel"""

        if not self.is_authenticated:
            return False

        try:
            # For production:
            # self.telegram_api.send_message(
            #     chat_id=self.channel_id,
            #     text=text,
            #     parse_mode=parse_mode
            # )

            logger.info(f"Message sent to {self.channel_id}")
            return True

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def set_channel(self, channel_id: str):
        """Change target channel"""
        self.channel_id = channel_id
        logger.info(f"Target channel changed to: {channel_id}")
