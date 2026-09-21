"""Configuration for Scout Agent"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class ScoutConfig:
    """Scout Agent configuration"""

    # YouTube API
    youtube_api_key: str = ""
    youtube_max_results: int = 20

    # Whisper transcription
    whisper_model: str = "base"  # tiny, base, small, medium, large
    language: Optional[str] = "en"

    # Viral analysis
    min_viral_score: float = 0.6  # 0-1 scale
    max_results: int = 5

    # Caching
    cache_dir: str = "./cache"
    cache_transcripts: bool = True

    # Logging
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "ScoutConfig":
        """Load config from environment variables"""
        import os
        return cls(
            youtube_api_key=os.getenv("YOUTUBE_API_KEY", ""),
            whisper_model=os.getenv("WHISPER_MODEL", "base"),
            language=os.getenv("LANGUAGE", "en"),
            min_viral_score=float(os.getenv("MIN_VIRAL_SCORE", "0.6")),
            max_results=int(os.getenv("MAX_RESULTS", "5")),
        )
