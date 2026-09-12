# 🎬 Video Skills & Plugins Installation Guide

**Date:** 2026-09-12  
**Status:** Installing 6 video-specific skills/plugins  
**Purpose:** Complete video handling ecosystem for MULTIC

---

## 📋 6 Skills/Plugins to Install

### 1️⃣ **Video-Downloader** ⏳
**GitHub:** ComposioHQ/awesome-claude-skills/video-downloader  
**Type:** Claude Skill  
**Status:** Cloning

#### What it does:
- Download videos from YouTube, TikTok, Instagram, Telegram
- Extract audio from videos
- Convert formats
- Batch processing

#### Installation:
```bash
# When clone completes
cp -r /tmp/awesome-claude-skills/video-downloader \
  ~/.claude/skills/

# Activate
/video-downloader "Download YouTube video"
```

#### Use in MULTIC:
```
Scout Agent → Find videos on YouTube
Video-Downloader → Download them locally
Copywriter → Analyze structure
```

#### Commands:
```bash
/video-downloader "youtube.com/watch?v=xxx"
/video-downloader "Extract audio from video.mp4"
/video-downloader "Convert to webm format"
```

---

### 2️⃣ **Content-Research-Writer** ⏳
**GitHub:** ComposioHQ/awesome-claude-skills/content-research-writer  
**Type:** Claude Skill  
**Status:** Cloning

#### What it does:
- Research content topics
- Write research-backed content
- Generate outlines
- Create variations

#### Installation:
```bash
# When clone completes
cp -r /tmp/awesome-claude-skills/content-research-writer \
  ~/.claude/skills/

# Activate
/content-research-writer "Write about viral marketing"
```

#### Use in MULTIC:
```
MasterAI → Decide topic
Content-Research-Writer → Research & outline
Copywriter → Create variations
Video-Editor → Generate captions
```

#### Commands:
```bash
/content-research-writer "Research viral TikTok trends"
/content-research-writer "Write 3 outline variations"
/content-research-writer "Research audience psychology"
```

---

### 3️⃣ **Competitive-Ads-Extractor** ⏳
**GitHub:** ComposioHQ/awesome-claude-skills/competitive-ads-extractor  
**Type:** Claude Skill  
**Status:** Cloning

#### What it does:
- Extract competitor ads from social media
- Analyze ad copy
- Identify successful patterns
- Track competitors

#### Installation:
```bash
# When clone completes
cp -r /tmp/awesome-claude-skills/competitive-ads-extractor \
  ~/.claude/skills/

# Activate
/competitive-ads-extractor "Find top TikTok ads in niche"
```

#### Use in MULTIC:
```
MasterAI → Research competition
Competitive-Ads-Extractor → Extract examples
Content-Research-Writer → Analyze patterns
Copywriter → Create better content
```

#### Commands:
```bash
/competitive-ads-extractor "Extract top TikTok ads trending"
/competitive-ads-extractor "Analyze competitor messaging"
/competitive-ads-extractor "Find highest engagement patterns"
```

---

### 4️⃣ **Claude-Video** ⏳
**GitHub:** bradautomates/claude-video  
**Type:** Claude Plugin  
**Status:** Cloning

#### What it does:
- /watch command for video analysis
- Extract frames from videos
- Generate video descriptions
- Caption generation

#### Installation:
```bash
# Copy to skills directory
cp -r /tmp/claude-video ~/.claude/skills/

# Or install as plugin
# Follow: https://github.com/bradautomates/claude-video
```

#### Use in MULTIC:
```
/watch "video.mp4" → Analyze content
Extract → Frame analysis
Generate → Descriptions & captions
```

#### Commands:
```bash
/watch "example_video.mp4"
/watch "analyze structure"
/watch "extract key moments"
```

---

### 5️⃣ **Video-Editing-Skill** ⏳
**GitHub:** 6missedcalls/video-editing-skill  
**Type:** Claude Skill  
**Status:** Cloning

#### What it does:
- Professional video editing
- Format conversion (with FFmpeg)
- Transcription (with Whisper)
- Effect application

#### Requirements:
```bash
# Install dependencies
brew install ffmpeg
pip install openai-whisper

# Or on Windows
winget install FFmpeg
pip install openai-whisper
```

#### Installation:
```bash
# Copy to skills
cp -r /tmp/video-editing-skill ~/.claude/skills/

# Install dependencies
pip install -r video-editing-skill/requirements.txt
```

#### Use in MULTIC:
```
VideoEditorAgent → Main editing
Video-Editing-Skill → Advanced features
Scout Agent → Find + Download
Promotion → Format for platforms
```

#### Commands:
```bash
/video-editing-skill "Add transitions"
/video-editing-skill "Extract transcript"
/video-editing-skill "Convert to webm"
/video-editing-skill "Apply effects"
```

---

### 6️⃣ **Claude-YouTube** ⏳
**GitHub:** AgriciDaniel/claude-youtube  
**Type:** Claude Skill  
**Status:** Cloning

#### What it does:
- YouTube search integration
- Video analysis
- Transcript extraction
- Metadata retrieval
- Comment analysis

#### Installation:
```bash
# Copy to skills
cp -r /tmp/claude-youtube ~/.claude/skills/

# Activate
/claude-youtube "Search for viral videos"
```

#### Use in MULTIC:
```
Scout Agent → Find videos (primary)
Claude-YouTube → Enhanced search
Copywriter → Analyze transcripts
Email Agent → Extract quotes
```

#### Commands:
```bash
/claude-youtube "Search viral marketing videos"
/claude-youtube "Extract transcript"
/claude-youtube "Analyze comments sentiment"
/claude-youtube "Get video metadata"
```

---

## 🔄 Installation Flow

### Step 1: Check Clones (5 minutes)
```bash
ls /tmp/awesome-claude-skills/ | grep -E "video|content|competitive"
ls /tmp/claude-video/
ls /tmp/video-editing-skill/
ls /tmp/claude-youtube/
```

### Step 2: Copy to Skills Directory (Immediately)
```bash
# Copy from awesome-claude-skills
mkdir -p ~/.claude/skills/
cp -r /tmp/awesome-claude-skills/video-downloader ~/.claude/skills/
cp -r /tmp/awesome-claude-skills/content-research-writer ~/.claude/skills/
cp -r /tmp/awesome-claude-skills/competitive-ads-extractor ~/.claude/skills/

# Copy standalone skills
cp -r /tmp/claude-video ~/.claude/skills/
cp -r /tmp/video-editing-skill ~/.claude/skills/
cp -r /tmp/claude-youtube ~/.claude/skills/
```

### Step 3: Install Dependencies
```bash
# FFmpeg (for video-editing-skill)
brew install ffmpeg          # macOS
sudo apt-get install ffmpeg  # Linux
winget install FFmpeg        # Windows

# Whisper (for transcription)
pip install openai-whisper

# Any Python requirements
cd ~/.claude/skills/video-editing-skill
pip install -r requirements.txt
```

### Step 4: Test Each Skill
```bash
/video-downloader "Test"
/content-research-writer "Test"
/competitive-ads-extractor "Test"
/watch "sample.mp4"
/video-editing-skill "Test"
/claude-youtube "Test"
```

---

## 🎯 Integration with MULTIC Agents

### Scout Agent
```python
# Find videos
uses: claude-youtube (enhanced)
command: /claude-youtube "Search viral videos"
output: List of video URLs
```

### VideoEditorAgent
```python
# Download & edit
uses: video-downloader, video-editing-skill
command: /video-downloader "youtube.com/..."
effect: /video-editing-skill "Add effects"
```

### CopywriterAgent
```python
# Analyze & write
uses: claude-youtube, content-research-writer
command: /claude-youtube "Extract transcript"
research: /content-research-writer "Write variation"
```

### EmailCampaignAgent
```python
# Get quotes & social proof
uses: claude-youtube
command: /claude-youtube "Extract top comments"
use: In email sequences
```

### MasterAI Loop
```python
# Competitive analysis
uses: competitive-ads-extractor
command: /competitive-ads-extractor "Find top ads"
learn: Pattern analysis
adapt: Strategy adjustment
```

---

## 📊 Skill Capabilities Matrix

| Skill | Type | MULTIC Use | Status |
|-------|------|-----------|--------|
| video-downloader | Skill | Scout input | ⏳ |
| content-research-writer | Skill | Copywriter input | ⏳ |
| competitive-ads-extractor | Skill | MasterAI learning | ⏳ |
| claude-video | Plugin | Frame analysis | ⏳ |
| video-editing-skill | Skill | Advanced editing | ⏳ |
| claude-youtube | Skill | Video search | ⏳ |

---

## 🔐 Security & Dependencies

### Required Installations

**FFmpeg** (for video processing):
```bash
# Check if installed
ffmpeg -version

# Install if needed
brew install ffmpeg        # macOS
sudo apt-get install ffmpeg # Linux
choco install ffmpeg       # Windows via Chocolatey
winget install FFmpeg      # Windows via WinGet
```

**Whisper** (for transcription):
```bash
# Install
pip install openai-whisper

# Test
whisper --version
```

**YouTube-dl** (for downloads):
```bash
# Install
pip install yt-dlp

# Test
yt-dlp --version
```

### API Keys Needed
- ✅ None! All these skills work offline
- ✅ Claude API (already have)
- ✅ YouTube API (already configured in Scout)

---

## 🚀 Usage Examples

### Complete Workflow Example

```bash
# 1. Find videos
/claude-youtube "Search top viral marketing videos"

# 2. Download videos
/video-downloader "https://youtube.com/watch?v=xxx"

# 3. Analyze video
/watch "downloaded_video.mp4"

# 4. Extract transcript
/claude-youtube "Get transcript from URL"

# 5. Research & write
/content-research-writer "Write variation based on transcript"

# 6. Check competitors
/competitive-ads-extractor "Find similar ads"

# 7. Edit & format
/video-editing-skill "Add captions and effects"

# 8. Done! Ready to publish
```

---

## 📋 Next Steps

### Immediate (Today)
- [ ] Wait for repos to clone (10 minutes)
- [ ] Copy skills to ~/.claude/skills/
- [ ] Test each skill with simple command

### Tomorrow
- [ ] Install FFmpeg and Whisper
- [ ] Configure YouTube API (if needed)
- [ ] Integrate into Scout Agent
- [ ] Test complete workflow

### This Week
- [ ] Integrate video-downloader with Scout
- [ ] Add claude-youtube enhanced search
- [ ] Test video editing pipeline
- [ ] Analyze competitor ads

### Production Ready
- [ ] All 6 skills fully integrated
- [ ] Error handling complete
- [ ] Performance optimized
- [ ] Rate limiting configured

---

## ✨ What You Get

After installation:
- ✅ Professional video downloading
- ✅ YouTube integration enhanced
- ✅ Video editing capabilities
- ✅ Transcript extraction
- ✅ Competitive analysis
- ✅ Content research

**Total:** Complete video handling ecosystem for MULTIC v4.0

---

## 🔧 Troubleshooting

### Skill Not Found
```bash
# Verify installation
ls ~/.claude/skills/ | grep video

# Reinstall if needed
cp -r /tmp/awesome-claude-skills/video-downloader ~/.claude/skills/
```

### FFmpeg Not Found
```bash
# Check installation
which ffmpeg

# Reinstall
brew reinstall ffmpeg

# Or add to PATH
export PATH="/usr/local/bin:$PATH"
```

### Whisper Errors
```bash
# Reinstall
pip install --upgrade openai-whisper

# Test
whisper --version
```

### Clone Still Running?
```bash
# Check clone status
ps aux | grep git

# Manual clone if needed
cd /tmp
git clone https://github.com/ComposioHQ/awesome-claude-skills.git
```

---

## 📚 References

- **Composio Skills:** github.com/ComposioHQ/awesome-claude-skills
- **Claude Video:** github.com/bradautomates/claude-video
- **Video Editing:** github.com/6missedcalls/video-editing-skill
- **Claude YouTube:** github.com/AgriciDaniel/claude-youtube

---

**Status:** Installation guide ready, repos cloning  
**Next:** Copy skills when clones complete  
**Timeline:** All 6 skills functional by tomorrow
