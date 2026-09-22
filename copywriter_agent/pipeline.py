"""Pipeline orchestration for Copywriter Agent"""

import logging
from typing import List

from scout_agent.types import AnalyzedVideo
from copywriter_agent.types import (
    CopywriterResult,
    PublishingRecommendation,
    VariationSelection,
    PublishTimeOptimal,
)
from copywriter_agent.generator import ContentGenerator
from copywriter_agent.config import CopywriterConfig

logger = logging.getLogger(__name__)


class CopywriterPipeline:
    """Orchestrates content generation and publishing recommendations"""

    def __init__(self, config: CopywriterConfig):
        self.config = config
        self.generator = ContentGenerator(config)

    def process(self, video: AnalyzedVideo) -> CopywriterResult:
        """Main pipeline: generate → validate → recommend → output"""

        logger.info(f"Processing video: {video.video.title}")

        # Step 1: Generate variations
        logger.debug("Step 1: Generating content variations...")
        variations = self.generator.generate(video)

        # Step 2: Validate variations
        logger.debug("Step 2: Validating variations...")
        valid_count = sum(1 for v in variations if v.is_valid())
        logger.info(f"Valid variations: {valid_count}/{len(variations)}")

        # Step 3: Create publishing recommendations
        logger.debug("Step 3: Creating publishing recommendations...")
        recommendations = self._create_recommendations(variations, video)

        # Step 4: Create result
        result = CopywriterResult(
            video_id=video.video.youtube_id,
            video_title=video.video.title,
            viral_score=video.overall_viral_score,
            variations=variations,
            publishing_recommendations=recommendations,
            model_version=self.config.model,
        )

        # Final validation
        result.validate_all()
        ready = result.is_ready_for_publishing()
        logger.info(f"Result ready for publishing: {ready}")

        return result

    def _create_recommendations(
        self,
        variations,
        video: AnalyzedVideo
    ) -> List[PublishingRecommendation]:
        """Create publishing recommendations for each platform"""
        recommendations = []

        for platform in video.recommended_for_platforms:
            # Find variations with this platform
            platform_variations = [
                v for v in variations
                if platform in v.platform_versions and v.is_valid()
            ]

            if not platform_variations:
                logger.warning(f"No valid variations for platform: {platform}")
                continue

            # Sort by quality score (descending)
            ranked = sorted(
                platform_variations,
                key=lambda v: v.validate().quality_score,
                reverse=True
            )

            # Select top 3 (or fewer if less available)
            top_3 = ranked[:3]

            # Create selections with priority
            selections = [
                VariationSelection(
                    variation_id=v.id,
                    priority=i + 1,
                    reason=f"Quality: {v.validate().quality_score:.1%} | "
                           f"Confidence: {v.confidence_score:.1%}"
                )
                for i, v in enumerate(top_3)
            ]

            # Create recommendation
            rec = PublishingRecommendation(
                platform=platform,
                variations=selections,
                publish_time=self._optimal_publish_time(platform, video),
                expected_reach=self._estimate_reach(platform, video),
                expected_engagement_rate=self._estimate_engagement(platform, video),
                confidence=self._recommendation_confidence(platform, video),
                notes=self._generate_notes(platform, video, top_3),
            )

            recommendations.append(rec)
            logger.debug(f"Created recommendation for {platform}")

        return recommendations

    @staticmethod
    def _optimal_publish_time(platform: str, video: AnalyzedVideo) -> PublishTimeOptimal:
        """Determine optimal publish time for platform"""
        # YouTube: morning (tech people check before work)
        if platform == "youtube":
            return PublishTimeOptimal.MORNING

        # TikTok: midday (lunch break scrolling)
        if platform == "tiktok":
            return PublishTimeOptimal.MIDDAY

        # Telegram: evening (leisure time)
        if platform == "telegram":
            return PublishTimeOptimal.EVENING

        # Instagram: evening
        if platform == "instagram":
            return PublishTimeOptimal.EVENING

        return PublishTimeOptimal.ANYTIME

    @staticmethod
    def _estimate_reach(platform: str, video: AnalyzedVideo) -> int:
        """Estimate reach based on platform and video viral score"""
        base_reach = {
            "youtube": 5000,
            "tiktok": 10000,
            "telegram": 2000,
            "instagram": 3000,
            "rutube": 1000,
            "vk": 2000,
            "okru": 500,
        }

        base = base_reach.get(platform, 1000)
        # Scale by viral score (0-100)
        multiplier = video.overall_viral_score / 50  # 85 → 1.7x multiplier

        return int(base * multiplier)

    @staticmethod
    def _estimate_engagement(platform: str, video: AnalyzedVideo) -> float:
        """Estimate engagement rate by platform"""
        base_engagement = {
            "youtube": 0.03,  # 3%
            "tiktok": 0.08,   # 8%
            "telegram": 0.12,  # 12%
            "instagram": 0.05,  # 5%
        }

        base = base_engagement.get(platform, 0.03)
        # Boost by viral score
        boost = (video.overall_viral_score / 100) * 0.05

        return min(0.30, base + boost)  # Cap at 30%

    @staticmethod
    def _recommendation_confidence(platform: str, video: AnalyzedVideo) -> float:
        """Confidence in this platform recommendation"""
        # Higher confidence for platforms in recommended list
        base_confidence = 0.75

        # Boost if viral score is high
        if video.overall_viral_score >= 80:
            base_confidence += 0.15
        elif video.overall_viral_score < 60:
            base_confidence -= 0.1

        return min(0.95, max(0.5, base_confidence))

    @staticmethod
    def _generate_notes(platform: str, video: AnalyzedVideo, top_variations) -> str:
        """Generate notes about this recommendation"""
        if not top_variations:
            return f"No valid variations for {platform}"

        top = top_variations[0]
        top_quality = top.validate().quality_score

        notes = f"Top variation quality: {top_quality:.1%}"

        if video.content_type == "tutorial" and platform == "youtube":
            notes += " | Strong for tutorial audience"

        if video.overall_viral_score >= 80:
            notes += " | High viral potential"

        return notes
