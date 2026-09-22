"""Video downloader - downloads found videos for review"""

import os
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import subprocess

logger = logging.getLogger(__name__)


@dataclass
class DownloadedVideo:
    """Info about downloaded video"""
    video_id: str
    file_path: str
    file_size_mb: float
    url: str
    title: str
    duration_seconds: int

    def __post_init__(self):
        """Verify file exists"""
        if not Path(self.file_path).exists():
            raise FileNotFoundError(f"Downloaded file not found: {self.file_path}")


class VideoDownloader:
    """Downloads videos from URLs using yt-dlp"""

    def __init__(self, download_path: str):
        self.download_path = Path(download_path)
        self.download_path.mkdir(parents=True, exist_ok=True)

        # Check if yt-dlp is installed
        self._check_ytdlp()

    def _check_ytdlp(self):
        """Check if yt-dlp is installed"""
        try:
            import yt_dlp
            logger.info(f"yt-dlp version: {yt_dlp.version.__version__}")
        except ImportError:
            logger.warning("yt-dlp not installed. Install with: pip install yt-dlp")

    def download_video(self, url: str, title: str, video_id: str,
                       audio_only: bool = False) -> Optional[DownloadedVideo]:
        """
        Download video from URL

        Args:
            url: Video URL
            title: Video title (for filename)
            video_id: Unique video ID
            audio_only: Download audio only

        Returns:
            DownloadedVideo object if successful, None otherwise
        """
        try:
            import yt_dlp

            # Sanitize filename
            safe_title = self._sanitize_filename(title)
            output_path = self.download_path / f"{video_id}_{safe_title}.%(ext)s"

            logger.info(f"Downloading video: {title} from {url}")

            ydl_opts = {
                'format': 'best' if not audio_only else 'bestaudio',
                'outtmpl': str(output_path),
                'quiet': False,
                'no_warnings': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                # Find downloaded file
                file_path = self._find_downloaded_file(video_id, safe_title)

                if file_path:
                    file_size_mb = file_path.stat().st_size / (1024 * 1024)
                    duration = int(info.get('duration', 0))

                    logger.info(f"Downloaded: {file_path.name} ({file_size_mb:.1f} MB)")

                    return DownloadedVideo(
                        video_id=video_id,
                        file_path=str(file_path),
                        file_size_mb=file_size_mb,
                        url=url,
                        title=title,
                        duration_seconds=duration
                    )

        except ImportError:
            logger.error("yt-dlp not installed. Cannot download video.")
            return None
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None

        return None

    def _find_downloaded_file(self, video_id: str, title: str) -> Optional[Path]:
        """Find the downloaded file in directory"""
        try:
            # List files matching pattern
            for file in self.download_path.glob(f"{video_id}_*"):
                if file.is_file():
                    return file
        except Exception as e:
            logger.error(f"Error finding downloaded file: {e}")

        return None

    def get_video_info(self, url: str) -> Optional[dict]:
        """Get video info without downloading"""
        try:
            import yt_dlp

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info

        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None

    def trim_video(self, input_path: str, output_path: str,
                   duration_seconds: int) -> Optional[str]:
        """
        Trim video to specified duration using FFmpeg

        Args:
            input_path: Path to input video
            output_path: Path to output video
            duration_seconds: Duration in seconds

        Returns:
            Path to trimmed video if successful
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-t', str(duration_seconds),
                '-c:v', 'copy',
                '-c:a', 'copy',
                output_path,
                '-y'  # Overwrite output
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                logger.info(f"Video trimmed: {output_path}")
                return output_path
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return None

        except FileNotFoundError:
            logger.error("FFmpeg not installed. Install with: pip install ffmpeg-python")
            return None
        except Exception as e:
            logger.error(f"Error trimming video: {e}")
            return None

    def add_subtitles(self, video_path: str, subtitle_path: str,
                      output_path: str) -> Optional[str]:
        """
        Add subtitles to video using FFmpeg

        Args:
            video_path: Path to input video
            subtitle_path: Path to subtitle file (.srt, .vtt)
            output_path: Path to output video

        Returns:
            Path to video with subtitles
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', subtitle_path,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-c:s', 'mov_text',
                output_path,
                '-y'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                logger.info(f"Subtitles added: {output_path}")
                return output_path
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
            return None

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Remove invalid characters from filename"""
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        safe_name = filename

        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')

        # Limit length
        return safe_name[:100]
