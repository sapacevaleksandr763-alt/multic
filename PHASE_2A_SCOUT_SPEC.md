# Phase 2A: Scout Agent Specification

**Status:** ✅ Implementation Complete  
**Date:** 2026-09-22  
**Version:** 0.1.0  

---

## Overview

Scout Agent finds viral video candidates from YouTube using AI-powered virality detection. It's the first stage of MULTIC's content pipeline.

**Pipeline:** Search → Download → Transcribe → Analyze → Rank → Output

---

## Architecture

### High-Level Flow

```
User Query
    ↓
Search YouTube (Downloader)
    ↓
Transcribe Audio (Whisper)
    ↓
Analyze Virality (Claude)
    ↓
Rank by Score
    ↓
Return Top 5 Candidates
    ↓
→ Pass to Copywriter Agent (Phase 2B)
```

### Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Downloader** | Search YouTube, fetch metadata | Google YouTube API v3 |
| **Transcriber** | Extract text from audio | OpenAI Whisper |
| **Analyzer** | Detect viral moments, score | Claude API (Opus 5) |
| **Pipeline** | Orchestrate flow | Python pipeline pattern |
| **Agent** | User-facing interface | Config + CLI |

---

## File Structure

```
scout_agent/
├── __init__.py              # Package init
├── agent.py                 # Main ScoutAgent class
├── config.py                # Configuration management
├── pipeline.py              # Pipeline orchestration
├── downloader.py            # YouTube video search
├── transcriber.py           # Audio transcription
├── analyzer.py              # Virality analysis
├── types.py                 # Data structures
├── logging_config.py        # Logging setup
├── README.md                # Usage guide
└── pytest.ini               # Test config

tests/
├── __init__.py
├── conftest.py              # (existing) pytest fixtures
├── test_scout_types.py      # Type tests
├── test_scout_config.py     # Config tests
└── test_scout_integration.py # Integration tests
```

---

## Data Types

### Input
- **Query** (str): Search term (e.g., "AI coding tutorials")

### Output
- **ScoutResult**:
  - `query` (str): Original search query
  - `videos` (List[YouTubeVideo]): All found videos
  - `analyzed_videos` (List[AnalyzedVideo]): Analyzed results
  - `top_candidates` (List[AnalyzedVideo]): Top N sorted by viral_score
  - `timestamp` (datetime): When search was performed

### Intermediate Types

**YouTubeVideo**
- `youtube_id`, `title`, `channel`, `view_count`
- `published_at`, `duration_seconds`
- `description`, `url`, `thumbnail_url`

**Transcript**
- `youtube_id`, `text` (full transcript)
- `segments`: [{start, end, text}, ...]
- `language`

**ViralMoment**
- `start_time`, `end_time`: Timestamp in video
- `text_snippet`: Exact quote
- `viral_factors`: ["opinion_bomb", "emotional_peak", ...]
- `confidence`: 0-1 score

**AnalyzedVideo**
- `video`: YouTubeVideo
- `transcript`: Transcript
- `viral_moments`: List[ViralMoment]
- `overall_viral_score`: 0-100
- `content_type`: "tutorial", "podcast", etc.
- `key_takeaway`: One-sentence summary
- `recommended_for_platforms`: ["youtube", "tiktok", ...]

---

## Virality Scoring

### Factors Analyzed

**Content Quality:**
- Hooks (opening line)
- Emotional peaks
- Quotable lines
- Story structure

**Engagement Potential:**
- Controversy/opinion
- Practical value
- Entertainment
- Trend alignment

**Platform Fit:**
- Duration (should be <10min for clips)
- Visual quality
- Pacing
- Topic relevance

### Score Range

- **75-100:** Ready for all platforms (YouTube, TikTok, Telegram, Instagram)
- **60-74:** Good for social clips (TikTok, Telegram, Instagram)
- **<60:** Best for Telegram/newsletter

### Examples

**High Score (85+):**
- "Why Rust is better than C++" (strong opinion + tutorial)
- Emotional breakdown moment + wisdom
- Trending topic + expert commentary

**Medium Score (60-74):**
- Educational content with decent pacing
- Interesting story but slow sections
- Niche topic with good explanation

**Low Score (<60):**
- Rambling discussion
- Technical details without hooks
- Long introduction before main point

---

## Configuration

### Environment Variables

```env
YOUTUBE_API_KEY=sk-...              # Required
CLAUDE_API_KEY=sk-...               # Required
WHISPER_MODEL=base                  # tiny, base, small, medium, large
LANGUAGE=en                         # Language code
MAX_RESULTS=5                       # Top N candidates to return
MIN_VIRAL_SCORE=0.6                 # Filter threshold (0-1)
LOG_LEVEL=INFO                      # INFO, DEBUG, WARNING, ERROR
```

### Programmatic Configuration

```python
from scout_agent.config import ScoutConfig
from scout_agent.agent import ScoutAgent

config = ScoutConfig(
    youtube_api_key="your_key",
    max_results=5,
    whisper_model="base",
    min_viral_score=0.6
)

scout = ScoutAgent(config=config)
```

---

## Usage

### Quick Start

```python
from scout_agent.agent import ScoutAgent

scout = ScoutAgent()
results = scout.find_viral_videos("AI safety")

for video in results.top_candidates:
    print(f"{video.video.title}: {video.overall_viral_score}")
```

### Interactive Mode

```bash
python -m scout_agent.agent
# Input prompts appear, enter search queries
```

### Batch Processing

```python
scout = ScoutAgent()

queries = [
    "AI coding tutorials",
    "Machine learning basics",
    "Rust programming"
]

for query in queries:
    results = scout.find_viral_videos(query)
    print(f"Found {len(results.top_candidates)} candidates for '{query}'")
    # Process results...
```

---

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Unit Tests
```bash
pytest tests/test_scout_types.py -v
pytest tests/test_scout_config.py -v
```

### Integration Tests
```bash
pytest tests/test_scout_integration.py -v
```

### With Coverage
```bash
pytest tests/ --cov=scout_agent --cov-report=html
```

### Test Suite

- **test_scout_types.py**: Data structure tests (6 tests)
- **test_scout_config.py**: Configuration tests (4 tests)
- **test_scout_integration.py**: End-to-end tests (3 tests)
- **Total: 13 integration + unit tests**

---

## Dependencies

**Core:**
- `google-api-python-client` - YouTube API
- `openai-whisper` - Audio transcription
- `yt-dlp` - Video downloading
- `anthropic` - Claude API

**Optional:**
- `faster-whisper` - Faster Whisper implementation
- `torch` - ML framework for Whisper

**Testing:**
- `pytest`, `pytest-cov`, `pytest-mock`

**See:** `requirements.txt`

---

## Error Handling

Scout Agent handles failures gracefully:

| Error | Handling |
|-------|----------|
| Invalid API key | RuntimeError on init |
| Network error | Log + retry once |
| Transcription fails | Log + skip video |
| Analysis fails | Use default score (50) |
| No results | Return empty ScoutResult |

All failures are logged, process continues.

---

## Performance Characteristics

### Typical Runtime (for 20 videos)

| Step | Time | Notes |
|------|------|-------|
| Search | 2-3s | API call + enrichment |
| Transcribe | 20-30s/video | Sequential: 5-10 min total |
| Analyze | 5-10s/video | Sequential: 2-3 min total |
| Rank | <1s | Sort operation |
| **Total** | **~15-20 min** | Can parallelize transcribe |

### Optimization Opportunities

1. **Parallel transcription** - Process videos concurrently (reduce 10min → 3min)
2. **Caching** - Cache transcripts, analysis results
3. **Batching** - Analyze multiple videos in single Claude call
4. **Local Whisper** - Use faster-whisper instead of cloud

---

## Integration with Phase 2B

Scout Agent outputs are consumed by **Copywriter Agent**:

```
ScoutResult.top_candidates[]
    ↓ (AnalyzedVideo objects)
    ↓
Copywriter Agent:
  1. Generate 15+ variations
  2. Create hooks
  3. Optimize descriptions
  4. A/B test candidates
    ↓ (CopywriterResult)
    ↓
Promotion Agent (Phase 2C)
```

**Interface:** AnalyzedVideo data structure is shared

---

## Monitoring & Observability

### Logging

Scout Agent logs at multiple levels:
- `DEBUG`: Detailed flow (model selection, etc.)
- `INFO`: Major steps (search, transcribe, analyze)
- `WARNING`: Recoverable errors (transcription failed, skipping)
- `ERROR`: Fatal errors in component (API unavailable)

### Metrics to Track

1. **Search metrics:**
   - Queries per day
   - Videos found per query
   - Average view counts

2. **Virality metrics:**
   - Score distribution
   - Top content types
   - Platform recommendations

3. **Performance metrics:**
   - Pipeline runtime
   - Error rates
   - Cache hit rates

---

## Future Enhancements (Phase 6+)

- [ ] Parallel transcription (3x speedup)
- [ ] Result caching (Redis)
- [ ] Transcript search/filtering
- [ ] Custom virality models
- [ ] Competitor tracking
- [ ] Historical trend analysis
- [ ] API rate-limit optimization

---

## Comparison: Scout vs Competitors

| Feature | Scout Agent | AI-Youtube-Shorts | MoneyPrinterTurbo |
|---------|-------------|-------------------|-------------------|
| **Find videos** | ✅ Search + rank | ❌ Requires URL | ❌ Requires URL |
| **Transcribe** | ✅ Whisper | ✅ Whisper | ✅ Whisper |
| **Virality detect** | ✅ Specialized | ⚠️ Generic | ❌ None |
| **Platform optimize** | ✅ Yes | ❌ Generic | ⚠️ Speed-focused |
| **A/B testing** | ✅ Phase 2C | ❌ None | ❌ None |
| **Pass to next stage** | ✅ Phase 2B | ❌ Outputs clips | ❌ Outputs video |

**Key difference:** Scout finds AND analyzes videos, not just processes given URLs.

---

## FAQ

**Q: Why Whisper instead of API transcription?**  
A: Faster, cheaper, works offline. We control data.

**Q: Why Claude instead of custom model?**  
A: Handles nuanced virality detection. Extensible for different niches.

**Q: How do I parallelize transcription?**  
A: Use `asyncio` or `multiprocessing` on `batch_transcribe()`.

**Q: Can I use local models?**  
A: Yes, see `analyzer.py` - can swap Claude for local LLM.

**Q: What's the cost?**  
A: ~$0.10/video (YouTube API free, Whisper $0.02/min, Claude $0.03/request)

---

## References

- [Architecture Template](/.claude/skills/ai-youtube-shorts-generator/SKILL.md)
- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [Whisper Docs](https://github.com/openai/whisper)
- [Claude API Docs](https://docs.anthropic.com)
- [Phase 2A Plan](./CLAUDE.md)

---

**Status:** ✅ Phase 2A Complete  
**Next:** Phase 2B - Copywriter Agent  
**Timeline:** 1-2 weeks until full pipeline (Phase 2A + 2B + 2C + 2D)
