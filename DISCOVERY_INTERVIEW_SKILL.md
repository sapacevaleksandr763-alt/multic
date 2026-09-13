# 🎯 Discovery Interview Skill - Installation & Usage

**Date:** 2026-09-13  
**Status:** ✅ INSTALLED  
**Version:** Latest (Continuous-Claude v3)  
**Source:** https://github.com/parcadei/Continuous-Claude-v3

---

## 📍 Installation Location

```
~/.claude/skills/discovery-interview/
└── SKILL.md (14.9 KB)
```

**Installation Scope:** Global (available in all projects)

---

## 🎯 What Discovery Interview Does

This skill transforms **vague ideas into detailed, implementable specifications** through deep, iterative interviews.

### Core Philosophy
- **Don't ask obvious questions** — dig deeper
- **Don't accept surface answers** — challenge assumptions
- **Don't assume knowledge** — educate when needed

### What It Does
1. **Deeply understand** what user actually wants (not what they say)
2. **Detect knowledge gaps** and educate when needed
3. **Surface hidden assumptions** and tradeoffs
4. **Research when uncertain** — spawn research agents
5. **Write detailed spec** only when complete understanding achieved

---

## 🔄 Interview Process (7 Phases)

### **Phase 1: Initial Orientation (2-3 questions)**
Understand the shape of the idea:
- "In one sentence, what problem are you solving?"
- "Who will use this?"
- "New thing or improving existing?"

Determines PROJECT TYPE:
- Backend service/API
- Frontend/Web app
- CLI tool
- Mobile app
- Full-stack app
- Script/Automation
- Library/SDK

### **Phase 2-6: Category-by-Category Deep Dive**

For each category (2-4 questions):

#### **Category A: Problem & Goals**
- Current pain point? How do people solve it today?
- What does success look like?
- Who are the stakeholders?
- What if this doesn't get built?

#### **Category B: User Experience & Journey**
- User opens it first time — what do they see?
- What's the ONE core action?
- What errors can happen?
- How technical are users?

#### **Category C: Data & State**
- What information needs storing?
- Where does data come from/go?
- Who owns data? Privacy concerns?
- What happens to existing data?

#### **Category D: Technical Architecture**
- What's the tech stack?
- How does it scale?
- What integrations needed?
- How does it handle errors?

#### **Category E: Success & Iteration**
- How do you measure success?
- What's MVP vs. nice-to-have?
- How will you iterate?
- What's the timeline?

#### **Category F: Risks & Constraints**
- Budget constraints?
- Technical risks?
- Regulatory/compliance issues?
- Resource limitations?

### **Phase 7: Implementation Handoff**

After spec is written, ask about next steps:
- Start implementation now
- Review spec first
- Plan implementation
- Done for now

---

## 🚀 Auto-Activation Triggers

Discovery Interview **automatically activates** when you:

### Building Something New
- "I want to build a [product]"
- "Help me design a [system]"
- "Let's create a [feature]"

### Requirements Gathering
- "I have an idea but not sure how to execute"
- "Help me spec out [project]"
- "What should this look like?"

### Vague Requirements
- User can't clearly articulate what they want
- Multiple conflicting ideas mentioned
- "I'm not sure what the MVP should be"

### Technical Design
- Need to design API / database schema
- Architecture decision needed
- "What should the user flow be?"

---

## 💡 Key Features

### Interview Approach
- **Minimum 10-15 questions** for real projects
- **At least 2 questions per category**
- **At least 1 research loop**
- **Completeness check before spec writing**
- **Summarizes understanding before finalizing**

### Handles Different User Types
- **Technical users** — less explanation, focus on tradeoffs
- **Non-technical users** — more education, use analogies
- **Users in a hurry** — prioritize core requirements, note risks

### Research Integration
- Spawns research agents for uncertainty
- WebSearch when needed
- Can benchmark against successful examples

### Drift Prevention
When implementing spec:
```
Say: "implement the <spec-name> spec"

This will:
1. Activate spec context
2. Inject requirements before each edit
3. Checkpoint every 5 edits for alignment
4. Validate acceptance criteria before finishing
```

---

## 🎯 Usage for MULTIC Phase 2

### Scout Agent Specification
```
/discovery-interview "Help me spec Scout Agent for YouTube video discovery"

Will cover:
- Problem: Find viral video patterns
- Users: Automated system (no human input needed)
- UX: Monitor dashboard showing discovered videos
- Data: Video metadata, trends, engagement patterns
- Tech: YouTube API, analysis engine, learning loop
- Success: Find 5+ viral videos/week with >2x engagement
- MVP: Discovery only, no analysis yet
```

### Copywriter Agent Specification
```
/discovery-interview "Spec out Copywriter Agent for content variation"

Will cover:
- Problem: Generate multiple variations of content
- Users: Internal to promotion system
- UX: Takes input content, outputs variations
- Data: Competitor patterns, brand guidelines, metrics
- Tech: Claude API, prompt optimization, A/B testing
- Success: 15+ high-quality variations in <2 hours
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
- Success: 15 videos published in 4 platforms (60 posts)
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
- Success: All system status visible at a glance
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

Before finalizing spec, the skill ensures:
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

## 📊 Integration with Other Skills

Works with:
- **Superpowers:brainstorming** — complementary, different approach
- **writing-plans** — takes discovery output as input
- **executing-plans** — uses spec for drift prevention
- **code-reviewer** — validates implementation against spec

---

**Status:** ✅ **INSTALLED & READY TO USE**

Perfect for transforming MULTIC Phase 2 vague requirements into detailed, implementable specifications! 🎯

---

*Installation completed: 2026-09-13*  
*Global availability: All future projects*  
*Perfect for: Agent specs, system design, feature requirements*
