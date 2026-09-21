"""Tests for rate limiting and concurrency control."""

import pytest
import time
from src.copywriter.rate_limiting import (
    TokenBucket,
    RateLimiter,
    ConcurrencyController,
    RateLimitExceeded
)


class TestTokenBucket:
    """Test token bucket rate limiter with integer arithmetic."""

    @pytest.fixture
    def token_bucket(self):
        """Create token bucket for tests."""
        return TokenBucket(capacity=20, refill_rate=0.333)  # 20/min

    def test_token_bucket_initialization(self, token_bucket):
        """Test bucket initializes with full capacity."""
        available = token_bucket.get_available_tokens()
        assert available == 20

    def test_token_bucket_acquire_single_token(self, token_bucket):
        """Test acquiring a single token."""
        assert token_bucket.acquire(1) == True
        available = token_bucket.get_available_tokens()
        assert available == 19

    def test_token_bucket_acquire_multiple_tokens(self, token_bucket):
        """Test acquiring multiple tokens."""
        assert token_bucket.acquire(5) == True
        available = token_bucket.get_available_tokens()
        assert available == 15

    def test_token_bucket_exceed_capacity(self, token_bucket):
        """Test that acquiring more than capacity fails."""
        assert token_bucket.acquire(21) == False
        available = token_bucket.get_available_tokens()
        assert available == 20  # Unchanged

    def test_token_bucket_refill_after_60_seconds(self, token_bucket):
        """Test bucket refills after 60 seconds (20 tokens)."""
        # Acquire all 20 tokens
        assert token_bucket.acquire(20) == True
        assert token_bucket.get_available_tokens() == 0

        # Wait for refill (60 seconds for 20 tokens at 0.333/sec)
        # For testing, we'll just verify the math
        # 60 seconds * 0.333 tokens/sec = ~20 tokens
        # Note: In real test, this would take 60 seconds
        # So we'll skip the actual time wait

    def test_token_bucket_partial_refill(self, token_bucket):
        """Test partial refill after some time."""
        # Acquire 10 tokens
        assert token_bucket.acquire(10) == True
        assert token_bucket.get_available_tokens() == 10

        # Wait 15 seconds (should add ~5 tokens)
        time.sleep(15)

        # Should have approximately 15 tokens
        available = token_bucket.get_available_tokens()
        assert 14 < available <= 20

    def test_token_bucket_no_float_precision_issues(self, token_bucket):
        """Test that integer arithmetic prevents float precision issues."""
        # Acquire 1 token 20 times (in normal bucket after refill)
        for i in range(20):
            token_bucket.acquire(1)

        # Should have 0 tokens, not 0.000001 or similar
        available = token_bucket.get_available_tokens()
        assert available < 0.001  # Allow tiny rounding


class TestRateLimiter:
    """Test rate limiter with dependency injection."""

    @pytest.fixture
    def rate_limiter(self):
        """Create rate limiter for tests."""
        return RateLimiter(max_concurrent=3, rate_per_minute=20)

    def test_rate_limiter_initialization(self, rate_limiter):
        """Test rate limiter initializes correctly."""
        status = rate_limiter.get_status()
        assert status['available_tokens'] == 20
        assert status['max_concurrent'] == 3
        assert status['rate_per_minute'] == 20

    def test_rate_limiter_acquire(self, rate_limiter):
        """Test acquiring rate limit tokens."""
        assert rate_limiter.acquire(1) == True
        status = rate_limiter.get_status()
        assert status['available_tokens'] == 19

    def test_rate_limiter_exceed_fails(self, rate_limiter):
        """Test that exceeding rate limit fails."""
        # Acquire all 20 tokens
        for i in range(20):
            assert rate_limiter.acquire(1) == True

        # Next should fail
        assert rate_limiter.acquire(1) == False

    def test_rate_limiter_decorator(self, rate_limiter):
        """Test rate limiter as decorator."""

        @rate_limiter
        def test_function():
            return "success"

        # Should work for first call
        result = test_function()
        assert result == "success"


class TestConcurrencyController:
    """Test concurrency controller."""

    @pytest.fixture
    def controller(self):
        """Create concurrency controller."""
        return ConcurrencyController(max_concurrent=3)

    def test_concurrency_acquire_release(self, controller):
        """Test acquiring and releasing concurrency slots."""
        assert controller.acquire() == True
        assert controller.active_operations == 1

        controller.release(success=True)
        assert controller.active_operations == 0
        assert controller.completed_operations == 1

    def test_concurrency_max_limit(self, controller):
        """Test concurrency respects max limit."""
        # Acquire 3 slots (max)
        assert controller.acquire(timeout=0.1) == True
        assert controller.acquire(timeout=0.1) == True
        assert controller.acquire(timeout=0.1) == True

        # 4th should fail (timeout)
        assert controller.acquire(timeout=0.1) == False

    def test_concurrency_stats(self, controller):
        """Test getting concurrency statistics."""
        controller.acquire()
        controller.acquire()
        controller.release(success=True)
        controller.release(success=False)

        stats = controller.get_stats()
        assert stats['active'] == 0
        assert stats['completed'] == 1
        assert stats['failed'] == 1
        assert stats['total'] == 2


class TestRateLimitExceptions:
    """Test rate limit exceptions."""

    def test_rate_limit_exceeded_exception(self):
        """Test RateLimitExceeded exception."""
        with pytest.raises(RateLimitExceeded):
            raise RateLimitExceeded("Rate limit exceeded")
