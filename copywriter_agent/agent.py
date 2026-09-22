"""Main Copywriter Agent class"""

import logging
from typing import Optional

from scout_agent.types import AnalyzedVideo
from copywriter_agent.types import CopywriterResult
from copywriter_agent.config import CopywriterConfig
from copywriter_agent.pipeline import CopywriterPipeline

logger = logging.getLogger(__name__)


class CopywriterAgent:
    """
    Copywriter Agent: generates high-quality content variations for viral videos

    Usage:
        agent = CopywriterAgent()
        result = agent.process_video(analyzed_video)

        # Check if ready for publishing
        if result.is_ready_for_publishing():
            # Pass to Promotion Agent (Phase 2C)
            json_output = result.to_json()
    """

    def __init__(self, config: Optional[CopywriterConfig] = None):
        if config is None:
            config = CopywriterConfig.from_env()

        self.config = config
        self.pipeline = CopywriterPipeline(config)

        logger.info("CopywriterAgent initialized")

    def process_video(self, analyzed_video: AnalyzedVideo) -> CopywriterResult:
        """
        Process a video and generate content variations

        Args:
            analyzed_video: AnalyzedVideo from Scout Agent

        Returns:
            CopywriterResult with 15 variations and publishing recommendations

        Raises:
            ValueError: If content validation fails critically
        """
        logger.info(f"Processing video: {analyzed_video.video.title}")

        result = self.pipeline.process(analyzed_video)

        # Check if ready for Phase 2C
        if not result.is_ready_for_publishing():
            validation = result.validate_all()
            errors = validation["errors"]
            logger.warning(f"Content not ready for publishing. Errors: {errors}")
            # Don't raise - let Phase 2C decide whether to proceed

        return result

    def run_interactive(self):
        """Interactive mode for testing"""
        print("\n🎬 Copywriter Agent - Interactive Mode")
        print("=" * 50)
        print("This mode is for testing. In production, use process_video()")
        print("Current configuration:")
        print(f"  Model: {self.config.model}")
        print(f"  Temperature: {self.config.temperature}")
        print(f"  Max variations: {self.config.max_variations}")
        print()
        print("Ready to process videos from Scout Agent.")
