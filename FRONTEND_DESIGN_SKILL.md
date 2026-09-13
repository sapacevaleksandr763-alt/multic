# 🎨 Frontend Design Skill - Installation & Usage

**Date:** 2026-09-13  
**Status:** ✅ INSTALLED (Fresh from GitHub)  
**Version:** 1.1.0  
**Authors:** Prithvi Rajasekaran & Alexander Bricken (Anthropic)  
**Source:** https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design

---

## 📍 Installation Location

```
~/.claude/skills/frontend-design/
├── SKILL.md (12K, 71 lines)
└── LICENSE.txt (10K)
```

**Installation Date:** 2026-09-13  
**Installation Method:** Direct from official Anthropic claude-code repository

---

## 🎯 What Frontend Design Does

This skill is the **design lead at a design studio** known for distinctive visual identities. It ensures:

✅ **Not AI slop** — avoids generic defaults  
✅ **Distinctive identity** — specific to the brief, not templated  
✅ **Bold aesthetic choices** — opinionated typography, color, layout  
✅ **Subject-matter grounded** — design emerges from the industry/domain  
✅ **Production-ready quality** — responsive, accessible, harmonious

---

## 🎨 Design Philosophy

### Core Principle
> "Give every client a distinct visual identity that is not mistaken for anyone else's. The client pays for a distinctive point of view: make deliberate, opinionated choices that are specific to this brief."

### Key Attributes
1. **No templates** — each design is unique to its subject matter
2. **Grounded in reality** — industry, materials, vernacular inform the design
3. **Bold typography** — typeface choice carries personality
4. **Intentional color** — deliberate palette, not defaults
5. **Restraint** — spend boldness in one place, keep rest quiet
6. **Self-critique** — review against brief, not generic defaults

---

## 📋 Design Process (2-Pass Approach)

### Pass 1: Plan
Create compact token system:
```
Color:   4-6 named hex values (core palette)
Type:    Typefaces and their roles
Layout:  Alignment, concept, ASCII wireframes
Principles: High-level guidance for uniqueness
```

### Pass 2: Review & Build
1. Review plan against brief
2. Check if it reads as "this specific brief" vs "generic default"
3. Revise any generic parts
4. Build only after confirming uniqueness

---

## 🚫 What NOT to Do (Common AI Defaults)

### Color Defaults
- ❌ Warm cream background (#F4F1EA) + warm clay accent (#D97757)
- ❌ Near-black + bright acid-green or vermilion
- ❌ Monochrome + single bright accent

### Typography Defaults
- ❌ Accent single word/phrase (italic/bold/color)
- ❌ ALL CAPS labels
- ❌ Unnecessary typographic labels above content
- ❌ Different typeface for display vs body (unless clearly distinct)

### Layout Defaults
- ❌ Identical rounded-corner cards (SaaS kit)
- ❌ Same soft shadow (rgba(0,0,0,.1)) under everything
- ❌ Gradient washes as pure decoration
- ❌ Hairline rules, zero border-radius (broadsheet style)
- ❌ Tracked-out ALL-CAPS eyebrows above headings

### Animation Defaults
- ❌ Fade-and-slide-up on every section
- ❌ Hover transitions on every card
- ❌ Scattered, unmotivated motion

---

## ✅ Design Guidelines

### Typography
- **Line length:** <80 characters (serif can be longer)
- **Type scale:** Follow Elements of Typographic Style defaults
- **Weights/widths:** Intentional, not accidental
- **Headline:** Active part of design, not neutral vehicle

### Structure
- **Outlines/borders/dividers:** Encode information, not decoration
- **Numbered markers:** Only if content is truly sequential
- **Labels:** Minimize, only what's needed

### Motion
- **Deliberate only** — draws attention or shows change
- **Single orchestrated moment** — one page-load sequence
- **Response motion:** Answers user's action (opening, expanding)

### Copy
- **Subject matter specific** — not generic placeholder text
- **Active voice** — "Save changes" not "Submit"
- **Conversational tone** — plain verbs, sentence case, no filler
- **Context-aware** — matched to brand and audience

### Accessibility & Quality Floor
- ✅ Responsive down to mobile
- ✅ Visible keyboard focus
- ✅ Reduced motion respected
- ✅ Visually accessible
- ✅ Harmonious color palettes

---

## 🔄 Auto-Activation Triggers

Frontend Design **automatically activates** when you:

### Building UI/Frontend
- "Create a dashboard for..."
- "Build a landing page for..."
- "Design a settings panel..."
- "Design a [component] for..."

### Redesigning Existing
- "Redesign this interface..."
- "Make this look [aesthetic]..."
- "Improve the visual design..."

### Any UI-Related Request
- "Make a beautiful [page/app/component]"
- "Professional UI for..."
- "Distinctive design for..."

---

## 💡 Key Insights from Skill

### Ground Design in Subject Matter
```
Example:
  Brief: "Dashboard for music streaming"
  ✅ Research music industry aesthetics
  ✅ Use color/typography specific to music
  ✅ Hero: album art, waveforms, or live preview
  ✅ NOT generic dashboard template

Example:
  Brief: "Dashboard for financial analysts"
  ✅ Clean, high-density information
  ✅ Numeric confidence, data hierarchy
  ✅ Reduced decoration, maximum signal
  ✅ NOT creative startup aesthetic
```

### Typography as Personality
```
✅ Choose typefaces deliberately
✅ Use 1-2 families max (make clearly distinct if 2)
✅ Follow type scale intentionally
✅ Set headline type as visual element
✅ NOT default serif/sans combination
```

### The Chanel Principle
> "Before leaving the house, look in the mirror and remove one accessory."

Apply to design:
- Build to quality floor without announcing it
- Critique as you go
- Remove decoration that doesn't serve brief
- Spend boldness in ONE place
- Keep everything around it quiet & disciplined

### CSS Specificity Gotchas
⚠️ Watch for conflicting selectors:
```css
.section { padding: 2rem; }
.cta { padding: 1rem; }  /* May cancel out .section */
```

---

## 🎯 Usage for MULTIC Phase 2

### Scout Agent Dashboard
```
/frontend-design "Design Scout Agent discovery dashboard"

Should:
  ✅ Ground in video/streaming industry
  ✅ Hero: trending video preview or analytics
  ✅ Color palette: vibrant (video energy), not corporate
  ✅ Typography: bold display for key metrics
  ✅ Motion: subtle video playback indicators
  ✅ NOT: generic SaaS dashboard cards
```

### Copywriter Agent UI
```
/frontend-design "Creative tool interface for content generation"

Should:
  ✅ Ground in creative studio/publishing
  ✅ Hero: content variations or A/B testing results
  ✅ Color palette: creative (bold, distinctive)
  ✅ Typography: character-driven, personality-filled
  ✅ Motion: reveal variations, show A/B results
  ✅ NOT: form-heavy spreadsheet-like UI
```

### Promotion Agent Dashboard
```
/frontend-design "Multi-platform publishing control panel"

Should:
  ✅ Ground in broadcast/publication
  ✅ Hero: real-time publishing status or metrics
  ✅ Color palette: professional, platform-aware
  ✅ Typography: clear hierarchy for multi-platform data
  ✅ Motion: status updates, publish confirmations
  ✅ NOT: generic admin panel
```

### Master MULTIC Dashboard
```
/frontend-design "System-wide metrics & agent health dashboard"

Should:
  ✅ Ground in autonomous systems/robotics aesthetic
  ✅ Hero: real-time agent status or key metric
  ✅ Color palette: cohesive, reflects agents' personalities
  ✅ Typography: clear data hierarchy, metrics prominent
  ✅ Motion: smooth agent status transitions
  ✅ NOT: template-based monitoring dashboard
```

---

## 📖 Learn More

**Frontend Aesthetics Cookbook:**
https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb

This notebook covers:
- How to prompt for distinctive frontend design
- Avoiding AI defaults and slop
- Subject-matter grounding
- Typography and color theory
- Production-ready implementation

---

## 📊 Integration with MULTIC Team

### In Superpowers Workflow
```
1. /brainstorming "Design [feature]"
   → General requirements

2. /frontend-design (auto-activates)
   → Gets distinctive visual identity
   
3. /design-review (gstack skill)
   → Gets feedback on distinctive choices
   
4. /executing-plans
   → Implements with design guidance
```

### With gstack
```
/design-review "Dashboard UI"
  + 
/frontend-design (background context)
  = Distinctive, reviewed UI design
```

---

## ✅ Installation Verification

```bash
# Check installation
ls ~/.claude/skills/frontend-design/

# Should show:
# ✅ SKILL.md (12K)
# ✅ LICENSE.txt (10K)

# Verify in Claude Code
# Use the skill tool to invoke frontend-design skill
```

---

## 🚀 Quick Start

### For Scout Agent Dashboard
```
1. Prompt to Claude:
   "Design Scout Agent dashboard with distinctive aesthetic"

2. Claude automatically:
   ✅ Activates frontend-design skill
   ✅ Creates 2-pass design plan
   ✅ Grounds in video streaming industry
   ✅ Produces distinctive color/typography
   ✅ Implements production code

3. Review & iterate:
   /design-review for feedback
   Revise based on distinctive feedback
```

---

## 📊 Skill Statistics

```
Name:              frontend-design
Version:           1.1.0
Author:            Prithvi Rajasekaran & Alexander Bricken (Anthropic)
Size:              12K (71 lines)
Installation:      ~/.claude/skills/frontend-design/
Source:            github.com/anthropics/claude-code
License:           Included (LICENSE.txt)
Auto-activation:   Any UI/frontend/design request
Integration:       Works with Superpowers, gstack, other frameworks
```

---

## 🎨 Philosophy Summary

### What Makes It Work
1. **Subject-matter grounding** — Design emerges from domain
2. **Deliberate choices** — Everything is intentional, not default
3. **Distinctive aesthetic** — Unique to brief, not templated
4. **Production quality** — Accessible, responsive, harmonious
5. **Self-critique** — Reviews against brief, removes defaults
6. **Restraint** — Bold in one place, quiet elsewhere

### What It Avoids
- Generic AI aesthetics and templates
- Unmotivated decoration and effects
- Default color/typography combinations
- Copy that feels templated
- Accessible-by-accident designs

### The Result
**Professional-grade UI that looks intentional, distinctive, and appropriate to its subject matter — not like it was generated by an AI.**

---

**Status:** ✅ **INSTALLED & READY TO USE**

Perfect for creating distinctive, production-ready interfaces for all MULTIC agents and dashboards.

---

*Installed: 2026-09-13 (Fresh from Anthropic source)*  
*Authors: Prithvi Rajasekaran & Alexander Bricken*  
*Official Anthropic Plugin for Claude Code*  
*Philosophy: Distinctive visual identity, no AI slop*
