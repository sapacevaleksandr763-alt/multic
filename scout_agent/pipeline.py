"""Scout Agent pipeline orchestration"""

import logging
from typing import List, Optional
from .config import ScoutConfig
from .types import YouTubeVideo, Transcript, AnalyzedVideo, ScoutResult
from .downloader import YouTubeDownloader
from .transcriber import WhisperTranscriber
from .analyzer import ViralAnalyzer

logger = logging.getLogger(__name__)

class ScoutPipeline:
    """Main Scout Agent pipeline"""

    def __init__(self, config: ScoutConfig):
        self.config = config
        self.downloader = YouTubeDownloader(config.youtube_api_key)
        self.transcriber = WhisperTranscriber(
            model=config.whisper_model,
            language=config.language
        )
        self.analyzer = ViralAnalyzer(config.youtube_api_key)  # Using API key for Claude

    def find_viral_videos(self, query: str) -> ScoutResult:
        """
        Main entry point: find viral videos for a topic

        Pipeline:
        1. Search YouTube for videos
        2. Transcribe audio
        3. Analyze virality
        4. Rank by viral score
        5. Return top N candidates
        """
        logger.info(f"Starting Scout Agent: searching for '{query}'")

        # Step 1: Search
        logger.info("Step 1/5: Searching YouTube...")
        videos = self.downloader.search(
            query,
            max_results=self.config.youtube_max_results
        )
        logger.info(f"Found {len(videos)} videos")

        if not videos:
            return ScoutResult(
                query=query,
                videos=[],
                analyzed_videos=[],
                top_candidates=[]
            )

        # Step 2: Transcribe
        logger.info("Step 2/5: Transcribing audio...")
        transcripts = self.transcriber.batch_transcribe(videos)

        # Step 3: Analyze
        logger.info("Step 3/5: Analyzing virality...")
        analyzed_videos = []
        for video in videos:
            transcript = transcripts.get(video.youtube_id)
            if not transcript:
                logger.warning(f"No transcript for {video.youtube_id}, skipping")
                continue

            try:
                analyzed = self.analyzer.analyze(video, transcript)
                analyzed_videos.append(analyzed)
            except Exception as e:
                logger.error(f"Failed to analyze {video.youtube_id}: {e}")
                continue

        logger.info(f"Analyzed {len(analyzed_videos)} videos")

        # Step 4: Rank
        logger.info("Step 4/5: Ranking by viral score...")
        ranked = sorted(
            analyzed_videos,
            key=lambda v: v.overall_viral_score,
            reverse=True
        )

        # Step 5: Return top candidates
        logger.info("Step 5/5: Preparing results...")
        top_candidates = ranked[:self.config.max_results]

        result = ScoutResult(
            query=query,
            videos=videos,
            analyzed_videos=analyzed_videos,
            top_candidates=top_candidates
        )

        logger.info(f"Scout Agent complete: {len(top_candidates)} viral candidates found")
        return result
