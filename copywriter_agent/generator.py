"""Content generation using Claude API"""

import json
import logging
from typing import List, Dict, Optional
from anthropic import Anthropic

from scout_agent.types import AnalyzedVideo
from copywriter_agent.types import (
    ContentVariation,
    PlatformVersion,
    PersonaType,
    REQUIRED_PLATFORMS,
)
from copywriter_agent.config import CopywriterConfig

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates content variations using Claude API"""

    def __init__(self, config: CopywriterConfig):
        self.config = config
        self.client = Anthropic(api_key=config.claude_api_key)

    def generate(self, analyzed_video: AnalyzedVideo) -> List[ContentVariation]:
        """Generate 15 content variations for a video"""
        variations = []

        # Determine best personas for this video
        personas = self._select_personas(analyzed_video)

        logger.info(
            f"Generating {self.config.max_variations} variations for {analyzed_video.video.title} "
            f"with personas: {[p.value for p in personas]}"
        )

        # Generate variations
        for i in range(1, self.config.max_variations + 1):
            # Rotate through personas
            persona = personas[(i - 1) % len(personas)]

            # Generate variation content
            prompt = self._build_generation_prompt(analyzed_video, i, persona)

            try:
                response = self.client.messages.create(
                    model=self.config.model,
                    max_tokens=2000,
                    temperature=self.config.temperature,
                    messages=[{"role": "user", "content": prompt}]
                )

                # Parse response
                content_data = self._parse_response(response.content[0].text)

                # Create platform versions
                platform_versions = self._create_platform_versions(
                    content_data, analyzed_video
                )

                # Create variation
                variation = ContentVariation(
                    video_id=analyzed_video.video.youtube_id,
                    variation_number=i,
                    title=content_data.get("title", f"Variation {i}"),
                    hook=content_data.get("hook", ""),
                    description=content_data.get("description", ""),
                    hashtags=content_data.get("hashtags", []),
                    cta=content_data.get("cta", "Watch video"),
                    persona=persona,
                    ab_test_hypothesis=content_data.get(
                        "ab_hypothesis",
                        f"Test variation {i}"
                    ),
                    expected_improvement=float(
                        content_data.get("expected_improvement", 0.05)
                    ),
                    platform_versions=platform_versions,
                    confidence_score=float(
                        content_data.get("confidence", 0.7)
                    ),
                    model_version=self.config.model,
                    model_temperature=self.config.temperature,
                )

                variations.append(variation)
                logger.debug(f"Generated variation {i}/{self.config.max_variations}")

            except Exception as e:
                logger.error(f"Failed to generate variation {i}: {e}")
                # Continue with next variation

        logger.info(f"Generated {len(variations)} variations")
        return variations

    def _select_personas(self, video: AnalyzedVideo) -> List[PersonaType]:
        """Select appropriate personas based on video content and platforms"""
        personas = []

        # Default personas for platform types
        if "youtube" in video.recommended_for_platforms:
            if video.content_type == "tutorial":
                personas.extend([
                    PersonaType.YOUTUBE_TECH_PROFESSIONAL,
                    PersonaType.YOUTUBE_STUDENT,
                ])
            elif video.content_type == "vlog":
                personas.extend([
                    PersonaType.YOUTUBE_CASUAL_DEVELOPER,
                    PersonaType.YOUTUBE_MARKETER,
                ])

        if "tiktok" in video.recommended_for_platforms:
            personas.extend([
                PersonaType.TIKTOK_GEN_Z_DEVELOPER,
                PersonaType.TIKTOK_CASUAL_LEARNER,
            ])

        if "telegram" in video.recommended_for_platforms:
            personas.extend([
                PersonaType.TELEGRAM_COMMUNITY,
                PersonaType.TELEGRAM_SUBSCRIBER,
            ])

        # Fallback to general persona
        if not personas:
            personas = [PersonaType.GENERAL_TECH_PROFESSIONAL]

        # Remove duplicates while preserving order
        seen = set()
        unique_personas = []
        for p in personas:
            if p not in seen:
                unique_personas.append(p)
                seen.add(p)

        return unique_personas

    def _build_generation_prompt(
        self,
        video: AnalyzedVideo,
        index: int,
        persona: PersonaType
    ) -> str:
        """Build prompt for Claude to generate a variation"""

        viral_moments_desc = "\n".join([
            f"- {m.text_snippet} (confidence: {m.confidence:.1%})"
            for m in video.viral_moments[:3]
        ])

        return f"""Generate content variation #{index} of social media content for this video.

VIDEO INFO:
Title: {video.video.title}
Content Type: {video.content_type}
Viral Score: {video.overall_viral_score:.0f}/100
Key Takeaway: {video.key_takeaway}

TRANSCRIPT (first 300 chars):
{video.transcript.text[:300]}

VIRAL MOMENTS:
{viral_moments_desc}

TARGET AUDIENCE:
Persona: {persona.value}
Platforms: {', '.join(video.recommended_for_platforms)}

TASK:
Generate variation #{index} with unique angle. Create content that:
1. Appeals to the {persona.value} audience
2. Highlights a different aspect than other variations
3. Works across {', '.join(video.recommended_for_platforms)}

REQUIRED JSON FORMAT:
{{
  "title": "compelling title under 60 chars",
  "hook": "opening line to grab attention (10-100 chars)",
  "description": "full description (50-300 chars)",
  "hashtags": ["tag1", "tag2", ...],
  "cta": "call-to-action like 'Watch full video'",
  "ab_hypothesis": "why this variation works (e.g., 'Emotional hook appeals more')",
  "expected_improvement": 0.05,
  "confidence": 0.75
}}

Generate ONLY valid JSON, no other text."""

    def _parse_response(self, text: str) -> Dict:
        """Parse Claude's JSON response"""
        try:
            # Find JSON in response
            start = text.find('{')
            end = text.rfind('}') + 1

            if start < 0 or end <= start:
                raise ValueError("No JSON found in response")

            json_str = text[start:end]
            data = json.loads(json_str)

            # Validate required fields
            required = ['title', 'hook', 'description', 'hashtags', 'cta']
            for field in required:
                if field not in data:
                    data[field] = ""

            # Ensure hashtags is a list
            if isinstance(data.get('hashtags'), str):
                data['hashtags'] = [t.strip() for t in data['hashtags'].split(',')]

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            # Return minimal valid response
            return {
                "title": "Content Variation",
                "hook": "Discover something new",
                "description": "Watch this interesting content",
                "hashtags": ["content", "video"],
                "cta": "Watch video",
            }

    def _create_platform_versions(
        self,
        content: Dict,
        video: AnalyzedVideo
    ) -> Dict[str, PlatformVersion]:
        """Create platform-specific versions of content"""
        versions = {}

        for platform in video.recommended_for_platforms:
            aspect_ratio = self._get_aspect_ratio(platform)

            versions[platform] = PlatformVersion(
                platform=platform,
                title=content.get("title", "")[:100],
                description=content.get("description", "")[:500],
                hashtags=content.get("hashtags", [])[:10],
                media_aspect_ratio=aspect_ratio,
            )

        return versions

    @staticmethod
    def _get_aspect_ratio(platform: str) -> str:
        """Get optimal aspect ratio for platform"""
        ratios = {
            "youtube": "16:9",
            "tiktok": "9:16",
            "telegram": "9:16",
            "instagram": "9:16",
            "rutube": "16:9",
            "vk": "9:16",
            "okru": "9:16",
        }
        return ratios.get(platform, "1:1")
