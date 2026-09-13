# 🍌 Banana Claude Skill - Installation & Usage

**Date:** 2026-09-13  
**Status:** ✅ INSTALLED  
**Version:** 3.0.0  
**Author:** AgriciDaniel  
**Source:** https://github.com/AgriciDaniel/banana-claude  
**Provider:** Google Gemini API (requires billing-enabled project)

---

## 📍 Installation Location

```
~/.claude/skills/banana/
├── SKILL.md (20K, 334 lines)
├── scripts/ (Python tools for generation/editing/review)
└── references/ (Documentation, models, cost tracking)
```

**Installation Date:** 2026-09-13  
**Installation Method:** Direct from source repository  
**Requirements:** Python 3.11+, Google AI Studio API key (billing-enabled)

---

## 🎯 What Banana Claude Does

**Create, edit, compare, and review Gemini images from Claude Code**

Turn plain-language creative requests into:
✅ **Planned image workflows** (offline first, no immediate cost)  
✅ **Exact prompts** (reviewable before execution)  
✅ **Model selection** (Nano Banana 2 Lite, 2, Pro)  
✅ **Cost estimates** (transparency before paid request)  
✅ **Generated images** (with metadata tracking)  
✅ **Visual review** (inspect pixels, approve before shipping)

---

## 🔄 The Workflow (5 Steps)

### 1. **Ask**
Describe the outcome in natural language:
```
/banana generate an urban 16:9 GitHub hero with clean left-side copy space
/banana edit make the background warmer without changing the subject
/banana portfolio compare three approaches to this product photo
```

### 2. **Plan**
Banana Claude builds visual brief offline:
- Interprets the request
- Chooses model route (Lite/2/Pro)
- Generates exact prompt
- Calculates cost estimate
- **No API call yet**

### 3. **Review**
Inspect the plan before paying:
- Read the exact prompt
- Check model choice
- Review cost estimate
- Verify output destination
- Verify data privacy settings

### 4. **Approve**
One short-lived approval authorizes one provider attempt:
- Approval valid for 30 minutes
- Single-use capability (consumed on execution)
- Changed plan = new approval needed
- No auto-retry (failures require re-approval)

### 5. **Create & Check**
Image is generated and saved:
- Inspect actual pixels
- Review metadata sidecar
- Visual review status tracked
- Fix, regenerate, or ship

---

## 🎨 What You Can Make

### Generate
- Campaign visuals & covers
- Product scenes & renders
- Diagrams & concepts
- Social media assets
- Character designs
- Conceptual artwork

### Edit
- Make one clear change
- Protect identity & geometry
- Preserve brand details
- Iterate on stored sessions

### Continue
- Iterate with Flash or Pro sessions
- Attach previous result as reference
- Build on existing work

### Compare
- Test up to 3 prompts
- Compare across 3 model routes
- Create bounded portfolio
- Select best result

### Review
- Check copy & crop
- Verify composition
- Ensure consistency
- Detect artifacts
- Clear rights & provenance
- Verify photographic accuracy

### Typeset
- Add approved copy
- Apply fonts
- Place logos
- Add raster art locally
- Perfect text placement

---

## 🤖 Model Routes

Banana routes across **Google's current Gemini image models**:

### Nano Banana 2 Lite
- **Speed:** Fastest
- **Quality:** Good
- **Cost:** Lowest
- **Use:** Quick iterations, drafts, tests

### Nano Banana 2
- **Speed:** Fast
- **Quality:** Better
- **Cost:** Medium
- **Use:** Production work, balanced

### Nano Banana Pro
- **Speed:** Slower
- **Quality:** Best
- **Cost:** Highest
- **Use:** Final output, complex requests

**Current models documented in:**
```
~/.claude/skills/banana/references/gemini-models.md
```

---

## 🔐 Security & Privacy (Non-Negotiable)

### API Key Management
✅ Plugin stores as sensitive Claude Code configuration  
✅ Standalone reads only from GEMINI_API_KEY env var  
❌ Never prints, logs, or exposes API key  
❌ Never includes in command lines or URLs

### Cost & Transparency
✅ Planning is offline (no API calls)  
✅ Plan shown before every paid request  
✅ Cost estimates provided upfront  
✅ Cost records omit raw prompts by default  
❌ No hidden charges

### Approval System
✅ Explicit approval required before execution  
✅ Approval is single-use capability  
✅ Expires after 30 minutes  
✅ Consumed before API call

### Assets & Rights
✅ Uploaded assets require explicit authority statement  
✅ Cannot infer rights from file possession  
✅ Unresolved authority blocks planning  
✅ Never invent rights or usage claims

### Visual Review
✅ Save/export not creative completion  
✅ Every image inspected before shipping  
✅ Visual review status tracked  
✅ Probabilistic output not guaranteed

---

## 📋 Complete Workflow Example

### Scenario: Create Product Hero Image

```
User: /banana generate a clean product hero for a meditation app
      16:9 aspect, white space on left, person meditating center-right

Step 1: PLAN (Offline)
  ✓ Interprets request
  ✓ Selects Nano Banana 2 (balanced)
  ✓ Generates prompt (multi-step refinement)
  ✓ Calculates cost: ~$0.03 (estimate)
  ✓ Shows approval request

Step 2: REVIEW
  User reads:
    Prompt: "Serene meditation scene, zen aesthetic, person in lotus..."
    Model: Nano Banana 2
    Aspect: 16:9
    Cost: ~$0.03
    Output: ~/banana-outputs/meditation-app-hero.png

Step 3: APPROVE
  User: "Looks good, approve"
  → Creates single-use approval token
  → Valid for 30 min
  → Ready to execute

Step 4: EXECUTE
  /banana execute approval-token-xyz
  → Calls Google Gemini API
  → Generates image
  → Saves with metadata
  → Shows result

Step 5: REVIEW
  User inspects pixels:
    ✓ Composition good
    ✓ White space on left ✓
    ✓ Person placement ✓
    ✗ Colors too warm
    
  Decision: Regenerate

Step 6: EDIT
  /banana edit make colors cooler and more zen
  (New plan → new approval → new execution)

Step 7: APPROVE & EXECUTE
  (Same workflow for regeneration)

Step 8: SHIP
  All visual reviews complete
  Metadata tracked
  Ready for production
```

---

## 💰 Cost Tracking

Banana includes comprehensive cost tracking:

```
~/.claude/skills/banana/scripts/cost_tracker.py
```

Features:
- ✅ Track per-request costs
- ✅ Aggregate spending by model
- ✅ Monthly/daily cost summaries
- ✅ Privacy-conscious logging
- ✅ Omit raw prompts by default

**Cost command:**
```
/banana cost [--model MODEL] [--period DAYS]
```

---

## 🛠️ Python Tools & Scripts

### banana_core.py (186K)
- Core engine for planning & execution
- Prompt optimization
- Model routing logic
- Gemini API client

### generate.py
- Image generation workflow
- Aspect ratio handling
- Quality parameters

### edit.py
- Image editing logic
- Iterative refinement
- Reference preservation

### portfolio.py
- Multi-model comparison
- A/B/C testing
- Result portfolio

### typeset.py
- Text overlay
- Font handling
- Logo placement
- Local post-processing

### presets.py (131K)
- Pre-defined workflows
- Common use cases
- Quick templates

### cost_tracker.py (120K)
- Cost tracking & reporting
- Budget monitoring
- Historical analysis

### approval_store.py (23K)
- Single-use approval tokens
- Token expiration (30 min)
- Audit trail

---

## 📚 Reference Documentation

### gemini-models.md (18K)
- Current model capabilities
- Pricing per model
- Speed/quality tradeoffs
- Deprecated compatibility routes

### prompt-engineering.md (17K)
- Effective prompt strategies
- Model-specific tips
- Common patterns
- Anti-patterns to avoid

### cost-tracking.md (13K)
- Budget management
- Cost estimation accuracy
- Spending patterns
- Optimization tips

### post-processing.md (18K)
- Local image adjustments
- Crop & composition
- Color correction
- Format conversion

### review-and-recovery.md (8K)
- Visual review process
- Common issues
- Recovery strategies
- When to regenerate

### mcp-tools.md (22K)
- MCP server integration
- Tool definitions
- Parameters & options
- Advanced workflows

### presets.md (9K)
- Pre-defined templates
- Custom preset creation
- Common use cases
- Workflow shortcuts

---

## 🎯 Usage for MULTIC Phase 2

### Scout Agent Dashboard Visuals
```
/banana generate YouTube thumbnail concepts for viral video topics
  - Multiple design approaches
  - Test audience appeal
  - A/B testing with portfolio
  - Generate from analysis data
```

### Copywriter Agent Visual Assets
```
/banana generate social media graphics for content variations
  - Adapt to platform aspect ratios
  - A/B test visual styles
  - Quick iteration cycles
  - Brand consistency
```

### Promotion Agent Graphics
```
/banana generate platform-specific cover images
  - YouTube thumbnails
  - Telegram channel art
  - Platform-optimized dimensions
  - Branded templates
```

### System Dashboard Visuals
```
/banana generate MULTIC agent illustrations
  - Character designs for agents
  - System architecture diagrams
  - Real-time metric visualizations
  - Status indicator graphics
```

---

## ⚠️ Important Limitations & Guarantees

### Gemini Output is Probabilistic
❌ Cannot guarantee consistency across runs  
❌ Cannot guarantee correct spelling  
❌ Cannot guarantee proper geometry  
❌ Cannot guarantee policy compliance  
❌ Cannot guarantee rights clearance  

These remain **review conditions**, not marketing claims.

### Cost Estimates are Nominal
- Estimates shown in planning
- Actual costs may vary
- Model response time affects cost
- Complex prompts cost more
- Never auto-retry without approval

### Visual Review is Required
- Every image must be inspected
- Save/export ≠ completion
- Track visual_review_status
- Keep as `needs_review` until inspected
- Only mark `approved` after human review

---

## 🔧 Configuration

### Plugin Installation (Recommended)
Requires Claude Code 2.1.199+

```bash
/plugin marketplace add AgriciDaniel/banana-claude
/plugin install banana-claude@banana-claude-marketplace
/plugin enable banana-claude@banana-claude-marketplace
/reload-plugins
```

Then set Gemini API key in Claude Code plugin settings.

### Standalone Installation
Can be used without plugin:

```bash
cd /tmp/banana-claude
./install.sh
```

Set env var:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 📊 Setup Validation

Banana includes validation tools:

```bash
python3 ~/.claude/skills/banana/scripts/validate_setup.py
```

Checks:
✅ Python version
✅ Dependencies
✅ API key configuration
✅ Gemini API connectivity
✅ Billing status

---

## 📖 Learn More

### Official Documentation
- https://github.com/AgriciDaniel/banana-claude
- https://github.com/AgriciDaniel/banana-claude/blob/main/SECURITY.md
- https://github.com/AgriciDaniel/banana-claude/blob/main/CONTRIBUTING.md

### Key Files
```
~/.claude/skills/banana/references/
  ├─ gemini-models.md
  ├─ prompt-engineering.md
  ├─ cost-tracking.md
  ├─ post-processing.md
  ├─ review-and-recovery.md
  └─ mcp-tools.md
```

---

## ✅ Installation Verification

```bash
# Check installation
ls ~/.claude/skills/banana/

# Should show:
# ✅ SKILL.md (20K)
# ✅ scripts/ (Python tools)
# ✅ references/ (Documentation)

# Validate setup
python3 ~/.claude/skills/banana/scripts/validate_setup.py
```

---

## 🚀 Quick Start Example

### Step 1: Generate an Image
```
/banana generate a modern dashboard interface for data analytics
       16:9 aspect, dark theme, colorful charts, minimal UI clutter
```

### Step 2: Review the Plan
Banana shows:
- Exact prompt
- Model selected
- Cost estimate
- Output location

### Step 3: Approve
```
/banana approve <approval-token>
```

### Step 4: Review Result
Inspect the generated image in output folder

### Step 5: Iterate (if needed)
```
/banana edit adjust the colors to be warmer and more vibrant
/banana continue iterate on this design with different layouts
```

---

## 📊 Skill Statistics

```
Name:              banana
Version:           3.0.0
Author:            AgriciDaniel
Provider:          Google Gemini API
Installation:      ~/.claude/skills/banana/
Source:            github.com/AgriciDaniel/banana-claude
License:           MIT
Requirements:      Python 3.11+, Billing-enabled Google AI key
Size:              ~600K (scripts + references)
```

---

## 🔐 Security Checklist

- ✅ API key stored as sensitive Claude Code config
- ✅ Never logged or exposed
- ✅ Approval required before execution
- ✅ Cost estimates shown upfront
- ✅ Visual review required before shipping
- ✅ Metadata tracking for audit
- ✅ Rights authority required for uploads

---

**Status:** ✅ **INSTALLED & READY TO USE**

Enables distinctive, production-grade image generation for MULTIC agents and dashboards. Requires Google AI Studio Gemini API key (billing-enabled project).

---

*Installed: 2026-09-13*  
*Author: AgriciDaniel*  
*Version: 3.0.0*  
*Provider: Google Gemini API*  
*Philosophy: Plan first, review always, approve explicitly*
