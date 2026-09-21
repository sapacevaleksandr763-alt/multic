# Copywriter Agent Initialization Design

**Date:** 2026-09-21  
**Status:** Design Approved  
**Task:** Task 1 - Initialize Copywriter Agent with CLAUDE_API_KEY  

---

## 📋 Overview

**Goal:** Initialize Copywriter Agent to accept video data from Scout Agent and generate 15 titles + 30 descriptions + 10 comments per video using Claude API.

**Scope:** 
- Create 4 core classes (HookAnalyzer, TitleGenerator, DescriptionGenerator, CommentGenerator)
- Validate CLAUDE_API_KEY works
- Single Claude API call per component (optimize cost)
- Save results to content_variants database table
- Full error handling and logging

**Success Criteria:**
- ✅ CLAUDE_API_KEY successfully validates
- ✅ All 4 classes instantiate without errors
- ✅ End-to-end flow: video_metadata → hook_analysis → titles → descriptions → comments
- ✅ Results persist in database
- ✅ Unit tests pass (70%+ coverage)

---

## 🏗️ Architecture

### Component 1: HookAnalyzer
**Purpose:** Analyze YouTube video metadata to extract viral hooks and audience sentiment

**Input:**
```python
{
    "video_id": "dQw4w9WgXcQ",
    "title": "Viral Marketing Strategy 2026",
    "description": "Learn how to...",
    "likes": 50000,
    "comments": 2000,
    "views": 1000000,
    "top_comments": ["Great insight!", "Saved me money!", ...]
}
```

**Output:**
```python
{
    "main_hook": "Unexpected marketing psychology insight",
    "audience_sentiment": "Viewers value expert education and practical tips",
    "trending_angle": "AI-powered personalization",
    "viral_potential": 8.5  # out of 10
}
```

**Implementation:**
- Parse title, description, comments
- Identify 2-3 key hooks
- Sentiment from top comments (keyword analysis)
- No external API call (local analysis)

---

### Component 2: TitleGenerator
**Purpose:** Generate 15 viral-optimized titles for YouTube Shorts/TikTok

**Input:**
```python
{
    "video_id": "dQw4w9WgXcQ",
    "hook_analysis": {...}
}
```

**Output:**
```python
[
    "This ONE Marketing Hack Changed Everything",
    "The $100K Strategy Nobody Talks About",
    "Psychology Experts HATE This Trick",
    ...  # 15 total
]
```

**Implementation:**
- Single Claude API call with structured prompt
- Prompt template includes: hook, audience, platform (YouTube Shorts)
- Cost: 1 API call per video
- Response parsing: JSON array of 15 strings

**Prompt Structure:**
```
You are a viral video title expert.
Given this hook analysis: {hook_analysis}
Generate exactly 15 attention-grabbing titles for YouTube Shorts.
Requirements:
- 8-15 words each
- Include emotional triggers or pattern interrupts
- Optimized for algorithm (use hooks, questions, numbers)
- Unique and not repetitive
Return as JSON array of strings only.
```

---

### Component 3: DescriptionGenerator
**Purpose:** Generate 30 platform-specific descriptions (5 per platform)

**Platforms:**
1. YouTube (longer, SEO-optimized)
2. RuTube (Russian platform specifics)
3. VK (social graph optimized)
4. Telegram (action-oriented)
5. Instagram (hashtag optimized)

**Input:**
```python
{
    "video_id": "dQw4w9WgXcQ",
    "hook_analysis": {...},
    "title": "This ONE Marketing Hack Changed Everything"
}
```

**Output:**
```python
{
    "youtube": [
        "Full description with SEO keywords and links...",
        "Alternative description focusing on retention...",
        ...  # 5 total
    ],
    "rutube": [...],
    "vk": [...],
    "telegram": [...],
    "instagram": [...]
}
```

**Implementation:**
- Single Claude API call with platform-aware prompting
- Prompt specifies platform constraints (length, format, hashtags)
- Cost: 1 API call (not 5)
- Response parsing: JSON object with platform keys

**Prompt Structure:**
```
You are a platform-specific copywriter.
Generate 5 descriptions each for YouTube, RuTube, VK, Telegram, and Instagram.
Video hook: {hook_analysis}
Title: {title}

Requirements per platform:
- YouTube: 150-300 words, SEO keywords, CTA
- RuTube: 100-200 words, Russian cultural context
- VK: 80-150 words, conversation starter, hashtags
- Telegram: 50-100 words, action-oriented, urgency
- Instagram: 50-100 words, hashtags (#), emojis, call-to-action

Return as JSON object: {"youtube": [...], "rutube": [...], ...}
```

---

### Component 4: CommentGenerator
**Purpose:** Generate 10 social proof comments (authentic engagement)

**Input:**
```python
{
    "video_id": "dQw4w9WgXcQ",
    "title": "This ONE Marketing Hack Changed Everything",
    "descriptions": {...}
}
```

**Output:**
```python
[
    "This literally saved my business. Thank you!",
    "I've watched 20 videos on this and this is the only one that explains it clearly",
    "Can't believe this is free information",
    ...  # 10 total
]
```

**Implementation:**
- Single Claude API call
- Generate authentic-sounding engagement comments
- Mix of: gratitude, validation, curiosity, practical results
- Cost: 1 API call per video

**Prompt Structure:**
```
Generate 10 authentic social proof comments for this video.
Title: {title}
Key hook: {hook_analysis["main_hook"]}

Requirements:
- Sound natural and authentic (not marketing-y)
- 15-50 words each
- Mix emotion types: gratitude (4), validation (3), curiosity (2), results (1)
- No hashtags, no @ mentions, no links
- First-person perspective (use "I")

Return as JSON array of strings.
```

---

## 🔄 Data Flow

```
Scout Agent Output (video metadata)
    ↓
HookAnalyzer.analyze(metadata)
    ↓ [hook_analysis: {main_hook, audience_sentiment, trending_angle, viral_potential}]
    ↓
TitleGenerator.generate(video_id, hook_analysis)
    ↓ [titles: [15 strings]]
    ↓
DescriptionGenerator.generate(video_id, hook_analysis, title)
    ↓ [descriptions: {youtube: [5], rutube: [5], vk: [5], telegram: [5], instagram: [5]}]
    ↓
CommentGenerator.generate(video_id, title, descriptions)
    ↓ [comments: [10 strings]]
    ↓
Database.save(content_variants)
    ↓
Return to Promotion Agent: {video_id, titles, descriptions, comments, analysis}
```

---

## 🛡️ Error Handling

**Critical Errors (stop processing):**
```python
- AuthenticationError: "CLAUDE_API_KEY invalid or expired"
  → Log, return error, DO NOT retry
  
- RateLimitError: "Claude API rate limit exceeded"
  → Log, implement exponential backoff, retry after 60s
  
- ValueError: "Invalid metadata format"
  → Log, return error, skip this video
```

**Warnings (log but continue):**
```python
- JSON parsing error in response
  → Fallback to raw text parsing
  
- Missing optional fields (comments, description)
  → Use defaults and continue
```

**Logging:**
- Log level: INFO for normal flow, ERROR for failures
- Format: `[COPYWRITER] {timestamp} {level} {message}`
- Log to: `logs/copywriter_agent.log`

---

## 🧪 Testing Strategy

**Unit Tests:**
```python
test_hook_analyzer_valid_metadata()
  → Input: valid YouTube metadata dict
  → Verify: returns dict with 4 required keys
  
test_hook_analyzer_missing_fields()
  → Input: partial metadata
  → Verify: handles gracefully or raises ValueError
  
test_title_generator_returns_exactly_15()
  → Input: hook_analysis
  → Verify: returns list of exactly 15 strings
  
test_title_generator_api_key_invalid()
  → Mock: invalid API key
  → Verify: raises AuthenticationError
  
test_description_generator_all_platforms()
  → Input: hook_analysis, title
  → Verify: output has all 5 platform keys
  → Verify: each platform has 5 descriptions
  
test_comment_generator_count_and_format()
  → Input: title, descriptions
  → Verify: returns list of exactly 10 strings
  → Verify: each comment is 15-50 words
  
test_db_persistence()
  → Execute full pipeline
  → Verify: results saved to content_variants table
```

**Integration Tests:**
```python
test_full_pipeline_scout_to_copywriter()
  → Input: real video from Scout Agent
  → Execute: hook → titles → descriptions → comments
  → Verify: end-to-end output structure
  → Verify: all 4 components work together
  
test_claude_api_key_validation()
  → Verify: CLAUDE_API_KEY loaded from .env
  → Verify: Anthropic client instantiates
  → Verify: test API call succeeds
```

**Coverage Target:** 70%+ (unit tests)

---

## 📦 Dependencies & API Costs

**Python Dependencies:**
```
anthropic>=0.7.0  (Claude API client)
python-dotenv>=1.0  (load .env)
sqlalchemy>=2.0  (database ORM)
```

**API Costs (per 100 videos):**
- Hook Analysis: $0 (local, no API)
- Titles (100 calls): ~$5-10
- Descriptions (100 calls): ~$10-20
- Comments (100 calls): ~$5-10
- **Total per 100 videos: ~$20-40**

**Cost Optimization:**
- ✅ Single API call per component (not per variant)
- ✅ Batch processing (future optimization)
- ✅ Caching hook analysis results

---

## 🎯 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| API Key Validation | ✅ Pass | Test call to Claude API |
| Titles Generated | 15 per video | Count array length |
| Descriptions Quality | 5 per platform | Platform-specific grammar check |
| Comments Authenticity | Natural sounding | Manual review sample |
| Database Persistence | 100% save rate | Query content_variants count |
| Error Handling | < 1% failure | Log analysis |
| Test Coverage | 70%+ | pytest coverage report |
| Execution Time | < 30s per video | Benchmark full pipeline |

---

## 📅 Implementation Timeline

**Phase 1 (Today - Day 1):**
- ✅ Create HookAnalyzer class (no API calls)
- ✅ Validate CLAUDE_API_KEY
- ✅ Create unit tests for HookAnalyzer

**Phase 2 (Day 2):**
- ✅ Create TitleGenerator class (Claude API)
- ✅ Create unit tests for TitleGenerator
- ✅ Integration test: Scout → HookAnalyzer → TitleGenerator

**Phase 3 (Day 3-4):**
- ✅ Create DescriptionGenerator & CommentGenerator
- ✅ Full end-to-end testing
- ✅ Database persistence

**Phase 4 (Day 5):**
- ✅ Code review
- ✅ Performance optimization
- ✅ Ready for Promotion Agent integration

---

## 📝 Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `copywriter_agent.py` | Modify | Add 4 classes + integrate CLAUDE_API_KEY |
| `tests/unit/test_copywriter_agent.py` | Create | Unit tests for all 4 components |
| `tests/integration/test_copywriter_pipeline.py` | Create | End-to-end pipeline test |
| `.env` | ✅ Done | CLAUDE_API_KEY already added |
| `logs/copywriter_agent.log` | Create | Logging output |
| `docs/superpowers/specs/2026-09-21-copywriter-initialization-design.md` | Create | This design doc |

---

## ✅ Acceptance Criteria

Before moving to implementation:
- [ ] All 4 components defined clearly
- [ ] API cost estimates acceptable
- [ ] Error handling strategy solid
- [ ] Testing strategy comprehensive
- [ ] No blockers identified
- [ ] Design document reviewed by user

---

**Design Document Created:** 2026-09-21 20:45 MSK  
**Status:** Ready for Implementation Review
