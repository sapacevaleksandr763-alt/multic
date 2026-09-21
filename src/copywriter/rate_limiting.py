"""Rate limiting and concurrency control for Copywriter Agent."""

import time
import logging
from threading import Semaphore
from typing import Optional
from functools import wraps

logger = logging.getLogger(__name__)


class TokenBucket:
    """Token bucket rate limiter using integer arithmetic.

    Capacity: 20 tokens
    Refill rate: 20 tokens per minute (0.333 tokens/second)

    Uses integer arithmetic scaled by 1000 to avoid float precision issues.
    """

    def __init__(self, capacity: int = 20, refill_rate: float = 0.333):
        """Initialize token bucket.

        Args:
            capacity: Maximum tokens in bucket (default 20)
            refill_rate: Tokens per second to refill (default 0.333 = 20/min)
        """
        # ✅ FIXED: Use integer arithmetic, scaled by 1000
        self.capacity_millis = capacity * 1000  # 20,000 token-millis
        self.tokens_remaining = capacity * 1000  # Start full
        self.refill_rate_millis = int(refill_rate * 1000)  # 333 millis/sec
        self.last_refill = time.time()

    def acquire(self, tokens: int = 1) -> bool:
        """Try to acquire tokens from bucket.

        Args:
            tokens: Number of tokens to acquire (default 1)

        Returns:
            True if tokens acquired, False if not enough tokens
        """
        self._refill()

        # ✅ FIXED: Use integer comparison, not float
        tokens_needed = tokens * 1000  # Convert to millis

        if self.tokens_remaining >= tokens_needed:
            self.tokens_remaining -= tokens_needed
            return True

        return False

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill

        # ✅ FIXED: Integer math prevents precision loss
        tokens_to_add = int(elapsed * self.refill_rate_millis)
        self.tokens_remaining = min(
            self.capacity_millis,
            self.tokens_remaining + tokens_to_add
        )

        self.last_refill = now

    def get_available_tokens(self) -> float:
        """Get current number of available tokens (for monitoring)."""
        self._refill()
        return self.tokens_remaining / 1000.0

    def get_refill_rate(self) -> float:
        """Get current refill rate in tokens per second."""
        return self.refill_rate_millis / 1000.0


class RateLimiter:
    """Rate limiter with dependency injection for Claude API calls."""

    def __init__(
        self,
        redis_client=None,
        max_concurrent: int = 3,
        rate_per_minute: int = 20
    ):
        """Initialize rate limiter.

        Args:
            redis_client: Redis client for distributed rate limiting (optional)
            max_concurrent: Maximum concurrent API calls (default 3)
            rate_per_minute: Maximum requests per minute (default 20)
        """
        self.redis = redis_client
        self.semaphore = Semaphore(max_concurrent)
        self.token_bucket = TokenBucket(
            capacity=rate_per_minute,
            refill_rate=rate_per_minute / 60.0  # Convert to per-second
        )
        self.max_concurrent = max_concurrent
        self.rate_per_minute = rate_per_minute

    def __call__(self, func):
        """Decorator for rate-limited API calls."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Acquire semaphore (max concurrent)
            with self.semaphore:
                # Check rate limit
                if not self.token_bucket.acquire():
                    raise RateLimitExceeded(
                        f"Rate limit exceeded: max {self.rate_per_minute}/minute"
                    )

                # Call the function
                return func(*args, **kwargs)

        return wrapper

    def acquire(self, tokens: int = 1) -> bool:
        """Try to acquire tokens (manual usage outside decorator).

        Args:
            tokens: Number of tokens to acquire

        Returns:
            True if acquired, False if rate limited
        """
        return self.token_bucket.acquire(tokens)

    def wait_if_needed(self, tokens: int = 1, timeout: float = 60.0):
        """Wait until tokens are available (blocking with timeout).

        Args:
            tokens: Number of tokens needed
            timeout: Maximum time to wait in seconds

        Raises:
            RateLimitExceeded: If timeout exceeded
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.acquire(tokens):
                return
            time.sleep(0.1)  # Check every 100ms

        raise RateLimitExceeded(
            f"Rate limit timeout after {timeout} seconds"
        )

    def get_status(self) -> dict:
        """Get current rate limiter status."""
        return {
            'available_tokens': self.token_bucket.get_available_tokens(),
            'capacity': self.token_bucket.capacity_millis / 1000.0,
            'refill_rate': self.token_bucket.get_refill_rate(),
            'max_concurrent': self.max_concurrent,
            'rate_per_minute': self.rate_per_minute
        }


class ConcurrencyController:
    """Manage concurrent API calls with proper cleanup."""

    def __init__(self, max_concurrent: int = 3):
        """Initialize concurrency controller.

        Args:
            max_concurrent: Maximum concurrent operations
        """
        self.semaphore = Semaphore(max_concurrent)
        self.active_operations = 0
        self.completed_operations = 0
        self.failed_operations = 0

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire a slot for concurrent operation.

        Args:
            timeout: Timeout in seconds (None for blocking)

        Returns:
            True if slot acquired, False if timeout
        """
        result = self.semaphore.acquire(timeout=timeout)
        if result:
            self.active_operations += 1
        return result

    def release(self, success: bool = True):
        """Release a slot and update statistics.

        Args:
            success: Whether the operation succeeded
        """
        self.semaphore.release()
        self.active_operations -= 1

        if success:
            self.completed_operations += 1
        else:
            self.failed_operations += 1

    def get_stats(self) -> dict:
        """Get concurrency statistics."""
        return {
            'active': self.active_operations,
            'completed': self.completed_operations,
            'failed': self.failed_operations,
            'total': self.completed_operations + self.failed_operations
        }


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    pass


class ConcurrencyLimitExceeded(Exception):
    """Exception raised when concurrency limit is exceeded."""
    pass


# Decorator for easy rate limiting
def rate_limited(max_concurrent: int = 3, rate_per_minute: int = 20):
    """Decorator for rate-limited function calls.

    Args:
        max_concurrent: Maximum concurrent calls
        rate_per_minute: Maximum calls per minute

    Returns:
        Decorator function
    """
    limiter = RateLimiter(
        max_concurrent=max_concurrent,
        rate_per_minute=rate_per_minute
    )

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not limiter.acquire():
                raise RateLimitExceeded(
                    f"Rate limit exceeded: {rate_per_minute} calls/minute"
                )

            try:
                return func(*args, **kwargs)
            finally:
                pass

        return wrapper

    return decorator
