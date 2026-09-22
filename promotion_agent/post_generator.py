"""Social media post generator - creates platform-specific posts from videos"""

import logging
from typing import List, Dict
from datetime import datetime
from promotion_agent.types import SocialPost, PublishedVideo

logger = logging.getLogger(__name__)


class PostGenerator:
    """Generates social media posts from published videos"""

    def __init__(self, claude_api_key: str):
        self.claude_api_key = claude_api_key
        self.platforms = [
            'youtube', 'telegram', 'tiktok', 'instagram', 'rutube', 'vk', 'okru'
        ]

    def generate_posts(self, video: PublishedVideo) -> List[SocialPost]:
        """
        Generate posts for each platform from video description

        Args:
            video: Published video

        Returns:
            List of SocialPost objects ready for scheduling
        """
        posts = []

        logger.info(f"Generating posts for video: {video.title}")

        for platform in self.platforms:
            try:
                post = self._generate_platform_post(video, platform)
                if post:
                    posts.append(post)
            except Exception as e:
                logger.error(f"Error generating post for {platform}: {e}")

        return posts

    def _generate_platform_post(self, video: PublishedVideo,
                               platform: str) -> SocialPost:
        """Generate post tailored to specific platform"""

        # Platform-specific configurations
        configs = {
            'youtube': {
                'max_title': 100,
                'max_description': 500,
                'max_hashtags': 30,
                'cta': 'Смотрите полное видео на YouTube!',
                'tone': 'профессиональный'
            },
            'telegram': {
                'max_title': 100,
                'max_description': 1000,
                'max_hashtags': 20,
                'cta': 'Нажмите для просмотра',
                'tone': 'информативный'
            },
            'tiktok': {
                'max_title': 50,
                'max_description': 150,
                'max_hashtags': 15,
                'cta': 'Смотри больше!',
                'tone': 'энергичный'
            },
            'instagram': {
                'max_title': 60,
                'max_description': 300,
                'max_hashtags': 30,
                'cta': 'Ссылка в bio',
                'tone': 'визуальный'
            },
            'rutube': {
                'max_title': 100,
                'max_description': 500,
                'max_hashtags': 20,
                'cta': 'Смотрите на RuTube!',
                'tone': 'профессиональный'
            },
            'vk': {
                'max_title': 100,
                'max_description': 400,
                'max_hashtags': 15,
                'cta': 'Смотрите в нашей группе',
                'tone': 'дружелюбный'
            },
            'okru': {
                'max_title': 100,
                'max_description': 400,
                'max_hashtags': 15,
                'cta': 'Смотрите в нашей группе',
                'tone': 'дружелюбный'
            }
        }

        config = configs.get(platform, configs['youtube'])

        # Extract title and description
        title = video.title[:config['max_title']]
        description = self._truncate_description(
            video.description,
            config['max_description']
        )

        # Generate hashtags based on platform
        hashtags = self._generate_hashtags(video, platform, config['max_hashtags'])

        # Create post ID
        post_id = f"{video.video_id}_{platform}_{datetime.now().timestamp()}"

        post = SocialPost(
            post_id=post_id,
            video_id=video.video_id,
            platform=platform,
            title=title,
            description=description,
            hashtags=hashtags,
            cta=config['cta'],
            scheduled_publish_at=datetime.now(),
        )

        logger.debug(f"Generated {platform} post for {video.video_id}")
        return post

    def _truncate_description(self, description: str, max_length: int) -> str:
        """Truncate description with ellipsis"""
        if len(description) <= max_length:
            return description

        truncated = description[:max_length-3]
        # Truncate at last space
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]

        return truncated + "..."

    def _generate_hashtags(self, video: PublishedVideo,
                          platform: str, max_count: int) -> List[str]:
        """Generate hashtags based on video content"""
        base_hashtags = [
            '#славяноарийская',
            '#родноверие',
            '#славянскаякультура',
            '#обереги',
            '#волхвы',
            '#буквицы',
            '#славянскиеобряды',
            '#славянскиепраздники',
        ]

        # Platform-specific hashtags
        platform_hashtags = {
            'youtube': ['#видео', '#просмотр', '#культура'],
            'telegram': ['#канал', '#информация'],
            'tiktok': ['#тикток', '#тренд', '#viral'],
            'instagram': ['#инстаграм', '#красиво', '#вдохновение'],
            'rutube': ['#рутуб', '#видео', '#русское'],
            'vk': ['#группа', '#сообщество'],
            'okru': ['#одноклассники', '#сообщество'],
        }

        # Combine hashtags
        all_tags = base_hashtags + platform_hashtags.get(platform, [])

        # Remove duplicates and limit
        unique_tags = list(dict.fromkeys(all_tags))[:max_count]

        return unique_tags
