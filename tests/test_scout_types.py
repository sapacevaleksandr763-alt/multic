"""Tests for Scout Agent type definitions"""

import pytest
from datetime import datetime
from scout_agent.types import (
    YouTubeVideo, Transcript, ViralMoment,
    AnalyzedVideo, ScoutResult
)


class TestYouTubeVideo:
    """Tests for YouTubeVideo dataclass"""

    def test_creation(self):
        """Test creating a YouTubeVideo"""
        video = YouTubeVideo(
            youtube_id="test123",
            title="Test Video",
            channel="Test Channel",
            view_count=1000,
            published_at=datetime.now(),
            duration_seconds=600
        )
        assert video.youtube_id == "test123"
        assert video.view_count == 1000

    def test_url_generation(self):
        """Test automatic URL generation"""
        video = YouTubeVideo(
            youtube_id="abc123",
            title="Test",
            channel="Channel",
            view_count=0,
            published_at=datetime.now(),
            duration_seconds=0
        )
        assert video.url == "https://www.youtube.com/watch?v=abc123"

    def test_url_override(self):
        """Test that custom URL is not overridden"""
        custom_url = "https://custom.com/video"
        video = YouTubeVideo(
            youtube_id="abc123",
            title="Test",
            channel="Channel",
            view_count=0,
            published_at=datetime.now(),
            duration_seconds=0,
            url=custom_url
        )
        assert video.url == custom_url


class TestTranscript:
    """Tests for Transcript dataclass"""

    def test_creation(self):
        """Test creating a Transcript"""
        transcript = Transcript(
            youtube_id="test123",
            text="This is a test transcript",
            segments=[
                {"start": 0, "end": 5, "text": "This is"},
                {"start": 5, "end": 10, "text": "a test"}
            ]
        )
        assert transcript.youtube_id == "test123"
        assert len(transcript.segments) == 2


class TestViralMoment:
    """Tests for ViralMoment dataclass"""

    def test_creation(self):
        """Test creating a ViralMoment"""
        moment = ViralMoment(
            start_time=10.5,
            end_time=30.0,
            text_snippet="Amazing quote",
            viral_factors=["opinion_bomb", "emotional"],
            confidence=0.85
        )
        assert moment.start_time == 10.5
        assert len(moment.viral_factors) == 2


class TestAnalyzedVideo:
    """Tests for AnalyzedVideo dataclass"""

    def test_creation(self):
        """Test creating an AnalyzedVideo"""
        video = YouTubeVideo(
            youtube_id="test123",
            title="Test",
            channel="Channel",
            view_count=0,
            published_at=datetime.now(),
            duration_seconds=0
        )
        transcript = Transcript(
            youtube_id="test123",
            text="Test transcript"
        )
        moment = ViralMoment(
            start_time=0,
            end_time=10,
            text_snippet="Test",
            viral_factors=["test"],
            confidence=0.9
        )

        analyzed = AnalyzedVideo(
            video=video,
            transcript=transcript,
            viral_moments=[moment],
            overall_viral_score=85.0,
            content_type="tutorial",
            key_takeaway="Learn something new",
            recommended_for_platforms=["youtube", "tiktok"]
        )

        assert analyzed.overall_viral_score == 85.0
        assert analyzed.content_type == "tutorial"


class TestScoutResult:
    """Tests for ScoutResult dataclass"""

    def test_creation(self):
        """Test creating a ScoutResult"""
        result = ScoutResult(
            query="test query",
            videos=[],
            analyzed_videos=[],
            top_candidates=[]
        )
        assert result.query == "test query"
        assert len(result.top_candidates) == 0

    def test_to_dict(self):
        """Test converting to dictionary"""
        video = YouTubeVideo(
            youtube_id="test123",
            title="Test",
            channel="Channel",
            view_count=1000,
            published_at=datetime.now(),
            duration_seconds=600
        )
        transcript = Transcript(
            youtube_id="test123",
            text="Test"
        )

        analyzed = AnalyzedVideo(
            video=video,
            transcript=transcript,
            viral_moments=[],
            overall_viral_score=80.0,
            content_type="tutorial",
            key_takeaway="Test",
            recommended_for_platforms=["youtube"]
        )

        result = ScoutResult(
            query="test",
            videos=[video],
            analyzed_videos=[analyzed],
            top_candidates=[analyzed]
        )

        data = result.to_dict()
        assert data["query"] == "test"
        assert data["candidates_found"] == 1
        assert len(data["top_candidates"]) == 1
        assert data["top_candidates"][0]["viral_score"] == 80.0
