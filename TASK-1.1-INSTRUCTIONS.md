# 🔴 TASK 1.1: FIX RETRYMANAGER DUPLICATE LOGIC

**Time:** 30-45 minutes  
**Status:** READY TO START  
**Priority:** CRITICAL (System will crash without this)

---

## 📍 WHAT YOU NEED TO DO

Fix a duplicate line in `src/copywriter/recovery.py` that overwrites the `next_retry` variable.

**The bug:**
```python
if retry_count > 5:
    next_retry = datetime.now() + timedelta(hours=4)
else:
    backoff_seconds = min([1, 2, 4, 8, 30*60][retry_count - 1], 30*60)
    next_retry = datetime.now() + timedelta(seconds=backoff_seconds)

next_retry = datetime.now() + timedelta(seconds=backoff_seconds)  # ❌ OVERWRITES!
# When retry_count > 5: backoff_seconds is UNDEFINED → NameError crash!
```

---

## ✅ STEP-BY-STEP INSTRUCTIONS

### Step 1: Find the file
```bash
# Open this file in your editor:
src/copywriter/recovery.py

# Go to around line 1114
# You should see the RetryManager class and retry logic
```

### Step 2: Locate the problematic code
Look for the `if retry_count > 5:` block around **lines 1114-1135**

It should look like this:
```python
def retry_failed_video(self, video_id: str, component: str, error: str):
    """Retry failed video with exponential backoff"""
    
    # Line 1114 area
    if retry_count > 5:
        next_retry = datetime.now() + timedelta(hours=4)  # Line 1116
        # Some other code...
    else:
        backoff_seconds = min([1, 2, 4, 8, 30*60][retry_count - 1], 30*60)
        next_retry = datetime.now() + timedelta(seconds=backoff_seconds)  # Line 1131
    
    # Line 1135 - THIS OVERWRITES next_retry!
    next_retry = datetime.now() + timedelta(seconds=backoff_seconds)
```

### Step 3: Make the fix

**Action 1: Delete the duplicate line**

Find this line (around line 1135):
```python
next_retry = datetime.now() + timedelta(seconds=backoff_seconds)
```

**DELETE IT COMPLETELY** ❌

The entire if/else block should look like:
```python
if retry_count > 5:
    next_retry = datetime.now() + timedelta(hours=4)
else:
    backoff_seconds = min([1, 2, 4, 8, 30*60][retry_count - 1], 30*60)
    next_retry = datetime.now() + timedelta(seconds=backoff_seconds)

# ✅ NO DUPLICATE LINE HERE!
```

**Action 2: Change timeout from 4 hours to 30 minutes**

Change this line:
```python
OLD: next_retry = datetime.now() + timedelta(hours=4)
NEW: next_retry = datetime.now() + timedelta(minutes=30)
```

Why? 30 minutes is reasonable for manual review. 4 hours is too long for customers to wait.

---

## 🧪 HOW TO TEST

After making the changes, run this command:

```bash
pytest tests/test_recovery.py::test_retry_timeout_30min -v
```

**Expected output:**
```
tests/test_recovery.py::test_retry_timeout_30min PASSED
```

If the test doesn't exist yet, create it. Add this to `tests/test_recovery.py`:

```python
def test_retry_timeout_30min():
    """Test that manual review timeout is 30 minutes"""
    from src.copywriter.recovery import RetryManager
    import datetime
    
    manager = RetryManager()
    # Simulate video with 6 retries
    result = manager.retry_failed_video(
        video_id='test-123',
        component='titlegen',
        error='Claude API failed',
        retry_count=6
    )
    
    # Should set next_retry to approximately 30 minutes from now
    assert result['next_retry_at'] is not None
    time_diff = result['next_retry_at'] - datetime.datetime.now()
    
    # Should be approximately 30 minutes (1800 seconds)
    # Allow 10 second buffer for test execution
    assert 1790 < time_diff.total_seconds() < 1810
```

---

## ✅ VERIFICATION CHECKLIST

After making the fix, verify:

- [ ] Found the duplicate line (around line 1135)
- [ ] Deleted the duplicate line
- [ ] Changed timeout from 4 hours to 30 minutes
- [ ] Saved the file
- [ ] Ran `pytest tests/test_recovery.py::test_retry_timeout_30min -v`
- [ ] Test passed ✅

---

## ⚠️ COMMON MISTAKES

❌ **Don't:** Delete the WRONG line. Make sure you delete line 1135, not line 1116!
❌ **Don't:** Leave the duplicate line in place
❌ **Don't:** Forget to change the timeout to 30 minutes

✅ **Do:** Keep the if/else block intact
✅ **Do:** Only delete the AFTER-the-if-else duplicate line

---

## 📊 WHAT THIS FIXES

| Problem | Before | After |
|---------|--------|-------|
| Duplicate line overwrites `next_retry` | ❌ YES | ✅ NO |
| NameError on retry_count > 5 | ❌ CRASH | ✅ FIXED |
| Manual review timeout | ❌ 4 hours | ✅ 30 min |
| Customers wait time | ❌ Forever | ✅ Reasonable |

---

## 🎯 WHEN YOU'RE DONE

1. **Verify** test passes
2. **Review** the code changes
3. **Commit** to git:
   ```bash
   git add src/copywriter/recovery.py
   git commit -m "🔧 Fix RetryManager duplicate logic - change timeout to 30 min"
   ```
4. **Move** to Task 1.2

---

## ⏱️ TIME ESTIMATE

- Reading this: 5 min
- Finding the code: 2 min
- Making the fix: 3 min
- Testing: 5 min
- **Total: 15 min** (well under 30-45 min estimate)

---

**READY? Open your editor and find `src/copywriter/recovery.py`** 🚀
