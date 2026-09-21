"""Copywriter Agent main service with dependency injection."""

import os
import logging
from threading import Semaphore
from typing import Dict, Any, Optional
from anthropic import Anthropic

from .recovery import RetryManager, RecoveryScheduler
from .rate_limiting import TokenBucket, RateLimiter, RateLimitExceeded
from .validation import sanitize_input, validate_title, parse_json_response
from .alerting import AlertManager, get_alert_manager

logger = logging.getLogger(__name__)


class CopywriterService:
    """Main Copywriter Service with dependency injection.

    Handles title, description, and comment generation with:
    - Concurrency control (max 3 concurrent API calls)
    - Rate limiting (max 20 calls/minute)
    - Automatic retry on failure
    - Alert escalation after 5 retries
    """

    def __init__(
        self,
        redis_client=None,
        db_connection=None,
        max_concurrent: int = 3,
        rate_per_minute: int = 20,
        timeout_seconds: float = 30.0
    ):
        """Initialize Copywriter Service with dependency injection.

        Args:
            redis_client: Redis client for caching and rate limiting
            db_connection: Database connection for retry queue
            max_concurrent: Maximum concurrent API calls (default 3)
            rate_per_minute: Maximum API calls per minute (default 20)
            timeout_seconds: Claude API timeout in seconds (default 30)
        """
        # Dependencies
        self.redis = redis_client
        self.db = db_connection

        # Alert manager
        self.alert_manager = get_alert_manager()

        # Concurrency control (max 3 concurrent)
        self.semaphore = Semaphore(max_concurrent)

        # Rate limiting (max 20/minute)
        self.rate_limiter = TokenBucket(
            capacity=rate_per_minute,
            refill_rate=rate_per_minute / 60.0
        )

        # Claude API client with 30-second timeout
        self.claude_client = Anthropic(
            api_key=os.getenv('CLAUDE_API_KEY'),
            timeout=timeout_seconds
        )

        # Retry management
        self.retry_manager = RetryManager(
            db_connection=db_connection,
            redis_client=redis_client,
            alert_manager=self.alert_manager
        )

        self.max_concurrent = max_concurrent
        self.rate_per_minute = rate_per_minute

    def generate_titles(
        self,
        video_id: str,
        metadata: Dict[str, Any],
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Generate title variants for a video.

        Args:
            video_id: ID of the video
            metadata: Video metadata (title, description, likes, etc.)
            retry_count: Current retry attempt (0-5+)

        Returns:
            Dictionary with generated titles and quality scores
        """

        # Concurrency control: max 3 concurrent
        if not self.semaphore.acquire(blocking=False):
            raise RuntimeError("Max concurrent API calls exceeded")

        try:
            # Rate limiting: max 20/minute
            if not self.rate_limiter.acquire():
                # Add to retry queue for later
                self.retry_manager.add_to_retry_queue(
                    video_id=video_id,
                    component='titles',
                    error_message='Rate limit exceeded',
                    variant_version=1,
                    retry_count=retry_count
                )
                raise RateLimitExceeded("Rate limit: max 20 calls/minute")

            # Sanitize input
            title = sanitize_input(metadata.get('title', ''), max_length=200)
            description = sanitize_input(metadata.get('description', ''), max_length=500)
            top_comments = metadata.get('top_comments', [])[:10]  # Cap at 10

            # Call Claude API
            prompt = f"""Generate 15 highly viral YouTube titles for this video.

Video Title: {title}
Description: {description}
Top Comments: {', '.join(top_comments[:5])}

Rules:
- Each title must be 8-15 words
- Each title must trigger ONE emotion (exactly one):
  * "number": Start with a number (e.g., "5 Ways to...")
  * "question": Start with a question (e.g., "What if...")
  * "superlative": Use superlatives (e.g., "The BEST...")
  * "urgency": Create urgency (e.g., "You NEED to...")
  * "aspiration": Promise achievement (e.g., "How to BECOME...")

Return as JSON: {{"titles": [{{"text": "...", "emotion_trigger": "...", "quality_score": 95}}]}}

Only return valid JSON, no other text."""

            message = self.claude_client.messages.create(
                model="claude-opus-5",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse response
            response_text = message.content[0].text
            result = parse_json_response(response_text)

            # Validate titles
            if 'titles' in result:
                validated_titles = []
                for title_obj in result['titles']:
                    title_text = title_obj.get('text', '')
                    validation = validate_title(title_text)
                    if validation['valid']:
                        validated_titles.append(title_obj)

                result['titles'] = validated_titles
                result['generated_count'] = len(validated_titles)
                result['video_id'] = video_id
                result['component'] = 'titles'

                return result

            return {
                'titles': [],
                'error': 'No titles in response',
                'video_id': video_id
            }

        except RateLimitExceeded as e:
            logger.warning(f"Rate limit for {video_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating titles for {video_id}: {e}")

            # Add to retry queue
            self.retry_manager.add_to_retry_queue(
                video_id=video_id,
                component='titles',
                error_message=str(e),
                variant_version=1,
                retry_count=retry_count
            )
            raise
        finally:
            self.semaphore.release()

    def generate_descriptions(
        self,
        video_id: str,
        title: str,
        alternative_titles: list,
        platforms: list,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Generate descriptions for specific platforms.

        Args:
            video_id: ID of the video
            title: Main title
            alternative_titles: List of alternative titles
            platforms: List of platforms (youtube, rutube, vk, telegram, instagram, okru)
            retry_count: Current retry attempt

        Returns:
            Dictionary with platform-specific descriptions
        """

        if not self.semaphore.acquire(blocking=False):
            raise RuntimeError("Max concurrent API calls exceeded")

        try:
            if not self.rate_limiter.acquire():
                self.retry_manager.add_to_retry_queue(
                    video_id=video_id,
                    component='descriptions',
                    error_message='Rate limit exceeded',
                    variant_version=1,
                    retry_count=retry_count
                )
                raise RateLimitExceeded("Rate limit: max 20 calls/minute")

            # Sanitize inputs
            title = sanitize_input(title, max_length=200)
            platforms_str = ', '.join(platforms)

            prompt = f"""Generate platform-specific descriptions for {platforms_str}.

Title: {title}
Alternative titles: {', '.join(alternative_titles[:3])}

Platform-specific word limits:
- YouTube: 150-300 words
- RuTube: 100-200 words
- VK: 80-150 words
- Telegram: 50-100 words
- Instagram: 50-100 words
- OK.ru: 80-150 words

Each description must include:
- CTA (Call-to-action): Subscribe, Follow, Share, etc.
- Platform-specific hashtags (3-5)
- Appropriate tone for the platform

Return as JSON with platform as keys: {{"youtube": "...", "rutube": "...", ...}}"""

            message = self.claude_client.messages.create(
                model="claude-opus-5",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            result = parse_json_response(response_text)

            result['video_id'] = video_id
            result['component'] = 'descriptions'
            result['platforms'] = platforms

            return result

        except Exception as e:
            logger.error(f"Error generating descriptions for {video_id}: {e}")
            self.retry_manager.add_to_retry_queue(
                video_id=video_id,
                component='descriptions',
                error_message=str(e),
                variant_version=1,
                retry_count=retry_count
            )
            raise
        finally:
            self.semaphore.release()

    def generate_comments(
        self,
        video_id: str,
        title: str,
        description: str,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Generate authentic comments for engagement.

        Args:
            video_id: ID of the video
            title: Video title
            description: Video description
            retry_count: Current retry attempt

        Returns:
            Dictionary with generated comments
        """

        if not self.semaphore.acquire(blocking=False):
            raise RuntimeError("Max concurrent API calls exceeded")

        try:
            if not self.rate_limiter.acquire():
                self.retry_manager.add_to_retry_queue(
                    video_id=video_id,
                    component='comments',
                    error_message='Rate limit exceeded',
                    variant_version=1,
                    retry_count=retry_count
                )
                raise RateLimitExceeded("Rate limit: max 20 calls/minute")

            title = sanitize_input(title, max_length=200)
            description = sanitize_input(description, max_length=300)

            prompt = f"""Generate 10 authentic YouTube comments for this video.

Title: {title}
Description: {description}

Emotion distribution:
- Gratitude (4 comments): Thank you, helpful, appreciate, etc.
- Validation (3 comments): Agree, yes, true, etc.
- Curiosity (2 comments): Questions, follow-up questions
- Achievement (1 comment): Story about their own success

Each comment must be 15-50 words.
Mix of first-person (6-8), questions (1-2), and statements (1-2).

Return as JSON: {{"comments": ["...", "...", ...]}}"""

            message = self.claude_client.messages.create(
                model="claude-opus-5",
                max_tokens=800,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            result = parse_json_response(response_text)

            result['video_id'] = video_id
            result['component'] = 'comments'
            result['count'] = len(result.get('comments', []))

            return result

        except Exception as e:
            logger.error(f"Error generating comments for {video_id}: {e}")
            self.retry_manager.add_to_retry_queue(
                video_id=video_id,
                component='comments',
                error_message=str(e),
                variant_version=1,
                retry_count=retry_count
            )
            raise
        finally:
            self.semaphore.release()

    def get_status(self) -> Dict[str, Any]:
        """Get service status and metrics."""
        return {
            'model': 'claude-opus-5',
            'timeout': '30 seconds',
            'max_concurrent': self.max_concurrent,
            'rate_per_minute': self.rate_per_minute,
            'available_rate_tokens': self.rate_limiter.get_available_tokens(),
            'status': 'operational'
        }


# For easy imports
__all__ = ['CopywriterService', 'get_alert_manager']
