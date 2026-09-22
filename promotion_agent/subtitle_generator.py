"""Subtitle generator - creates subtitles from video audio using Whisper API"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class SubtitleGenerator:
    """Generates Russian subtitles from video audio"""

    def __init__(self, model: str = "base"):
        self.model = model
        self._check_whisper()

    def _check_whisper(self):
        """Check if Whisper is installed"""
        try:
            import openai
            logger.info("OpenAI Whisper available")
        except ImportError:
            logger.warning("openai not installed. Install with: pip install openai")

    def generate_subtitles(self, video_path: str,
                          output_path: Optional[str] = None,
                          language: str = "ru") -> Optional[str]:
        """
        Generate subtitles from video using Whisper API

        Args:
            video_path: Path to video file
            output_path: Path to save subtitle file (SRT format)
            language: Language code (default: ru for Russian)

        Returns:
            Path to generated subtitle file
        """
        try:
            import openai
            from openai import OpenAI

            video_file = Path(video_path)
            if not video_file.exists():
                logger.error(f"Video file not found: {video_path}")
                return None

            # Determine output path
            if not output_path:
                output_path = str(video_file.parent / f"{video_file.stem}.srt")

            logger.info(f"Generating subtitles for: {video_file.name}")

            # Open video file for Whisper API
            with open(video_file, 'rb') as audio_file:
                client = OpenAI()
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="srt"
                )

            # Write SRT file
            output_file = Path(output_path)
            output_file.write_text(transcript, encoding='utf-8')

            logger.info(f"Subtitles saved: {output_path}")
            return output_path

        except ImportError:
            logger.error("openai library not installed")
            return None
        except Exception as e:
            logger.error(f"Error generating subtitles: {e}")
            return None

    def generate_subtitles_batch(self, video_paths: list,
                                output_dir: str = None) -> dict:
        """
        Generate subtitles for multiple videos

        Args:
            video_paths: List of video file paths
            output_dir: Directory to save subtitle files

        Returns:
            Dict mapping video_path -> subtitle_path
        """
        results = {}

        for video_path in video_paths:
            output_path = None
            if output_dir:
                video_file = Path(video_path)
                output_path = str(Path(output_dir) / f"{video_file.stem}.srt")

            subtitle_path = self.generate_subtitles(video_path, output_path)
            if subtitle_path:
                results[video_path] = subtitle_path

        return results

    def parse_srt(self, srt_path: str) -> list:
        """
        Parse SRT subtitle file

        Args:
            srt_path: Path to SRT file

        Returns:
            List of subtitle entries with timing and text
        """
        try:
            srt_file = Path(srt_path)
            if not srt_file.exists():
                logger.error(f"SRT file not found: {srt_path}")
                return []

            content = srt_file.read_text(encoding='utf-8')
            entries = []

            # Parse SRT format
            blocks = content.strip().split('\n\n')
            for block in blocks:
                lines = block.strip().split('\n')
                if len(lines) >= 3:
                    entries.append({
                        'index': lines[0],
                        'timing': lines[1],
                        'text': '\n'.join(lines[2:])
                    })

            logger.info(f"Parsed {len(entries)} subtitle entries from {srt_path}")
            return entries

        except Exception as e:
            logger.error(f"Error parsing SRT file: {e}")
            return []

    def convert_srt_to_vtt(self, srt_path: str, output_path: str) -> Optional[str]:
        """
        Convert SRT subtitles to VTT format

        Args:
            srt_path: Path to input SRT file
            output_path: Path to output VTT file

        Returns:
            Path to VTT file if successful
        """
        try:
            srt_file = Path(srt_path)
            if not srt_file.exists():
                logger.error(f"SRT file not found: {srt_path}")
                return None

            content = srt_file.read_text(encoding='utf-8')

            # Convert SRT to VTT
            vtt_content = "WEBVTT\n\n"
            vtt_content += content.replace(',', '.')  # Replace comma with period in timestamps

            output_file = Path(output_path)
            output_file.write_text(vtt_content, encoding='utf-8')

            logger.info(f"Converted to VTT: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error converting SRT to VTT: {e}")
            return None
