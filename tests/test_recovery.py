"""Tests for retry recovery system."""

import pytest
from datetime import datetime, timedelta
from src.copywriter.recovery import RetryManager


class TestRetryManager:
    """Test retry queue management."""

    @pytest.fixture
    def retry_manager(self):
        """Create retry manager for tests."""
        return RetryManager()

    def test_retry_timeout_30min(self, retry_manager):
        """Test that manual review timeout is 30 minutes (FIXED from 4 hours)."""
        result = retry_manager.add_to_retry_queue(
            video_id='test-123',
            component='titles',
            error_message='Test error',
            variant_version=1,
            retry_count=6  # Exceeds max of 5
        )

        # Should be manual review status
        assert result['status'] == 'manual_review'

        # Calculate time difference
        time_diff = result['next_retry_at'] - datetime.now()

        # Should be approximately 30 minutes (1800 seconds)
        # Allow 10 second buffer for test execution
        assert 1790 < time_diff.total_seconds() < 1810

    def test_exponential_backoff_first_retry(self, retry_manager):
        """Test exponential backoff for first retry (1 second)."""
        result = retry_manager.add_to_retry_queue(
            video_id='test-124',
            component='titles',
            error_message='Test error',
            variant_version=1,
            retry_count=1
        )

        # Should be pending retry status
        assert result['status'] == 'pending_retry'

        # Should retry after 1 second
        time_diff = result['next_retry_at'] - datetime.now()
        assert 0.9 < time_diff.total_seconds() < 1.2

    def test_exponential_backoff_second_retry(self, retry_manager):
        """Test exponential backoff for second retry (2 seconds)."""
        result = retry_manager.add_to_retry_queue(
            video_id='test-125',
            component='descriptions',
            error_message='Test error',
            variant_version=1,
            retry_count=2
        )

        # Should retry after 2 seconds
        time_diff = result['next_retry_at'] - datetime.now()
        assert 1.9 < time_diff.total_seconds() < 2.2

    def test_exponential_backoff_fifth_retry(self, retry_manager):
        """Test exponential backoff for fifth retry (30 minutes)."""
        result = retry_manager.add_to_retry_queue(
            video_id='test-126',
            component='comments',
            error_message='Test error',
            variant_version=1,
            retry_count=5
        )

        # Should retry after 30 minutes (capped at 30*60 = 1800 seconds)
        time_diff = result['next_retry_at'] - datetime.now()
        assert 1790 < time_diff.total_seconds() < 1810

    def test_no_duplicate_overwrite(self, retry_manager):
        """Test that retry timeout is not overwritten (was the bug)."""
        # Create retry with retry_count > 5 (should set 30 min timeout)
        result = retry_manager.add_to_retry_queue(
            video_id='test-127',
            component='titles',
            error_message='Test error',
            variant_version=1,
            retry_count=6
        )

        # Verify next_retry_at is correct (30 minutes, not undefined)
        assert result['next_retry_at'] is not None

        # Verify it's in the future
        assert result['next_retry_at'] > datetime.now()

        # Verify it's not some random value (would be if backoff_seconds was undefined)
        time_diff = result['next_retry_at'] - datetime.now()
        assert time_diff.total_seconds() > 1500  # At least 25 minutes
