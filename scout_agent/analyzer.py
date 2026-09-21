"""Viral content analysis using Claude"""

import logging
import json
from typing import List, Optional
from .types import (
    YouTubeVideo, Transcript, AnalyzedVideo,
    ViralMoment, ScoutResult
)

logger = logging.getLogger(__name__)

class ViralAnalyzer:
    """Analyze video for viral potential using Claude"""

    def __init__(self, claude_api_key: str):
        self.claude_api_key = claude_api_key
        self._setup_claude()

    def _setup_claude(self):
        """Initialize Claude client"""
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.claude_api_key)
        except ImportError:
            logger.warning("anthropic library not installed")
            self.client = None

    def analyze(self, video: YouTubeVideo, transcript: Transcript) -> AnalyzedVideo:
        """Analyze video for viral moments and scoring"""
        if not self.client:
            raise RuntimeError("Claude API not available")

        # Detect content type
        content_type = self._detect_content_type(transcript)

        # Extract viral moments
        viral_moments = self._extract_viral_moments(transcript, content_type)

        # Calculate overall score
        overall_score = self._calculate_viral_score(
            video, transcript, viral_moments, content_type
        )

        # Get key takeaway
        key_takeaway = self._summarize_content(transcript)

        # Recommend platforms
        platforms = self._recommend_platforms(content_type, overall_score)

        analyzed = AnalyzedVideo(
            video=video,
            transcript=transcript,
            viral_moments=viral_moments,
            overall_viral_score=overall_score,
            content_type=content_type,
            key_takeaway=key_takeaway,
            recommended_for_platforms=platforms
        )

        return analyzed

    def _detect_content_type(self, transcript: Transcript) -> str:
        """Detect content type using Claude"""
        if not self.client:
            return "unknown"

        prompt = f"""Analyze this transcript and classify into ONE category:
- tutorial: Step-by-step instructions
- interview: Q&A with guest
- vlog: Personal story/experience
- podcast: Long-form discussion
- news: Current events/updates
- debate: Opposing viewpoints
- education: Learning content
- commentary: Opinion/analysis
- comedy: Entertainment/humor
- other: Something else

Transcript (first 500 chars):
{transcript.text[:500]}

Respond with ONLY the category name."""

        response = self.client.messages.create(
            model="claude-opus-5",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip().lower()

    def _extract_viral_moments(
        self, transcript: Transcript, content_type: str
    ) -> List[ViralMoment]:
        """Extract viral-worthy moments from transcript"""
        if not self.client:
            return []

        prompt = f"""Find 3-5 viral moments in this transcript that could go viral on TikTok/YouTube Shorts.

Content type: {content_type}
Transcript:
{transcript.text[:2000]}

For each moment, identify:
1. The exact quote/section (30-60 seconds of content)
2. Why it's viral (emotional peak, controversy, humor, insight, etc.)
3. Confidence (0-1)

Return as JSON:
[{{"start": 120, "end": 150, "text": "...", "factors": ["factor1"], "confidence": 0.9}}]"""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text.strip()
            # Extract JSON from response
            start = text.find('[')
            end = text.rfind(']') + 1
            if start >= 0 and end > start:
                data = json.loads(text[start:end])

                moments = []
                for item in data:
                    moment = ViralMoment(
                        start_time=float(item.get('start', 0)),
                        end_time=float(item.get('end', 0)),
                        text_snippet=item.get('text', ''),
                        viral_factors=item.get('factors', []),
                        confidence=float(item.get('confidence', 0.5))
                    )
                    moments.append(moment)

                return moments
        except Exception as e:
            logger.error(f"Failed to extract viral moments: {e}")

        return []

    def _calculate_viral_score(
        self, video: YouTubeVideo, transcript: Transcript,
        viral_moments: List[ViralMoment], content_type: str
    ) -> float:
        """Calculate overall viral score (0-100)"""
        if not self.client:
            return 50.0

        prompt = f"""Rate the viral potential of this video (0-100):

Title: {video.title}
Channel: {video.channel}
Views: {video.view_count:,}
Duration: {video.duration_seconds}s
Content type: {content_type}
Key moments found: {len(viral_moments)}

Transcript excerpt:
{transcript.text[:1000]}

Consider:
- Hooks (opening line captures attention)
- Emotional peaks (high energy/emotion)
- Quotable lines (memorable phrases)
- Controversy/opinion (strong takes)
- Practical value (useful info)
- Entertainment (fun/engaging)
- Trend alignment (current topics)

Respond with ONLY a number 0-100."""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )

            score = float(response.content[0].text.strip())
            return min(100, max(0, score))
        except Exception as e:
            logger.error(f"Score calculation failed: {e}")
            return 50.0

    def _summarize_content(self, transcript: Transcript) -> str:
        """Get key takeaway from content"""
        if not self.client:
            return "No summary available"

        prompt = f"""Summarize the key takeaway in 1 sentence (under 20 words):

{transcript.text[:1000]}

Respond with ONLY the summary."""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=30,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text.strip()
        except Exception as e:
            logger.warning(f"Summary failed: {e}")
            return "Content summary unavailable"

    def _recommend_platforms(self, content_type: str, score: float) -> List[str]:
        """Recommend target platforms based on content"""
        platforms = []

        # High-quality content goes to all platforms
        if score >= 75:
            platforms = ["youtube", "tiktok", "telegram", "instagram"]
        elif score >= 60:
            platforms = ["tiktok", "telegram", "instagram"]
        else:
            platforms = ["telegram"]

        # Adjust by content type
        if content_type in ["tutorial", "education"]:
            if "youtube" not in platforms:
                platforms.insert(0, "youtube")

        if content_type in ["comedy", "vlog"]:
            if "tiktok" not in platforms:
                platforms.insert(0, "tiktok")

        return platforms
