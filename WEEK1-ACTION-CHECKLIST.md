# 📋 WEEK 1: ACTION CHECKLIST - TASKS BY HOUR

**Week:** Sep 23-29, 2026  
**Hours:** 48-56 (8h per day)  
**Goal:** Complete Phase 1 (Critical Fixes) + Start Phase 2 (Real Tests)

---

## ⏰ DAY 1 (Monday, Sep 23) - CRITICAL BUGS FIX

### MORNING SESSION (4 hours: 09:00-13:00)

#### 🔴 HOUR 1-2: Fix RetryManager Duplicate Logic (Task 1.1)

**Files to edit:**
- `src/copywriter/recovery.py` (Lines 1114-1135)

**Step-by-step:**
```
1. Open recovery.py at line 1114
2. Find the if/else block that sets next_retry
3. DELETE the line that overwrites: 
   next_retry = datetime.now() + timedelta(seconds=backoff_seconds)
4. Change timeout from 4 hours to 30 minutes:
   OLD: next_retry = datetime.now() + timedelta(hours=4)
   NEW: next_retry = datetime.now() + timedelta(minutes=30)
5. Run test: 
   pytest tests/test_recovery.py::test_retry_timeout_30min -v
```

**Expected output:**
```
tests/test_recovery.py::test_retry_timeout_30min PASSED
```

**Estimated time:** 30 min  
**Buffer:** +15 min

✅ **DONE when:** Test passes + code reviewed

---

#### 🔴 HOUR 3-4: Fix Sanitization Case-Insensitive Bug (Task 1.2)

**Files to edit:**
- `src/copywriter/validation.py` (Lines 590-591)

**Step-by-step:**
```
1. Open validation.py at line 590
2. Import regex at top: import re
3. Replace dangerous_patterns loop:
   OLD: escaped.replace(pattern.lower(), f"[{pattern}]")
   NEW: regex = re.compile(re.escape(pattern), re.IGNORECASE)
        escaped = regex.sub(f"[{pattern}]", escaped)
4. Run tests:
   pytest tests/test_validation.py::test_sanitize_uppercase -v
   pytest tests/test_validation.py::test_sanitize_lowercase -v
   pytest tests/test_validation.py::test_sanitize_mixed_case -v
```

**Expected output:**
```
test_sanitize_uppercase PASSED
test_sanitize_lowercase PASSED
test_sanitize_mixed_case PASSED
```

✅ **DONE when:** All 3 tests pass

---

### AFTERNOON SESSION (4 hours: 14:00-18:00)

#### 🔴 HOUR 5: Fix TokenBucket Float Precision (Task 1.3)

**Files to edit:**
- `src/copywriter/rate_limiting.py` (Lines 639-662)

**Step-by-step:**
```
1. Open rate_limiting.py
2. Rewrite TokenBucket class to use integer arithmetic
3. Change self.tokens from float to self.tokens_remaining (int)
4. Scale by 1000: capacity * 1000
5. Update _refill() to use integer math
6. Run tests:
   pytest tests/test_rate_limiting.py -v
```

**Expected output:**
```
test_token_bucket_60_seconds PASSED
test_token_bucket_30_seconds PASSED
test_token_bucket_acquire_respects_limit PASSED
```

✅ **DONE when:** All rate limiting tests pass

**Time estimate:** 60 min (this is complex)

---

#### 🔴 HOUR 6: Add UNIQUE Constraint on external_id (Task 1.4)

**Files to edit:**
- `src/database/schema.py` (Lines 363-378)
- Create migration: `migrations/add_unique_external_id.sql`

**Step-by-step:**
```
1. Open schema.py, find CREATE TABLE videos
2. Change: external_id VARCHAR(255)
   To: external_id VARCHAR(255) UNIQUE NOT NULL
3. Add composite key after table creation:
   ALTER TABLE videos ADD CONSTRAINT unique_video_per_channel 
   UNIQUE (channel_id, external_id);
4. Create migration file with SQL
5. Run migration:
   psql multic_db < migrations/add_unique_external_id.sql
6. Test:
   pytest tests/test_database.py::test_unique_external_id -v
```

**Expected output:**
```
test_unique_external_id PASSED
IntegrityError when inserting duplicate: expected behavior ✓
```

✅ **DONE when:** Constraint added + migration works

---

#### 🔴 HOUR 7-8: Start DI Refactor (Task 1.5 - Part 1)

**Files to edit:**
- `src/copywriter/main.py` (Create CopywriterService class)

**Step-by-step:**
```
1. Open main.py
2. Create new class CopywriterService:
   - __init__(redis_client, max_concurrent=3, rate_per_minute=20)
   - self.redis_client
   - self.semaphore = Semaphore(max_concurrent)
   - self.rate_limiter = TokenBucket(...)
   - self.claude_client = Anthropic(timeout=30.0)
3. Move generate_titles() into class method
4. Update method to use self.semaphore + self.rate_limiter
5. Add timeout to Anthropic client (30 seconds)
```

✅ **DONE when:** CopywriterService class created + constructor tested

---

### END OF DAY 1

**Summary:**
- ✅ RetryManager duplicate logic fixed
- ✅ Sanitization case-insensitive bug fixed
- ✅ TokenBucket float precision fixed
- ✅ UNIQUE constraint added
- ✅ CopywriterService class started

**Tests to run at end of day:**
```bash
pytest tests/test_recovery.py tests/test_validation.py tests/test_rate_limiting.py tests/test_database.py -v
```

**Expected:** All tests PASS ✅

---

## ⏰ DAY 2 (Tuesday, Sep 24) - FINISH DI + MONITORING

### MORNING SESSION (4 hours: 09:00-13:00)

#### 🔴 HOUR 1-2: Finish DI Refactor (Task 1.5 - Part 2)

**Files to edit:**
- `src/copywriter/main.py` (Finish CopywriterService)

**Step-by-step:**
```
1. Update generate_titles() method:
   - Use self.semaphore: with self.semaphore:
   - Check rate limiter: if not self.rate_limiter.acquire():
   - Raise RateLimitExceeded
2. Update generate_descriptions() method (same pattern)
3. Update generate_comments() method (same pattern)
4. Create in main():
   redis_client = redis.Redis(host='localhost', port=6379)
   copywriter = CopywriterService(redis_client)
5. Test with real Redis:
   pytest tests/test_copywriter_service.py -v
```

**Expected output:**
```
test_concurrent_requests_limited_to_3 PASSED
test_rate_limit_max_20_per_minute PASSED
test_timeout_30_seconds PASSED
```

✅ **DONE when:** All DI tests pass + no globals remain

---

#### 🔴 HOUR 3-4: Add Prometheus Config (Task 1.6)

**Files to create/edit:**
- `docker-compose.yml` (Add prometheus + grafana)
- `prometheus.yml` (Create new)

**Step-by-step:**
```
1. Open docker-compose.yml
2. Add prometheus service:
   - image: prom/prometheus:latest
   - volumes: ./prometheus.yml
   - ports: 9090
3. Add grafana service:
   - image: grafana/grafana:latest
   - ports: 3000
   - depends_on: prometheus
4. Create prometheus.yml with copywriter job:
   scrape_configs:
   - job_name: 'copywriter'
     static_configs:
     - targets: ['localhost:8000']
5. Test:
   docker-compose up
   curl http://localhost:9090 (should get Prometheus UI)
   curl http://localhost:3000 (should get Grafana login)
```

**Expected output:**
```
Successfully started prometheus container
Successfully started grafana container
Both accessible at localhost:9090 and localhost:3000
```

✅ **DONE when:** docker-compose up works + services accessible

---

### AFTERNOON SESSION (4 hours: 14:00-18:00)

#### 🟠 HOUR 5-6: Add Alerting Integration (Task 1.7)

**Files to create:**
- `src/copywriter/alerting.py` (New file)

**Step-by-step:**
```
1. Create new file src/copywriter/alerting.py
2. Write AlertManager class:
   - __init__(): load SLACK_WEBHOOK_URL, PAGERDUTY_INTEGRATION_KEY from .env
   - alert_video_escalation(): send Slack + PagerDuty
   - _send_slack(): POST to webhook
   - _send_pagerduty(): POST to PagerDuty API
3. Add to .env:
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
   PAGERDUTY_INTEGRATION_KEY=...
4. In recovery.py, import AlertManager
5. When retry_count >= 5:
   alert_manager.alert_video_escalation(video_id, retry_count, error)
6. Test:
   pytest tests/test_alerting.py -v
```

**Expected output:**
```
test_send_slack_alert PASSED
test_send_pagerduty_alert PASSED
test_escalation_triggers_alert PASSED
```

✅ **DONE when:** Alerts working for video escalation

---

#### 🟠 HOUR 7-8: Convert Pseudocode Tests to Real Code (Task 1.8 - Start)

**Files to create:**
- `tests/test_negative_cases.py` (New file with real test functions)

**Step-by-step:**
```
1. Create tests/test_negative_cases.py
2. Write test class TestInputValidation with 4 test functions:
   - test_sanitize_blocks_system_prompt_injection
   - test_sanitize_blocks_uppercase_injection
   - test_sanitize_preserves_normal_text
   - test_sanitize_handles_utf8_emoji
3. Write test class TestJSONParsing with 5 test functions:
   - test_parse_valid_json
   - test_parse_trailing_comma_fails
   - test_parse_incomplete_array_fails
   - test_parse_incomplete_json_fails
   - test_parse_null_value_fails
4. Run tests:
   pytest tests/test_negative_cases.py -v
```

**Expected output:**
```
test_sanitize_blocks_system_prompt_injection PASSED
test_sanitize_blocks_uppercase_injection PASSED
test_parse_valid_json PASSED
test_parse_trailing_comma_fails PASSED
...9 more PASSED
```

✅ **DONE when:** 9+ real test functions pass

---

### END OF DAY 2

**Summary:**
- ✅ DI refactor completed
- ✅ Prometheus + Grafana added to docker-compose
- ✅ Alerting system integrated
- ✅ Real negative case tests created

**Tests to run at end of day:**
```bash
pytest tests/test_copywriter_service.py tests/test_alerting.py tests/test_negative_cases.py -v
```

**Expected:** All tests PASS ✅

---

## 📊 END OF WEEK 1: PHASE 1 COMPLETE ✅

### What we've done:
- ✅ Fixed 8 critical blockers
- ✅ Replaced globals with DI
- ✅ Added monitoring infrastructure
- ✅ Added alerting system
- ✅ Created 20+ real test functions

### Tests passing:
```
tests/test_recovery.py ............................ 5 passed
tests/test_validation.py .......................... 4 passed
tests/test_rate_limiting.py ....................... 6 passed
tests/test_database.py ............................ 3 passed
tests/test_copywriter_service.py .................. 8 passed
tests/test_alerting.py ............................ 5 passed
tests/test_negative_cases.py ....................... 9 passed
```

**Total: 40 tests passing** ✅

---

## 🎯 NEXT: WEEK 2 (Phase 2: Real Tests)

After Day 2, we move to WEEK 2:
- Days 3-4: Write 30+ more unit tests
- Days 5-6: Integration & concurrency tests
- Days 7-9: Production deployment

---

## ✅ CHECKLIST FOR WEEK 1

**Day 1:**
- [ ] Hour 1-2: RetryManager fixed
- [ ] Hour 3-4: Sanitization fixed
- [ ] Hour 5: TokenBucket fixed
- [ ] Hour 6: UNIQUE constraint added
- [ ] Hour 7-8: DI class started

**Day 2:**
- [ ] Hour 1-2: DI class finished
- [ ] Hour 3-4: Prometheus added
- [ ] Hour 5-6: Alerting integrated
- [ ] Hour 7-8: Tests created

---

**Ready to start Day 1?** 🚀

First commit when Day 1 complete:
```bash
git add .
git commit -m "🔧 Phase 1: Fix 8 critical blockers - RetryManager, Sanitization, TokenBucket, DI"
```
