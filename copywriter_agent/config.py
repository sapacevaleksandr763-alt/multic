"""Configuration for Copywriter Agent"""

from dataclasses import dataclass
import os


@dataclass
class CopywriterConfig:
    """Configuration for Copywriter Agent with validation"""
    claude_api_key: str
    model: str = "claude-opus-5"
    temperature: float = 0.8
    max_variations: int = 15
    min_quality_score: float = 0.7

    def validate(self) -> None:
        """Validate configuration values"""
        if not self.claude_api_key or not self.claude_api_key.strip():
            raise ValueError("CLAUDE_API_KEY required")

        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("temperature must be 0-1")

        if self.max_variations != 15:
            raise ValueError("max_variations must be exactly 15")

        if self.min_quality_score < 0 or self.min_quality_score > 1:
            raise ValueError("min_quality_score must be 0-1")

    @classmethod
    def from_env(cls) -> "CopywriterConfig":
        """Load configuration from environment variables"""
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise ValueError("CLAUDE_API_KEY environment variable not set")

        config = cls(
            claude_api_key=api_key,
            model=os.getenv("COPYWRITER_MODEL", "claude-opus-5"),
            temperature=float(os.getenv("COPYWRITER_TEMPERATURE", "0.8")),
            max_variations=int(os.getenv("COPYWRITER_MAX_VARIATIONS", "15")),
            min_quality_score=float(os.getenv("COPYWRITER_MIN_QUALITY", "0.7")),
        )

        config.validate()
        return config
