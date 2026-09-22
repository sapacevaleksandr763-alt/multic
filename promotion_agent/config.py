"""Configuration for Promotion Agent"""

from dataclasses import dataclass
import os


@dataclass
class PromotionConfig:
    """Configuration for Promotion Agent"""

    # API Keys
    youtube_api_key: str
    telegram_bot_token: str
    claude_api_key: str

    # Paths
    base_download_path: str = "C:\\Users\\Alex\\Downloads\\rutube-videos"
    found_videos_path: str = "C:\\Users\\Alex\\Downloads\\rutube-videos\\found"
    published_videos_path: str = "C:\\Users\\Alex\\Downloads\\rutube-videos\\Опубликовано"

    # Configuration
    publish_interval_days: int = 3
    post_delay_hours: int = 24

    # Search
    search_keywords: list = None
    search_channels: list = None
    search_hashtags: list = None

    # Video processing
    whisper_model: str = "base"
    subtitle_language: str = "ru"
    max_video_duration_seconds: int = 120

    def __post_init__(self):
        """Validate and set defaults"""
        if not self.youtube_api_key:
            raise ValueError("YOUTUBE_API_KEY required")
        if not self.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN required")
        if not self.claude_api_key:
            raise ValueError("CLAUDE_API_KEY required")

        # Set default search parameters
        if self.search_keywords is None:
            self.search_keywords = [
                "Славяно-арийская", "славянская культура", "обереги",
                "славянские обряды", "славянские праздники", "буквицы",
                "родноверие", "волхвы", "Трехлебов", "Хиневищ"
            ]

        if self.search_channels is None:
            self.search_channels = [
                "Школа Родноверов", "Волхвы", "Славянская культура",
                "Трехлебов", "Хиневищ", "Родноверие"
            ]

        if self.search_hashtags is None:
            self.search_hashtags = [
                "#славяноарийская", "#родноверие", "#волхвы",
                "#славянскаякультура", "#обереги", "#буквицы",
                "#славянскиеобряды", "#славянскиепраздники"
            ]

    @classmethod
    def from_env(cls) -> "PromotionConfig":
        """Load configuration from environment variables"""
        youtube_key = os.getenv("YOUTUBE_API_KEY")
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        claude_key = os.getenv("CLAUDE_API_KEY")

        if not youtube_key:
            raise ValueError("YOUTUBE_API_KEY not set in environment")
        if not telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")
        if not claude_key:
            raise ValueError("CLAUDE_API_KEY not set in environment")

        return cls(
            youtube_api_key=youtube_key,
            telegram_bot_token=telegram_token,
            claude_api_key=claude_key,
            base_download_path=os.getenv(
                "PROMOTION_BASE_PATH",
                "C:\\Users\\Alex\\Downloads\\rutube-videos"
            ),
        )
