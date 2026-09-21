"""Input validation and sanitization for Copywriter Agent."""

import re
import json
import logging
from typing import Any, Dict, List
from urllib.parse import quote, unquote

logger = logging.getLogger(__name__)


def sanitize_input(text: str, max_length: int = 500) -> str:
    """Sanitize input to prevent prompt injection attacks.

    Args:
        text: Input text to sanitize
        max_length: Maximum length in characters

    Returns:
        Sanitized text safe for Claude API
    """

    if not isinstance(text, str):
        text = str(text)

    # Limit by byte size (UTF-8), max 3 bytes per character
    max_bytes = max_length * 3
    text_bytes = text.encode('utf-8')
    if len(text_bytes) > max_bytes:
        # Decode carefully to preserve UTF-8 integrity
        text = text_bytes[:max_bytes].decode('utf-8', errors='ignore')

    # Escape for JSON
    escaped = json.dumps(text)[1:-1]

    # Dangerous patterns to block (case-insensitive)
    dangerous_patterns = [
        "system:",
        "ignore:",
        "override:",
        "break",
        "``` python",
        "<|endofprompt|>",
        "jailbreak:",
        "hidden instruction:",
        "__import__",
        "eval(",
        "exec(",
    ]

    # ✅ FIXED: Case-insensitive replacement using regex
    for pattern in dangerous_patterns:
        # Use re.IGNORECASE to catch "SYSTEM:", "System:", "system:", etc.
        regex = re.compile(re.escape(pattern), re.IGNORECASE)
        escaped = regex.sub(f"[{pattern}]", escaped)

    return escaped


def validate_title(title: str) -> Dict[str, Any]:
    """Validate a generated title.

    Args:
        title: Title to validate

    Returns:
        Dictionary with validation results
    """

    errors = []

    # Check length
    if not title or len(title.strip()) == 0:
        errors.append("Title is empty")
        return {'valid': False, 'errors': errors}

    # Count words (excluding emojis)
    # Remove emoji to count actual words
    text_no_emoji = re.sub(r'[^\w\s]', '', title)
    words = text_no_emoji.split()
    word_count = len(words)

    # Minimum 8 words
    if word_count < 8:
        errors.append(f"Too few words ({word_count}, minimum 8)")

    # Maximum 15 words
    if word_count > 15:
        errors.append(f"Too many words ({word_count}, maximum 15)")

    # Check for quality
    if len(title) < 20:
        errors.append("Title too short (minimum 20 characters)")

    if len(title) > 100:
        errors.append("Title too long (maximum 100 characters)")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'word_count': word_count,
        'character_count': len(title)
    }


def validate_description(description: str, platform: str) -> Dict[str, Any]:
    """Validate a generated description for specific platform.

    Args:
        description: Description to validate
        platform: Target platform (youtube, rutube, vk, telegram, instagram, okru)

    Returns:
        Dictionary with validation results
    """

    errors = []

    # Platform-specific word count requirements
    platform_limits = {
        'youtube': (150, 300),
        'rutube': (100, 200),
        'vk': (80, 150),
        'telegram': (50, 100),
        'instagram': (50, 100),
        'okru': (80, 150),
    }

    if platform not in platform_limits:
        errors.append(f"Unknown platform: {platform}")
        return {'valid': False, 'errors': errors}

    # Check word count
    words = description.split()
    word_count = len(words)
    min_words, max_words = platform_limits[platform]

    if word_count < min_words:
        errors.append(f"Too few words ({word_count}, minimum {min_words} for {platform})")

    if word_count > max_words:
        errors.append(f"Too many words ({word_count}, maximum {max_words} for {platform})")

    # Check for CTA (Call-To-Action)
    cta_keywords = [
        'subscribe', 'подпишись', 'join', 'присоединяйся',
        'follow', 'click', 'read', 'watch', 'visit', 'share'
    ]
    has_cta = any(keyword in description.lower() for keyword in cta_keywords)

    if not has_cta:
        logger.warning(f"Description for {platform} missing CTA")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'word_count': word_count,
        'has_cta': has_cta,
        'platform': platform
    }


def validate_comment(comment: str) -> Dict[str, Any]:
    """Validate a generated comment.

    Args:
        comment: Comment to validate

    Returns:
        Dictionary with validation results
    """

    errors = []

    # Check length
    words = comment.split()
    word_count = len(words)

    # Comments should be 15-50 words
    if word_count < 15:
        errors.append(f"Comment too short ({word_count} words, minimum 15)")

    if word_count > 50:
        errors.append(f"Comment too long ({word_count} words, maximum 50)")

    # Check for authenticity markers
    authenticity_indicators = [
        'i ',
        'me ',
        'my ',
        'we ',
        'our ',
        '?',  # Question mark
        '!',  # Exclamation
        'love',
        'great',
        'amazing',
        'helpful',
        'thanks',
        'appreciate'
    ]

    has_authenticity = any(
        indicator in comment.lower()
        for indicator in authenticity_indicators
    )

    if not has_authenticity:
        logger.warning("Comment may lack authenticity markers")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'word_count': word_count,
        'has_authenticity': has_authenticity
    }


def parse_json_response(response_text: str, expected_count: int = None) -> Dict[str, Any]:
    """Parse and validate JSON response from Claude.

    Args:
        response_text: Raw response text from Claude
        expected_count: Expected number of items in array (optional)

    Returns:
        Parsed JSON response

    Raises:
        ValueError: If JSON is invalid or structure is wrong
    """

    # Try to extract JSON if it's wrapped in markdown
    if '```json' in response_text:
        match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if match:
            response_text = match.group(1)
    elif '```' in response_text:
        match = re.search(r'```\s*(.*?)\s*```', response_text, re.DOTALL)
        if match:
            response_text = match.group(1)

    # Parse JSON
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")

    # Validate structure
    if not isinstance(result, (dict, list)):
        raise ValueError(f"Expected JSON object or array, got {type(result).__name__}")

    # If it's a dict, check for required fields
    if isinstance(result, dict):
        if 'titles' in result:
            titles = result['titles']
            if not isinstance(titles, list):
                raise ValueError("'titles' field must be an array")
            if expected_count and len(titles) != expected_count:
                raise ValueError(
                    f"Expected {expected_count} titles, got {len(titles)}"
                )
            # Check for null values
            if any(t is None for t in titles):
                raise ValueError("Title array contains null values")

    # If it's a list, validate count
    elif isinstance(result, list):
        if expected_count and len(result) != expected_count:
            raise ValueError(
                f"Expected {expected_count} items, got {len(result)}"
            )
        # Check for null values
        if any(item is None for item in result):
            raise ValueError("Array contains null values")

    return result


def validate_quality_score(score: float) -> bool:
    """Validate that quality score is in valid range.

    Args:
        score: Quality score (0-100)

    Returns:
        True if valid, False otherwise
    """

    if not isinstance(score, (int, float)):
        return False

    return 0 <= score <= 100


def validate_emotion_trigger(emotion: str) -> bool:
    """Validate that emotion trigger is one of allowed values.

    Args:
        emotion: Emotion trigger value

    Returns:
        True if valid, False otherwise
    """

    allowed_emotions = [
        'number',      # "5 Ways to..."
        'question',    # "What if...?"
        'superlative', # "The BEST..."
        'urgency',     # "You NEED to..."
        'aspiration'   # "How to BECOME..."
    ]

    return emotion in allowed_emotions
