"""Integration tests for Scout Agent"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from scout_agent.agent import ScoutAgent
from scout_agent.config import ScoutConfig
from scout_agent.types import YouTubeVideo, Transcript


class TestScoutAgentIntegration:
    """Integration tests for ScoutAgent"""

    def test_agent_initialization(self):
        """Test Scout Agent initialization"""
        config = ScoutConfig(
            youtube_api_key="test_key",
            max_results=5
        )
        agent = ScoutAgent(config=config)

        assert agent.config.youtube_api_key == "test_key"
        assert agent.config.max_results == 5

    def test_agent_finds_videos(self):
        """Test that agent can find videos (mocked)"""
        config = ScoutConfig(youtube_api_key="test_key")
        agent = ScoutAgent(config=config)

        # Mock the pipeline
        with patch.object(agent.pipeline, 'find_viral_videos') as mock_find:
            # Create mock result
            video = YouTubeVideo(
                youtube_id="test123",
                title="Test Video",
                channel="Test Channel",
                view_count=1000,
                published_at=datetime.now(),
                duration_seconds=600
            )

            from scout_agent.types import AnalyzedVideo, ScoutResult
            analyzed = AnalyzedVideo(
                video=video,
                transcript=Transcript(youtube_id="test123", text="Test"),
                viral_moments=[],
                overall_viral_score=75.0,
                content_type="tutorial",
                key_takeaway="Test takeaway"
            )

            result = ScoutResult(
                query="test",
                videos=[video],
                analyzed_videos=[analyzed],
                top_candidates=[analyzed]
            )

            mock_find.return_value = result

            # Call agent
            results = agent.find_viral_videos("test query")

            assert len(results.top_candidates) == 1
            assert results.top_candidates[0].overall_viral_score == 75.0
            mock_find.assert_called_once_with("test query")


class TestPipelineFlow:
    """Test the pipeline flow"""

    @patch('scout_agent.downloader.YouTubeDownloader')
    @patch('scout_agent.transcriber.WhisperTranscriber')
    @patch('scout_agent.analyzer.ViralAnalyzer')
    def test_pipeline_orchestration(self, mock_analyzer_class, mock_transcriber_class, mock_downloader_class):
        """Test that pipeline calls components in order"""
        config = ScoutConfig(youtube_api_key="test_key")

        # Setup mocks
        mock_downloader = Mock()
        mock_transcriber = Mock()
        mock_analyzer = Mock()

        mock_downloader_class.return_value = mock_downloader
        mock_transcriber_class.return_value = mock_transcriber
        mock_analyzer_class.return_value = mock_analyzer

        # Create mock video
        video = YouTubeVideo(
            youtube_id="test123",
            title="Test",
            channel="Channel",
            view_count=1000,
            published_at=datetime.now(),
            duration_seconds=600
        )

        mock_downloader.search.return_value = [video]
        mock_transcriber.batch_transcribe.return_value = {
            "test123": Transcript(youtube_id="test123", text="Test transcript")
        }

        from scout_agent.types import AnalyzedVideo
        analyzed = AnalyzedVideo(
            video=video,
            transcript=Transcript(youtube_id="test123", text="Test"),
            viral_moments=[],
            overall_viral_score=75.0,
            content_type="tutorial",
            key_takeaway="Test"
        )
        mock_analyzer.analyze.return_value = analyzed

        # Run pipeline
        from scout_agent.pipeline import ScoutPipeline
        pipeline = ScoutPipeline(config)
        results = pipeline.find_viral_videos("test query")

        # Verify calls
        mock_downloader.search.assert_called_once()
        mock_transcriber.batch_transcribe.assert_called_once()
        mock_analyzer.analyze.assert_called_once()
