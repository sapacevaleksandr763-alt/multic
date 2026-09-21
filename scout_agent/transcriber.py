"""Audio transcription using Whisper"""

import logging
from typing import Optional, List
from .types import Transcript, YouTubeVideo

logger = logging.getLogger(__name__)

class WhisperTranscriber:
    """Transcribe audio using OpenAI Whisper"""

    def __init__(self, model: str = "base", language: Optional[str] = "en"):
        self.model = model
        self.language = language
        self._setup_whisper()

    def _setup_whisper(self):
        """Initialize Whisper model"""
        try:
            import whisper
            self.whisper_model = whisper.load_model(self.model)
        except ImportError:
            logger.warning("whisper not installed, using fallback")
            self.whisper_model = None

    def get_transcript(self, video: YouTubeVideo) -> Transcript:
        """Get transcript for a video"""
        if not self.whisper_model:
            raise RuntimeError("Whisper not available")

        try:
            # Download audio from video
            audio_path = self._download_audio(video)

            # Transcribe
            result = self.whisper_model.transcribe(
                audio_path,
                language=self.language,
                verbose=False
            )

            # Parse segments
            segments = []
            for segment in result.get('segments', []):
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip()
                })

            transcript = Transcript(
                youtube_id=video.youtube_id,
                text=result['text'],
                segments=segments,
                language=self.language or result.get('language', 'en')
            )

            return transcript

        except Exception as e:
            logger.error(f"Transcription failed for {video.youtube_id}: {e}")
            raise

    def _download_audio(self, video: YouTubeVideo) -> str:
        """Download audio from YouTube video"""
        try:
            import yt_dlp
            import tempfile
            import os

            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, f"{video.youtube_id}.mp3")

            if os.path.exists(audio_path):
                return audio_path

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(temp_dir, '%(id)s'),
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video.url])

            return audio_path

        except ImportError:
            raise RuntimeError("yt-dlp not installed")
        except Exception as e:
            logger.error(f"Audio download failed: {e}")
            raise

    def batch_transcribe(self, videos: List[YouTubeVideo]) -> dict:
        """Transcribe multiple videos"""
        transcripts = {}
        for video in videos:
            try:
                transcript = self.get_transcript(video)
                transcripts[video.youtube_id] = transcript
            except Exception as e:
                logger.error(f"Failed to transcribe {video.youtube_id}: {e}")
                transcripts[video.youtube_id] = None

        return transcripts
