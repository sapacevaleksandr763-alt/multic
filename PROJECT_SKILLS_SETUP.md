# 🚀 Project-Local Skills Setup

**Date:** 2026-09-13  
**Status:** ✅ CONFIGURED  
**Location:** `.claude/skills/` (project-local)

---

## 📍 What's Installed

### `.claude/skills/discovery-interview/`
**Skill:** discovery-interview (14.9K)  
**Author:** parcadei (Continuous-Claude-v3)  
**Model:** claude-opus-4-5-20251101  
**Purpose:** Transform vague ideas into detailed specifications

```
.claude/skills/
├── discovery-interview/
│   └── SKILL.md (14.9K, 443 lines)
└── content-creator/
    └── SKILL.md (already installed)
```

---

## 🎯 Discovery Interview Skill

### What It Does

Deep interview process to transform vague ideas into detailed, implementable specifications. Works with both technical and non-technical users.

**Core Philosophy:**
> "Don't ask obvious questions. Don't accept surface answers. Don't assume knowledge."

### The Interview Process (7 Phases)

#### Phase 1: Initial Orientation (2-3 questions)
Understand the shape of the idea:
- "In one sentence, what problem are you solving?"
- "Who will use this?"
- "New thing or improving existing?"

**Determines PROJECT TYPE:**
- Backend service/API
- Frontend/Web app
- CLI tool
- Mobile app
- Full-stack app
- Script/Automation
- Library/SDK

#### Phases 2-6: Category-by-Category Deep Dive

For each category (2-4 questions):

**Category A: Problem & Goals**
- Current pain point? How do people solve today?
- What does success look like?
- Who are stakeholders?
- What if this doesn't get built?

**Category B: User Experience & Journey**
- User opens it first time → what do they see?
- What's the ONE core action?
- What errors can happen?
- How technical are users?

**Category C: Data & State**
- What information needs storing?
- Where does data come from/go?
- Who owns data? Privacy concerns?
- What happens to existing data?

**Category D: Technical Landscape**
- What existing systems integrate?
- Technology constraints?
- Deployment environment?
- Team's technical expertise?

**Category E: Scale & Performance**
- How many users/requests?
- Acceptable response times?
- Handling traffic spikes?
- Read-heavy, write-heavy, or balanced?

**Category F: Risks & Constraints**
- Budget constraints?
- Technical risks?
- Regulatory/compliance issues?
- Resource limitations?

#### Phase 7: Implementation Handoff

After spec written:
- Start implementation now?
- Review spec first?
- Plan implementation?
- Done for now?

### Key Features

**Interview Approach:**
- Minimum 10-15 questions for real projects
- At least 2 questions per category
- At least 1 research loop
- Completeness check before spec writing
- Summarizes understanding before finalizing

**Handles Different User Types:**
- Technical users → less explanation, focus on tradeoffs
- Non-technical users → more education, use analogies
- Users in a hurry → prioritize core requirements, note risks

**Research Integration:**
- Spawns research agents for uncertainty
- WebSearch when needed
- Benchmarks against successful examples

---

## 🎯 Usage for MULTIC Phase 2

### Scout Agent Specification
```
/discovery-interview "Help me spec Scout Agent for YouTube video discovery"

Will cover:
- Problem: Find viral video patterns
- Users: Automated system (no human input)
- UX: Monitor dashboard showing discovered videos
- Data: Video metadata, trends, engagement patterns
- Tech: YouTube API, analysis engine, learning loop
- Scale: Find 5+ viral videos/week with >2x engagement
- MVP: Discovery only, no analysis yet
```

### Copywriter Agent Specification
```
/discovery-interview "Spec out Copywriter Agent for content variation"

Will cover:
- Problem: Generate multiple content variations
- Users: Internal to promotion system
- UX: Takes input content, outputs variations
- Data: Competitor patterns, brand guidelines, metrics
- Tech: Claude API, prompt optimization, A/B testing
- Scale: 15+ high-quality variations in <2 hours
- MVP: Basic variations, no A/B testing yet
```

### Promotion Agent Specification
```
/discovery-interview "Spec Promotion Agent for multi-platform publishing"

Will cover:
- Problem: Publish video to multiple platforms
- Users: Internal automation
- UX: Dashboard showing publish queue, metrics
- Data: Video files, captions, platform-specific formats
- Tech: Platform APIs, scheduling, analytics
- Scale: 15 videos published in 4 platforms (60 posts)
- MVP: YouTube + Telegram, manual scheduling first
```

### Master Dashboard Design
```
/discovery-interview "Help me design MULTIC master dashboard"

Will cover:
- Problem: Monitor autonomous system health
- Users: Human operator checking status
- UX: Real-time metrics, agent status, alerts
- Data: System logs, agent metrics, performance data
- Tech: Real-time updates, beautiful visualization
- Scale: All system status visible at glance
- MVP: Basic metrics, no deep analytics yet
```

---

## 🔍 Knowledge Gap Signals

The skill detects and addresses:
- User can't articulate problem clearly
- Describes solution instead of problem
- Hasn't thought through user flow
- Doesn't understand data implications
- Overlooking technical complexity
- No clear success metrics

When detected → offers research or education

---

## 📋 Completeness Check

Before finalizing spec, skill ensures:
- ✅ Problem clearly defined
- ✅ User journey mapped
- ✅ Data model understood
- ✅ Technical architecture sketched
- ✅ Success metrics defined
- ✅ Risks identified
- ✅ MVP clearly separated from nice-to-have

---

## 🚀 Next Steps with Spec

After discovery is complete:

1. **Implement the spec** → Say "implement the [spec-name] spec"
2. **Plan implementation** → Spawn plan-agent with spec context
3. **Review spec** → Read and refine before building
4. **Save for later** → Return when ready to build

---

## 📊 Integration with Other Frameworks

Works perfectly with:
- **Superpowers:brainstorming** — complementary, different approach
- **gstack:autoplan** — takes discovery output as input
- **gstack:spec** — technical spec writing with gates
- **Superpowers:writing-plans** — creates plan from discovery spec
- **Superpowers:executing-plans** — uses spec for drift prevention
- **gstack:design-review** — validates design against spec

---

## 🎯 Project-Local vs Global Skills

### discovery-interview (Project-Local)
```
Location: .claude/skills/discovery-interview/
Scope: This project only
Use: /discovery-interview [request]
Purpose: Deep requirement gathering for MULTIC agents
```

### Global Skills (Global)
```
Location: ~/.claude/skills/
Scope: All projects
Use: /skill-name [request]
Examples: /frontend-design, /banana, /gstack-autoplan
```

---

## ✅ Current Project Setup

```
MULTIC Project Structure:
├── .claude/skills/
│   ├── discovery-interview/    (PROJECT-LOCAL)
│   └── content-creator/        (PROJECT-LOCAL)
│
├── ~/.claude/skills/
│   ├── frontend-design/        (GLOBAL)
│   ├── banana/                 (GLOBAL)
│   ├── gstack/                 (GLOBAL - 55 skills)
│   ├── awesome-skills/         (GLOBAL - 31 skills)
│   └── [other global skills]
│
└── Global Plugins
    ├── Superpowers v6.3.0      (13 methodology skills)
    └── Frontend Design v1.1.0  (distinctive UI)
```

---

## 🔄 Recommended Workflow for Phase 2A

### 1. Discover Requirements
```
/discovery-interview "Detailed Scout Agent specification for YouTube discovery"
→ In-depth interview
→ Detailed specification saved
```

### 2. Design Phase
```
/brainstorming "Scout Agent dashboard design based on discovery spec"
→ Visual direction proposed
→ Design review feedback
```

### 3. Architecture Review
```
/plan-eng-review "Scout Agent architecture"
→ Engineering approval
```

### 4. Planning
```
/writing-plans "Scout Agent implementation plan"
→ Detailed tasks, timeline, dependencies
```

### 5. Execution
```
/executing-plans "Scout Agent implementation with TDD"
→ Build with tests, verify against spec
```

### 6. Review & QA
```
/review "Scout Agent code quality"
/qa "Scout Agent testing"
→ Quality gates pass
```

### 7. Deployment
```
/ship "Scout Agent production release"
→ Full deployment pipeline
```

---

## 📊 Skill Statistics

```
Skill Name:        discovery-interview
Version:           Continuous-Claude v3
Author:            parcadei
Model:             claude-opus-4-5-20251101
Location:          .claude/skills/discovery-interview/
Size:              14.9K (443 lines)
Installation:      2026-09-13
Scope:             Project-local (MULTIC only)
User-Invocable:    Yes
```

---

## 🎯 Why This Matters for MULTIC

### Scout Agent Specification Example

Without discovery-interview:
```
"Build a YouTube discovery system"
→ Ambiguous, missing details
→ Implementation surprises
→ Rework required
```

With discovery-interview:
```
/discovery-interview "YouTube discovery system spec"
→ Deep interview (10-15 questions)
→ 7-phase process covering all categories
→ Complete specification
→ Clear implementation path
→ No surprises
```

---

## ✅ Status

**Project-Local Setup:** ✅ COMPLETE
- discovery-interview skill installed
- Ready for Phase 2A requirements gathering
- Integrated with global frameworks (Superpowers, gstack, etc.)
- Prepared for Scout Agent specification

**Next Action:** 
```
/discovery-interview "Detailed Scout Agent specification"
```

---

**Status:** ✅ **PROJECT SKILLS READY**

Project-local skills configured, global skills operational, frameworks integrated.

Ready for Phase 2A: Scout Agent discovery & specification phase.

---

*Setup Date: 2026-09-13*  
*Skill Source: github.com/parcadei/Continuous-Claude-v3*  
*Integration: MULTIC Phase 2 workflow*
