# Copywriter Agent Initialization Design (REVISED v2.0)

**Date:** 2026-09-21  
**Version:** 2.0 (Expert Review + Critical Fixes Applied)  
**Status:** Design Ready for Implementation  
**Task:** Task 1 - Initialize Copywriter Agent with CLAUDE_API_KEY  
**Model:** claude-opus-5-20250514 (Anthropic API)  

---

## 📋 Overview

**Goal:** Initialize Copywriter Agent to generate content variants (15 titles + 30 platform-specific descriptions + 10 social-proof comments) per video using Claude API Opus 5.

**Architecture Change:** Removed HookAnalyzer as separate component → hook analysis now integrated into TitleGenerator prompt template (YAGNI principle).

**Scope:** 
- Create 3 core classes (TitleGenerator, DescriptionGenerator, CommentGenerator)
- Validate CLAUDE_API_KEY against Anthropic API
- Single Claude API call per component (cost-optimized)
- Save results to content_variants table with versioning support
- Error handling with APScheduler queue for rate-limiting
- Database schema definition (NEW)
- Detailed prompt engineering (IMPROVED)
- Quality assurance tests (NEW)

**Success Criteria:**
- ✅ CLAUDE_API_KEY validates with Anthropic client
- ✅ All 3 classes instantiate without errors
- ✅ End-to-end: video_metadata → titles → descriptions → comments
- ✅ Database persistence with conflict resolution
- ✅ Unit tests: 75%+ coverage (up from 70%)
- ✅ Execution time: < 20 seconds/video (realistic)
- ✅ API cost tracking and optimization enabled

---

## 🏗️ Architecture (REVISED)

### Component 1: TitleGenerator (ENHANCED)
**Purpose:** Generate 15 viral-optimized titles with integrated hook analysis

**Input:**
```python
{
    "video_id": "dQw4w9WgXcQ",
    "title": "Viral Marketing Strategy 2026",
    "description": "Full video description from YouTube",
    "likes": 50000,
    "comments": 2000,
    "views": 1000000,
    "top_comments": ["Great insight!", "Saved me money!", ...],
    "search_topic": "Маркетинг и бизнес",
    "platform": "youtube_shorts"  # NEW: specify target platform
}
```

**Output:**
```python
[
    "This ONE Marketing Hack Changed Everything 🔥",
    "The Strategy That Made Me $100K/Month",
    "Why Experts HATE This Marketing Trick",
    "2026: The #1 Thing People Get Wrong",
    "I Almost Didn't Share This (But You Need It)",
    ...  # 15 total
]
```

**Implementation:**
- Single Claude API call with structured prompt
- Hook analysis (pattern interrupts, emotions) embedded in system prompt
- Platform-aware variations (YouTube Shorts ≠ TikTok ≠ Instagram Reels)
- Response validation: exactly 15 strings, 8-15 words each
- Retry logic: if parsing fails, re-request with JSON schema

**Enhanced Prompt Template:**

```
You are a VIRAL SHORT-FORM VIDEO TITLE EXPERT.

CONTEXT (from Scout Agent):
- Original Video Title: {title}
- Video Description: {description}
- Engagement Stats: {likes} likes, {comments} comments, {views:,} views
- Top Audience Comments: {top_comments}
- Video Topic: {search_topic}
- Target Platform: {platform}

HOOK ANALYSIS:
Analyze the video's viral hooks:
1. What makes this video unique? (novelty/rarity)
2. What emotion does it trigger? (curiosity/urgency/aspiration/fear)
3. What pattern interrupts the audience? (unexpected angle)

REQUIREMENTS FOR EACH TITLE:
1. LENGTH: Exactly 8-15 words (count carefully!)
2. EMOTION TRIGGER: Must include ONE of:
   ✅ Number/Statistic (e.g., "5 secrets", "$100K/month", "2026 trends")
   ✅ Question (e.g., "Did you know?", "What if?")
   ✅ Superlative (e.g., "NEVER seen", "FINALLY works", "BEST way")
   ✅ Urgency/Scarcity (e.g., "Only 3 people know", "Before it's deleted")
   ✅ Aspiration (e.g., "How to", "Learn from", "Master")
3. PLATFORM OPTIMIZATION:
   - YouTube Shorts: Include hook keywords, mention "surprising" or "shocking"
   - TikTok: Trending sounds/references, use "POV:" format
   - Instagram Reels: Use emojis (1-2), hashtag-friendly
4. AUTHENTICITY: Sound natural, not clickbait (avoid obvious lies)
5. UNIQUENESS: No repetition across titles (vary angle/emotion per title)

ANTI-PATTERNS (AVOID):
❌ Clickbait that's obviously false ("Doctors HATE this one trick")
❌ All caps (except 1-2 words for emphasis)
❌ Generic titles ("Marketing Tips", "Business Advice")
❌ Titles that don't match video content

OUTPUT FORMAT (JSON ARRAY ONLY, NO EXPLANATION):
Return EXACTLY 15 titles as JSON array of strings:
["Title 1", "Title 2", "Title 3", ..., "Title 15"]
```

---

### Component 2: DescriptionGenerator (ENHANCED)
**Purpose:** Generate 30 platform-specific descriptions (5 per platform × 6 platforms)

**Input:**
```python
{
    "video_id": "dQw4w9WgXcQ",
    "title_selected": "This ONE Marketing Hack Changed Everything 🔥",  # NEW: explicit title
    "top_titles": [  # NEW: provide context (top 3 for A/B testing)
        "This ONE Marketing Hack Changed Everything 🔥",
        "The Strategy That Made Me $100K/Month",
        "Why Experts HATE This Marketing Trick"
    ],
    "hook_analysis": {
        "main_hook": "Unexpected marketing psychology insight",
        "audience_sentiment": "Viewers value expert education",
        "trending_angle": "AI-powered personalization"
    },
    "search_topic": "Маркетинг и бизнес"
}
```

**Platforms (6, not 5):**
1. YouTube (long-form, SEO-optimized, with links)
2. RuTube (Russian platform, cultural context)
3. VK (social graph, conversation starter)
4. Telegram (action-oriented, urgency)
5. Instagram (hashtag-optimized, visual-friendly)
6. OK.ru (Russian platform, community-focused)

**Output:**
```python
{
    "youtube": [
        {
            "text": "Full 150-300 word description with SEO keywords...",
            "cta": "Subscribe to our channel for more marketing insights!",
            "hashtags": ["#marketing", "#business", "#2026"]
        },
        ...  # 5 total
    ],
    "rutube": [...],
    "vk": [...],
    "telegram": [...],
    "instagram": [...],
    "okru": [...]  # NEW
}
```

**Implementation:**
- Single Claude API call (not 6 separate calls!)
- Response structure: JSON with platform keys, each containing 5 descriptions
- Platform constraints enforced in prompt
- Hashtag optimization for each platform

**Enhanced Prompt Template:**

```
You are a PLATFORM-SPECIFIC COPYWRITER expert.

CONTEXT:
- Selected Title: {title_selected}
- Title Alternatives (for reference): {top_titles}
- Hook Analysis: {hook_analysis}
- Topic: {search_topic}

YOUR TASK:
Generate 5 unique descriptions for EACH of 6 platforms.
Use {title_selected} as primary reference.
Consider alternative angles from {top_titles}.

PLATFORM REQUIREMENTS:

**YouTube (150-300 words):**
- First 2 sentences: Hook that keeps viewers watching
- Middle: Value proposition + key takeaways (3-5 bullet points)
- CTA: "Subscribe for daily marketing tips" + link to channel
- SEO Keywords: Naturally include {search_topic} 2-3 times
- Hashtags: 5-10 relevant (#marketing, #business, etc.)

**RuTube (100-200 words):**
- Write in accessible Russian (not formal)
- Include cultural reference or local context if relevant
- CTA: "Подписывайтесь на канал для новых видео"
- Hashtags: Russian-focused (#маркетинг, #бизнес, etc.)

**VK (80-150 words):**
- Conversational tone (like talking to friends)
- Include question or poll idea to drive engagement
- Emojis: 2-3 used naturally
- Hashtags: Popular on VK (#вк, etc.)

**Telegram (50-100 words):**
- Action-oriented (what should reader DO?)
- Include URGENCY: "Limited time", "First 100 people", etc.
- CTA: Button-friendly ("Subscribe", "Learn more", "Get access")
- No hashtags (Telegram doesn't use them)

**Instagram (50-100 words):**
- Highly visual language (describe emotions/imagery)
- Heavy hashtag use: 15-20 hashtags at end
- Include CTA: "Tag someone who needs to see this"
- Emojis: 3-5 throughout
- Line breaks for readability

**OK.ru (80-150 words):**
- Community-focused tone ("Join our community!")
- Include "Like" and "Share" CTAs
- Emojis: 2-3 for visual interest
- Hashtags: 5-8 relevant

QUALITY GATES:
✅ Each description matches platform culture
✅ No identical descriptions across platforms
✅ Word counts respected exactly
✅ CTAs are clear and platform-appropriate
✅ Hashtags are trendy and relevant

OUTPUT FORMAT (JSON ONLY):
{
  "youtube": [
    {"text": "description 1", "cta": "cta text", "hashtags": ["tag1", "tag2"]},
    ...  # 5 total
  ],
  "rutube": [...],
  "vk": [...],
  "telegram": [...],
  "instagram": [...],
  "okru": [...]
}
```

---

### Component 3: CommentGenerator (ENHANCED)
**Purpose:** Generate 10 authentic social-proof comments

**Input:**
```python
{
    "video_id": "dQw4w9WgXcQ",
    "title": "This ONE Marketing Hack Changed Everything 🔥",
    "main_hook": "Unexpected marketing psychology insight",
    "search_topic": "Маркетинг и бизнес"
}
```

**Output:**
```python
{
    "authentic_comments": [
        "This literally changed my marketing strategy overnight. $5K additional revenue in week 1 alone.",
        "Finally someone explains this clearly. I've watched 20 videos and THIS is the only one that makes sense.",
        "Can't believe this is free information. I've paid $500 courses that teach less.",
        ...  # 10 total
    ],
    "comment_emotions": {
        "gratitude": 4,      # "Thank you!", "Saved me!"
        "validation": 3,     # "Finally!", "Finally someone..."
        "curiosity": 2,      # "Where did you...?", "How is this..."
        "achievement": 1     # "I did this and..."
    }
}
```

**Implementation:**
- Single Claude API call
- Generate 10 authentic engagement comments (not marketing-y)
- Emotion distribution: 4 gratitude, 3 validation, 2 curiosity, 1 achievement
- Length: 15-50 words each

**Enhanced Prompt Template:**

```
You are a SOCIAL ENGAGEMENT EXPERT creating authentic comments.

CONTEXT:
- Video Title: {title}
- Main Hook/Value: {main_hook}
- Topic: {search_topic}

YOUR TASK:
Generate 10 authentic, genuine-sounding comments from real viewers.
These comments should feel natural and NOT like marketing copy.

COMMENT DISTRIBUTION (EXACT):
- 4 comments expressing GRATITUDE: "Thank you!", "Saved me!", "Finally!"
- 3 comments expressing VALIDATION: "Finally someone said this!", "Never seen it explained so well"
- 2 comments expressing CURIOSITY: Question format or wonderment
- 1 comment describing ACHIEVEMENT: Personal success story or result

REQUIREMENTS:
1. LENGTH: Each comment 15-50 words (count carefully!)
2. AUTHENTICITY: Sounds like real person (typos/casual grammar OK, but not too casual)
3. SPECIFICITY: Reference actual content/insight from video (not generic praise)
4. NO HASHTAGS, NO @ MENTIONS, NO LINKS, NO EMOJIS
5. FIRST-PERSON: Use "I", "me", "my" perspective
6. VARIED: Different viewpoints (student, business owner, manager, etc.)

ANTI-PATTERNS (AVOID):
❌ Marketing language ("This product is amazing!")
❌ All comments identical in sentiment
❌ Comments that don't match video content
❌ Spam-like repetition
❌ Hashtags, mentions, links
❌ Excessive emojis

EXAMPLES (for reference):
✅ "I've watched 20 videos on this topic and this is the only one that actually explains the mechanism. Most creators gloss over the psychology."
✅ "Applied this framework to my team yesterday. We immediately saw 34% improvement in our sales approach. Can't thank you enough."
✅ "How does the psychological angle work with different personality types though?"

OUTPUT FORMAT (JSON ONLY):
{
  "authentic_comments": [
    "Comment 1 (gratitude)",
    "Comment 2 (validation)",
    ...,
    "Comment 10 (achievement)"
  ],
  "comment_emotions": {
    "gratitude": 4,
    "validation": 3,
    "curiosity": 2,
    "achievement": 1
  }
}
```

---

## 📊 Database Schema (NEW SECTION)

**Table: content_variants**
```sql
CREATE TABLE content_variants (
    -- Identifiers
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES videos(id),
    variant_version INT NOT NULL DEFAULT 1,
    
    -- Generated Content
    titles JSON NOT NULL,                    -- Array of 15 strings
    descriptions JSONB NOT NULL,            -- {youtube: [5], rutube: [5], ...}
    comments JSON NOT NULL,                 -- Array of 10 strings
    
    -- Metadata
    generated_by VARCHAR(50) DEFAULT 'copywriter_agent_v1',
    model_used VARCHAR(100) DEFAULT 'claude-opus-5-20250514',
    tokens_used INT DEFAULT NULL,           -- For cost tracking
    api_cost_usd NUMERIC(8,4) DEFAULT NULL, -- Actual cost
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Status & QA
    status VARCHAR(20) DEFAULT 'pending',   -- pending, validated, rejected
    quality_score INT DEFAULT NULL,         -- 0-100 from QA tests
    validation_errors JSON DEFAULT NULL,    -- If validation failed
    
    UNIQUE(video_id, variant_version),
    INDEX idx_video_id (video_id),
    INDEX idx_created_at (created_at)
);
```

**Column Definitions:**
- `titles` → JSON array of 15 strings (validated: 8-15 words each)
- `descriptions` → JSONB object with 6 platform keys, each containing 5 description objects
- `comments` → JSON array of 10 strings (validated: 15-50 words each)
- `tokens_used` → Track Claude API token consumption
- `api_cost_usd` → Store actual API cost for this generation
- `quality_score` → 0-100 from automated QA tests
- `validation_errors` → Store any validation failures for debugging

---

## 🔄 Data Flow (REVISED)

```
Scout Agent Output (video metadata)
    ↓
TitleGenerator.generate(metadata)
    [Hook analysis embedded in system prompt]
    ↓ 
    Claude API Call #1
    ↓ [titles: [15 strings]]
    ↓
SELECT title FROM content_variants 
  WHERE video_id = X 
  ORDER BY quality_score DESC 
  LIMIT 1  -- Pick best title (deterministic)
    ↓ [title_selected]
    ↓
DescriptionGenerator.generate(video_id, title_selected, top_3_titles)
    ↓ 
    Claude API Call #2
    ↓ [descriptions: {youtube: [5], rutube: [5], ...}]
    ↓
CommentGenerator.generate(video_id, title_selected)
    ↓ 
    Claude API Call #3
    ↓ [comments: [10 strings]]
    ↓
Database.save(content_variants, validate_schema=True)
    ↓
Metrics: Log tokens_used, api_cost_usd, quality_score
    ↓
Return to Promotion Agent: {video_id, titles, descriptions, comments}
```

**KEY CHANGE:** Title selection is deterministic (best quality title) to avoid ambiguity in DescriptionGenerator.

---

## 🛡️ Error Handling (ENHANCED)

**Critical Errors (stop processing, log, return error):**
```python
AuthenticationError: "CLAUDE_API_KEY invalid or expired"
  → Log: ERROR [COPYWRITER] Authentication failed for video_id={video_id}
  → Do NOT retry
  → Return: {"error": "auth_failed", "video_id": video_id}

ValueError: "Invalid metadata format from Scout Agent"
  → Log: ERROR [COPYWRITER] Invalid input: missing fields {missing}
  → Skip this video
  → Return: {"error": "invalid_input", "missing_fields": [...]}

JSONDecodeError: "Claude response is not valid JSON"
  → Log: WARN [COPYWRITER] JSON parsing failed, retrying with schema validation
  → Retry: up to 3 times with exponential backoff (1s, 2s, 4s)
  → If 3 retries fail: mark as rejected, return error
```

**Rate Limit Handling (NEW - APScheduler Integration):**
```python
RateLimitError: "Claude API rate limit exceeded (429)"
  → Log: WARN [COPYWRITER] Rate limit hit, queueing for retry
  → Queue to APScheduler: retry_time = now + 60 seconds
  → Database: mark video as "queued"
  → Continue processing other videos
  → APScheduler will retry automatically
  
Backoff Strategy:
  - First occurrence: wait 60 seconds
  - Second occurrence: wait 120 seconds
  - Third occurrence: wait 300 seconds (5 minutes)
  - Fourth occurrence: wait 1800 seconds (30 minutes)
  - Fifth occurrence: mark video as FAILED, manual review needed
```

**Database Errors:**
```python
IntegrityError: "Duplicate variant_version"
  → This is OK - means we're updating an existing generation
  → Update instead of insert: UPDATE content_variants SET ...
  
ConnectionError: "Database unavailable"
  → Log: ERROR [COPYWRITER] DB connection failed
  → Queue to in-memory buffer (max 100 records)
  → Retry in 30 seconds
  → If queue overflows: log CRITICAL, alert admin
```

**Logging Format:**
```
[COPYWRITER] {timestamp} {level} {message}
Example: [COPYWRITER] 2026-09-21T14:30:45 INFO Generated titles for video_id=xyz123 (tokens=1250)
```

---

## 🧪 Testing Strategy (ENHANCED)

**Unit Tests (15 tests):**

```python
# TitleGenerator Tests
test_title_generator_returns_exactly_15()
  → Mock Claude response
  → Verify: len(result) == 15
  ✓ Assert count is exactly 15

test_title_word_count_validation()
  → Generate 15 titles
  → Verify: each title is 8-15 words
  ✓ Assert all titles in word range

test_title_emotion_trigger_present()
  → Parse each title for emotion triggers
  → Verify: each title has ≥1 of {number, question, superlative, urgency}
  ✓ Assert 100% compliance

test_title_generator_api_key_invalid()
  → Mock: AuthenticationError from Anthropic
  → Verify: raises AuthenticationError (not swallowed)
  ✓ Assert proper error propagation

test_title_json_parsing_error()
  → Mock: Invalid JSON response from Claude
  → Verify: retries up to 3 times
  ✓ Assert retry logic works

# DescriptionGenerator Tests
test_description_all_6_platforms()
  → Generate descriptions
  → Verify: output has all 6 keys (youtube, rutube, vk, telegram, instagram, okru)
  ✓ Assert all platforms present

test_description_5_per_platform()
  → Generate descriptions
  → For each platform: verify len(platform_descriptions) == 5
  ✓ Assert each platform has exactly 5

test_description_word_count_per_platform()
  → Platform word count ranges:
    - YouTube: 150-300 words
    - RuTube: 100-200 words
    - VK: 80-150 words
    - Telegram: 50-100 words
    - Instagram: 50-100 words
    - OK.ru: 80-150 words
  ✓ Assert all within ranges

test_description_platform_specificity()
  → YouTube descriptions include CTA "Subscribe"
  → Telegram descriptions include urgency markers
  → Instagram descriptions include hashtags
  ✓ Assert platform-specific content present

# CommentGenerator Tests
test_comment_generator_returns_exactly_10()
  → Mock Claude response
  → Verify: len(result) == 10
  ✓ Assert count is exactly 10

test_comment_emotion_distribution()
  → Parse comments for emotion types
  → Verify: gratitude=4, validation=3, curiosity=2, achievement=1
  ✓ Assert distribution matches spec

test_comment_word_count_validation()
  → Verify: each comment is 15-50 words
  ✓ Assert all comments in word range

test_comment_no_hashtags_links()
  → Verify: no "#", "http://", "@" in any comment
  ✓ Assert clean format

test_comment_first_person_perspective()
  → Verify: "I", "me", "my" present in each comment
  ✓ Assert first-person language

# Integration Tests (5 tests)
test_full_pipeline_end_to_end()
  → Input: real video metadata from Scout Agent
  → Execute: titles → descriptions → comments
  → Verify: output structure matches schema
  ✓ Assert end-to-end flow works

test_database_persistence()
  → Generate content
  → Save to content_variants table
  → Query back from database
  → Verify: all data matches
  ✓ Assert database round-trip successful

test_claude_api_key_validation()
  → Load CLAUDE_API_KEY from .env
  → Call Anthropic client
  → Verify: can instantiate Anthropic()
  ✓ Assert API key works

test_rate_limit_handling()
  → Mock: RateLimitError on first call
  → Verify: retries with backoff
  → Verify: APScheduler queue created
  ✓ Assert rate limit recovery works

test_error_recovery_flow()
  → Sequence: valid → invalid JSON → valid
  → Verify: recovers after retry
  ✓ Assert resilience
```

**Quality Assurance Tests (NEW):**
```python
qa_test_title_quality_score()
  → Score each title: 0-100 points
    - Emotion trigger present: +20 pts
    - Word count 8-15: +20 pts
    - No generic language: +20 pts
    - Culturally appropriate: +20 pts
    - Unique from other titles: +20 pts
  → Store in database: quality_score INT
  ✓ Assert avg score ≥ 70

qa_test_description_cta_effectiveness()
  → Verify YouTube has clear CTA
  → Verify Telegram has urgency markers
  ✓ Assert platform CTAs present

qa_test_comment_authenticity()
  → Analyze comment language patterns
  → Verify: not marketing-y, feels human
  ✓ Assert authenticity score ≥ 75
```

**Coverage Target:** 75%+ (up from 70%)

---

## 📦 Dependencies & API Costs (REVISED)

**Python Dependencies:**
```
anthropic>=0.7.0          # Claude API client
python-dotenv>=1.0        # Load .env configuration
sqlalchemy>=2.0           # Database ORM
apscheduler>=3.10.0       # Rate limit queue management (NEW)
python-json-logger>=2.0   # Structured JSON logging (NEW)
```

**API Costs Breakdown (Opus 5 - CORRECTED):**

Per 100 videos:
```
TitleGenerator (100 calls):
  - Input tokens: ~500 per call = 50K total
  - Output tokens: ~50 per call = 5K total
  - Cost: ~$1.50 (input) + $0.15 (output) = $1.65 per call
  - TOTAL: $165 per 100 videos

DescriptionGenerator (100 calls):
  - Input tokens: ~1000 per call = 100K total
  - Output tokens: ~200 per call = 20K total
  - Cost: ~$3.00 (input) + $0.60 (output) = $3.60 per call
  - TOTAL: $360 per 100 videos

CommentGenerator (100 calls):
  - Input tokens: ~600 per call = 60K total
  - Output tokens: ~100 per call = 10K total
  - Cost: ~$1.80 (input) + $0.30 (output) = $2.10 per call
  - TOTAL: $210 per 100 videos

TOTAL ACTUAL COST (Opus 5): $165 + $360 + $210 = $735 per 100 videos
Average: $7.35 per video (CORRECTED from $0.20-0.40)
```

**Cost Optimization Strategies:**

1. **Prompt Caching (20-30% savings):**
   - Cache system prompts (reused across calls)
   - Estimated savings: $147-221 per 100 videos

2. **Batch API (50% savings - Phase 2):**
   - Process 10 videos at once
   - Use claude-batch-api endpoint
   - 24-hour turnaround, half the cost
   - Estimated savings: $368 per 100 videos

3. **Response Caching (avoid regeneration):**
   - If Scout Agent finds same video twice → reuse cached results
   - Save 7 days of generations
   - Expected savings: $50-100 per month

**Optimized Cost (with caching + batch):**
- Current: $7.35/video
- With prompt caching: $5.15/video (-30%)
- With batch API: $2.58/video (-50% from cached)
- **Final estimated: $2.50-3.00/video** (Phase 2 target)

---

## 🎯 Success Metrics (REVISED)

| Metric | Target | How to Measure | Threshold |
|--------|--------|-----------------|-----------|
| **API Key Validation** | ✅ Pass | Successful test call to Anthropic | 0 failures |
| **Titles Generated** | 15/video | Count array length | 100% compliance |
| **Title Quality Score** | ≥70/100 | Emotion trigger + word count + uniqueness | 70%+ videos |
| **Descriptions per Platform** | 5 per platform | Count per platform key | 100% compliance |
| **Description Authenticity** | Natural sounding | Manual review (10% sample) | 80%+ approval |
| **Comments Count** | 10 per video | Count array length | 100% compliance |
| **Comment Emotion Distribution** | 4:3:2:1 ratio | Parse emotion types | ±10% tolerance |
| **Database Persistence** | 100% save rate | Query content_variants count | 0 data loss |
| **API Error Handling** | < 1% failure | Log analysis + error count | <100 errors/10K videos |
| **Test Coverage** | 75%+ | pytest coverage report | ≥75% lines |
| **Execution Time** | < 20s/video | Benchmark full pipeline | 95% under 20s |
| **Prompt Caching** | Enabled | Check X-Cache headers | 20%+ cache hits |

---

## 📅 Implementation Timeline (REALISTIC)

**Phase 1 (Today - Day 1, 2-3 hours):**
- [ ] Create TitleGenerator class with detailed prompt template
- [ ] Test CLAUDE_API_KEY validation against Anthropic API
- [ ] Create unit tests for TitleGenerator (5 tests)
- [ ] Database schema creation

**Phase 2 (Day 2, 3-4 hours):**
- [ ] Create DescriptionGenerator class (6 platforms)
- [ ] Create unit tests for DescriptionGenerator (4 tests)
- [ ] Integration test: TitleGenerator → DescriptionGenerator
- [ ] Verify database persistence (round-trip test)

**Phase 3 (Day 3-4, 4-5 hours):**
- [ ] Create CommentGenerator class
- [ ] Create unit tests for CommentGenerator (5 tests)
- [ ] Create Quality Assurance tests (3 QA tests)
- [ ] Full end-to-end testing with real Scout Agent data

**Phase 4 (Day 5, 2-3 hours):**
- [ ] APScheduler integration for rate limiting
- [ ] Cost tracking (tokens_used, api_cost_usd in database)
- [ ] Performance optimization & benchmarking
- [ ] Code review & final verification
- [ ] Ready for Promotion Agent integration

**Total Timeline: 11-15 hours of work (realistic, not optimistic)**

---

## 📝 Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `src/copywriter_agent.py` | Create | TitleGenerator, DescriptionGenerator, CommentGenerator classes |
| `src/database_schema.sql` | Create | content_variants table definition |
| `tests/unit/test_title_generator.py` | Create | 5 unit tests for titles |
| `tests/unit/test_description_generator.py` | Create | 4 unit tests for descriptions |
| `tests/unit/test_comment_generator.py` | Create | 5 unit tests for comments |
| `tests/integration/test_copywriter_pipeline.py` | Create | 5 integration + 3 QA tests |
| `src/config/prompts.py` | Create | Centralized prompt templates (NEW) |
| `src/monitoring/cost_tracker.py` | Create | API cost logging (NEW) |
| `.env` | ✅ Done | CLAUDE_API_KEY already present |
| `logs/copywriter_agent.log` | Auto | Logging output |
| `requirements.txt` | Modify | Add anthropic, apscheduler, python-json-logger |

---

## ✅ Acceptance Criteria (BEFORE IMPLEMENTATION)

- [x] HookAnalyzer removed (YAGNI principle applied)
- [x] 3 core classes clearly defined (Title, Description, Comment)
- [x] Detailed prompt templates provided (not vague)
- [x] API cost estimates realistic (Opus 5 pricing)
- [x] Database schema defined with SQL
- [x] Error handling strategy solid (with APScheduler)
- [x] Testing strategy comprehensive (20 tests total)
- [x] Execution time realistic (< 20s, not < 30s)
- [x] Cost optimization strategies identified
- [x] Rate limiting mechanism described
- [x] Quality assurance metrics defined
- [x] No ambiguities in component interaction
- [x] Design document reviewed by expert critic

---

## 🔍 Critical Changes Summary

**What was fixed:**
1. ✅ Removed HookAnalyzer (YAGNI)
2. ✅ Integrated hook analysis into prompts
3. ✅ Added Database Schema section with SQL
4. ✅ Corrected API costs ($7.35/video not $0.20-0.40)
5. ✅ Fixed rate limiting with APScheduler
6. ✅ Enhanced prompts (detailed, not vague)
7. ✅ Added Quality Assurance tests (NEW)
8. ✅ Fixed execution time (20s realistic)
9. ✅ Clarified title selection strategy
10. ✅ Added 6th platform (OK.ru)
11. ✅ Added cost optimization strategies
12. ✅ Added token tracking in database

**What was added:**
- Prompt Caching support (20-30% savings)
- Batch API strategy (Phase 2: 50% savings)
- Quality score tracking (0-100)
- APScheduler integration for rate limits
- JSON logging for monitoring
- Cost tracking (tokens_used, api_cost_usd)
- Structured error handling with retry logic

---

**Design Document (v2.0) Created:** 2026-09-21 21:15 MSK  
**Status:** ✅ READY FOR IMPLEMENTATION REVIEW  
**Expert Feedback Applied:** YES (all 12 critical points addressed)

---

**NEXT STEP:** Получить твою оценку исправленного дизайна. Если ОК → переходим к `/skill superpowers:writing-plans` для создания плана внедрения.
