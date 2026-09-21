"""Type definitions for Scout Agent"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class YouTubeVideo:
    """YouTube video metadata"""
    youtube_id: str
    title: str
    channel: str
    view_count: int
    published_at: datetime
    duration_seconds: int
    description: str = ""
    url: str = ""
    thumbnail_url: str = ""

    def __post_init__(self):
        if not self.url:
            self.url = f"https://www.youtube.com/watch?v={self.youtube_id}"

@dataclass
class Transcript:
    """Video transcript with timestamps"""
    youtube_id: str
    text: str
    segments: List[dict] = field(default_factory=list)  # [{start, end, text}, ...]
    language: str = "en"

@dataclass
class ViralMoment:
    """A moment in the video that could go viral"""
    start_time: float  # seconds
    end_time: float
    text_snippet: str
    viral_factors: List[str]  # ["opinion_bomb", "emotional_peak", etc]
    confidence: float  # 0-1

@dataclass
class AnalyzedVideo:
    """Video with viral analysis"""
    video: YouTubeVideo
    transcript: Transcript
    viral_moments: List[ViralMoment]
    overall_viral_score: float  # 0-100
    content_type: str  # "tutorial", "vlog", "podcast", "news", etc
    key_takeaway: str
    recommended_for_platforms: List[str] = field(default_factory=list)  # youtube, tiktok, telegram

@dataclass
class ScoutResult:
    """Final result from Scout Agent"""
    query: str
    videos: List[YouTubeVideo]
    analyzed_videos: List[AnalyzedVideo]
    top_candidates: List[AnalyzedVideo]  # sorted by viral_score, top N
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "query": self.query,
            "timestamp": self.timestamp.isoformat(),
            "candidates_found": len(self.videos),
            "top_candidates": [
                {
                    "youtube_id": v.video.youtube_id,
                    "title": v.video.title,
                    "viral_score": v.overall_viral_score,
                    "content_type": v.content_type,
                    "key_moments": len(v.viral_moments),
                    "platforms": v.recommended_for_platforms,
                    "url": v.video.url,
                }
                for v in self.top_candidates
            ]
        }
