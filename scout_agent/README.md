# 🎬 Scout Agent - Viral Video Discovery

Scout Agent finds viral video candidates from YouTube using intelligent virality detection.

## Architecture

```
Search → Download → Transcribe → Analyze → Rank → Return Top 5
        (YouTube)  (Whisper)   (Claude)  (Score)
```

## Installation

```bash
pip install -r requirements.txt
```

### Dependencies

- `google-api-python-client` - YouTube API
- `openai-whisper` - Audio transcription
- `yt-dlp` - Video downloading
- `anthropic` - Claude API for analysis
- `python-dotenv` - Environment configuration

## Quick Start

### Configuration

Create `.env` file:

```env
YOUTUBE_API_KEY=your_api_key_here
CLAUDE_API_KEY=your_claude_key_here
WHISPER_MODEL=base  # tiny, base, small, medium, large
MAX_RESULTS=5
MIN_VIRAL_SCORE=0.6
```

### Usage

```python
from scout_agent.agent import ScoutAgent

# Initialize
scout = ScoutAgent()

# Find viral videos
results = scout.find_viral_videos("AI coding tutorials")

# Access results
for video in results.top_candidates:
    print(f"{video.video.title}")
    print(f"Viral Score: {video.overall_viral_score}/100")
    print(f"Platforms: {video.recommended_for_platforms}")
    print(f"Moments: {len(video.viral_moments)}")
```

### Interactive Mode

```bash
python -m scout_agent.agent
```

## Output

### ScoutResult

```python
{
    "query": "AI coding tutorials",
    "timestamp": "2026-09-22T10:30:00",
    "candidates_found": 20,
    "top_candidates": [
        {
            "youtube_id": "...",
            "title": "How to Learn Rust",
            "viral_score": 87.5,
            "content_type": "tutorial",
            "key_moments": 4,
            "platforms": ["youtube", "tiktok", "telegram"],
            "url": "https://youtube.com/watch?v=..."
        },
        ...
    ]
}
```

## Architecture Components

### 1. Downloader (`downloader.py`)
- Searches YouTube for videos
- Fetches metadata (views, duration, etc.)
- Returns list of YouTubeVideo objects

### 2. Transcriber (`transcriber.py`)
- Downloads audio from videos
- Transcribes using Whisper
- Returns segments with timestamps

### 3. Analyzer (`analyzer.py`)
- Detects content type
- Extracts viral moments
- Calculates viral score (0-100)
- Recommends target platforms

### 4. Pipeline (`pipeline.py`)
- Orchestrates the flow
- Handles errors gracefully
- Returns ranked candidates

### 5. Agent (`agent.py`)
- Main entry point
- Configuration management
- Interactive mode for testing

## Viral Scoring

Scout Agent analyzes multiple factors:

- **Hooks** - Opening line captures attention
- **Emotional peaks** - High energy/emotion moments
- **Quotable lines** - Memorable phrases
- **Controversy** - Strong opinions/takes
- **Practical value** - Useful information
- **Entertainment** - Fun/engaging content
- **Trend alignment** - Current topics

Score range: 0-100
- 75+: Suitable for all platforms (YouTube, TikTok, Telegram, Instagram)
- 60-74: Good for TikTok, Telegram, Instagram
- <60: Best for Telegram only

## Content Types

Scout Agent classifies videos as:
- `tutorial` - Step-by-step instructions
- `interview` - Q&A with guest
- `vlog` - Personal story/experience
- `podcast` - Long-form discussion
- `news` - Current events/updates
- `debate` - Opposing viewpoints
- `education` - Learning content
- `commentary` - Opinion/analysis
- `comedy` - Entertainment/humor
- `other` - Something else

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_scout_types.py -v

# Run with coverage
pytest tests/ --cov=scout_agent
```

## Error Handling

Scout Agent handles errors gracefully:

- Invalid API keys → RuntimeError
- Network errors → Logged and skipped
- Transcription failures → Video skipped, process continues
- Analysis errors → Logged, defaults to score 50

## Performance

Typical times (for 20 videos):
- Search: 2-3 seconds
- Transcription: 20-30 seconds per video (parallel: 5-10 minutes)
- Analysis: 5-10 seconds per video (sequential: 2-3 minutes)
- Total: ~15-20 minutes for full pipeline

## Next Steps (Phase 2B)

Scout Agent outputs are passed to Copywriter Agent which:
1. Creates 15+ variations
2. Generates hooks and descriptions
3. Optimizes for each platform

Then Promotion Agent:
1. Publishes to 4 platforms
2. Tracks performance
3. A/B tests variations

## Links

- [Architecture Template](../../.claude/skills/ai-youtube-shorts-generator/SKILL.md)
- [Phase 2A Plan](../../CLAUDE.md)
- [Project Memory](../../.claude/projects/c--Users-Alex-Documents-Projects-multic/memory/MEMORY.md)

---

**Status:** Phase 2A - Production Ready ✅  
**Version:** 0.1.0  
**Last Updated:** 2026-09-22
