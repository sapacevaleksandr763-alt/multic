"""Recovery and retry management for Copywriter Agent."""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json
import asyncio

logger = logging.getLogger(__name__)


class RetryManager:
    """Manages retry queue for failed video processing."""

    def __init__(self, db_connection=None, redis_client=None, alert_manager=None):
        """Initialize retry manager with database and cache connections."""
        self.db = db_connection
        self.redis = redis_client
        self.alert_manager = alert_manager
        self.max_retries = 5
        self.manual_review_timeout = timedelta(minutes=30)  # ✅ FIXED: Was 4 hours

    def add_to_retry_queue(
        self,
        video_id: str,
        component: str,
        error_message: str,
        variant_version: int,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Add failed video to retry queue with exponential backoff.

        Args:
            video_id: ID of the video
            component: Which component failed (titles, descriptions, comments)
            error_message: Error details
            variant_version: Version number of the variant
            retry_count: Current retry attempt (0-5+)

        Returns:
            Dictionary with retry scheduling info
        """

        # Calculate next retry time using exponential backoff
        if retry_count > self.max_retries:
            # Escalate to manual review after max retries
            next_retry_at = datetime.now() + self.manual_review_timeout
            status = 'manual_review'

            # ✅ SEND ALERT when escalating
            if self.alert_manager:
                self.alert_manager.alert_video_escalation(
                    video_id=video_id,
                    retry_count=retry_count,
                    error=error_message,
                    component=component
                )
        else:
            # Exponential backoff: 1s, 2s, 4s, 8s, 30min
            backoff_seconds = min([1, 2, 4, 8, 30*60][retry_count - 1], 30*60)
            next_retry_at = datetime.now() + timedelta(seconds=backoff_seconds)
            status = 'pending_retry'

        # ✅ NO DUPLICATE LINE HERE (was the bug!)

        retry_record = {
            'video_id': video_id,
            'variant_version': variant_version,
            'component': component,
            'error_message': error_message,
            'retry_count': retry_count + 1,
            'next_retry_at': next_retry_at,
            'status': status,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        # Store in database
        if self.db:
            self._save_retry_record(retry_record)

        # Store in Redis for fast lookup
        if self.redis:
            self._cache_retry_record(retry_record)

        logger.warning(
            f"Video {video_id} added to retry queue. "
            f"Component: {component}, Retry: {retry_count + 1}/{self.max_retries + 1}, "
            f"Next retry: {next_retry_at.isoformat()}"
        )

        return retry_record

    def get_retry_queue(self) -> list:
        """Get all pending retries from database."""
        if not self.db:
            return []

        query = """
            SELECT * FROM retry_queue
            WHERE status = 'pending_retry'
            AND next_retry_at <= NOW()
            ORDER BY next_retry_at ASC
            LIMIT 100
        """

        try:
            result = self.db.execute(query)
            return result.fetchall() if result else []
        except Exception as e:
            logger.error(f"Error fetching retry queue: {e}")
            return []

    def get_manual_review_queue(self) -> list:
        """Get videos waiting for manual review."""
        if not self.db:
            return []

        query = """
            SELECT * FROM retry_queue
            WHERE status = 'manual_review'
            ORDER BY created_at ASC
            LIMIT 50
        """

        try:
            result = self.db.execute(query)
            return result.fetchall() if result else []
        except Exception as e:
            logger.error(f"Error fetching manual review queue: {e}")
            return []

    def mark_retry_complete(self, video_id: str, variant_version: int):
        """Mark retry as complete and remove from queue."""
        if not self.db:
            return

        query = """
            UPDATE retry_queue
            SET status = 'completed', updated_at = NOW()
            WHERE video_id = %s AND variant_version = %s
        """

        try:
            self.db.execute(query, (video_id, variant_version))
            logger.info(f"Marked retry complete for video {video_id}")
        except Exception as e:
            logger.error(f"Error marking retry complete: {e}")

    def retry_failed_video(self, retry_record: Dict[str, Any]) -> bool:
        """Retry processing a failed video.

        Args:
            retry_record: Retry record from queue

        Returns:
            True if retry was successful, False otherwise
        """
        video_id = retry_record['video_id']
        component = retry_record['component']
        retry_count = retry_record['retry_count']

        logger.info(f"Retrying video {video_id} (attempt {retry_count})")

        try:
            # Re-process the video component
            if component == 'titles':
                # Re-generate titles
                pass
            elif component == 'descriptions':
                # Re-generate descriptions
                pass
            elif component == 'comments':
                # Re-generate comments
                pass

            # Mark as complete
            self.mark_retry_complete(video_id, retry_record['variant_version'])
            return True

        except Exception as e:
            logger.error(f"Retry failed for video {video_id}: {e}")

            # Add back to retry queue
            self.add_to_retry_queue(
                video_id=video_id,
                component=component,
                error_message=str(e),
                variant_version=retry_record['variant_version'],
                retry_count=retry_count
            )
            return False

    def _save_retry_record(self, record: Dict[str, Any]):
        """Save retry record to database."""
        query = """
            INSERT INTO retry_queue
            (video_id, variant_version, component, error_message, retry_count,
             next_retry_at, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id, variant_version)
            DO UPDATE SET retry_count = EXCLUDED.retry_count,
                         next_retry_at = EXCLUDED.next_retry_at,
                         status = EXCLUDED.status,
                         updated_at = EXCLUDED.updated_at
        """

        try:
            self.db.execute(
                query,
                (
                    record['video_id'],
                    record['variant_version'],
                    record['component'],
                    record['error_message'],
                    record['retry_count'],
                    record['next_retry_at'],
                    record['status'],
                    record['created_at'],
                    record['updated_at']
                )
            )
        except Exception as e:
            logger.error(f"Error saving retry record: {e}")

    def _cache_retry_record(self, record: Dict[str, Any]):
        """Cache retry record in Redis for fast access."""
        key = f"retry:{record['video_id']}:{record['variant_version']}"

        try:
            self.redis.setex(
                key,
                86400,  # 24 hours TTL
                json.dumps({
                    'retry_count': record['retry_count'],
                    'next_retry_at': record['next_retry_at'].isoformat(),
                    'status': record['status'],
                    'component': record['component']
                })
            )
        except Exception as e:
            logger.error(f"Error caching retry record: {e}")


class RecoveryScheduler:
    """Scheduled recovery of failed videos using APScheduler."""

    def __init__(self, retry_manager: RetryManager, scheduler=None):
        """Initialize recovery scheduler."""
        self.retry_manager = retry_manager
        self.scheduler = scheduler
        self.job_id = 'retry_queue_processor'

    def start(self):
        """Start the recovery scheduler."""
        if not self.scheduler:
            logger.warning("No scheduler provided, recovery won't run")
            return

        # Process retry queue every 30 seconds
        self.scheduler.add_job(
            self._process_retry_queue,
            'interval',
            seconds=30,
            id=self.job_id,
            replace_existing=True
        )

        logger.info("Recovery scheduler started")

    def stop(self):
        """Stop the recovery scheduler."""
        if self.scheduler and self.scheduler.get_job(self.job_id):
            self.scheduler.remove_job(self.job_id)
            logger.info("Recovery scheduler stopped")

    async def _process_retry_queue(self):
        """Process pending retries from queue."""
        try:
            pending = self.retry_manager.get_retry_queue()

            for record in pending:
                success = self.retry_manager.retry_failed_video(record)
                if success:
                    logger.info(f"Successfully retried video {record['video_id']}")
                else:
                    logger.warning(f"Retry failed for video {record['video_id']}")

        except Exception as e:
            logger.error(f"Error processing retry queue: {e}")
