"""Scout Agent: Find viral videos from YouTube"""

import logging
from typing import Optional
from .config import ScoutConfig
from .pipeline import ScoutPipeline
from .types import ScoutResult

logger = logging.getLogger(__name__)

class ScoutAgent:
    """
    Scout Agent finds viral video candidates from YouTube

    Usage:
        scout = ScoutAgent()
        results = scout.find_viral_videos("AI coding tutorials")
        for video in results.top_candidates:
            print(f"{video.video.title}: {video.overall_viral_score}")
    """

    def __init__(self, config: Optional[ScoutConfig] = None):
        if config is None:
            config = ScoutConfig.from_env()

        self.config = config
        self.pipeline = ScoutPipeline(config)

        # Setup logging
        logging.basicConfig(
            level=getattr(logging, config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def find_viral_videos(self, query: str) -> ScoutResult:
        """
        Find viral video candidates for a topic

        Args:
            query: Search query (e.g., "AI coding tutorials")

        Returns:
            ScoutResult with top viral candidates
        """
        return self.pipeline.find_viral_videos(query)

    def run_interactive(self):
        """Interactive mode for testing"""
        print("\n🎬 Scout Agent - Find Viral Videos")
        print("=" * 50)

        while True:
            query = input("\nEnter search query (or 'quit' to exit): ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not query:
                print("Please enter a valid query")
                continue

            try:
                results = self.find_viral_videos(query)

                print(f"\n📊 Results for '{query}':")
                print(f"Total videos found: {len(results.videos)}")
                print(f"Videos analyzed: {len(results.analyzed_videos)}")
                print(f"Top candidates: {len(results.top_candidates)}\n")

                if not results.top_candidates:
                    print("No viral candidates found.")
                    continue

                for i, video in enumerate(results.top_candidates, 1):
                    print(f"{i}. {video.video.title}")
                    print(f"   Channel: {video.video.channel}")
                    print(f"   Views: {video.video.view_count:,}")
                    print(f"   Viral Score: {video.overall_viral_score:.1f}/100")
                    print(f"   Content Type: {video.content_type}")
                    print(f"   Key Takeaway: {video.key_takeaway}")
                    print(f"   Platforms: {', '.join(video.recommended_for_platforms)}")
                    print(f"   Viral Moments: {len(video.viral_moments)}")
                    print(f"   URL: {video.video.url}")
                    print()

            except KeyboardInterrupt:
                print("\nInterrupted")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"Error: {e}")


if __name__ == "__main__":
    agent = ScoutAgent()
    agent.run_interactive()
