# 🦾 Awesome LLM Apps Skills Installation

**Date:** 2026-09-13  
**Status:** ✅ INSTALLED  
**Source:** https://github.com/Shubhamsaboo/awesome-llm-apps  
**Author:** Shubham Saboo

---

## 📍 Installation Location

```
.claude/skills/ (PROJECT-LOCAL)
├── advisor-orchestrator-worker/
└── self-improving-agent-skills/
```

**Note:** Repository doesn't contain `content-creator` and `fullstack-developer`. 
Those are already installed globally. These two skills are more aligned with MULTIC's multi-agent architecture.

---

## 🦾 Advisor Orchestrator Worker

**Purpose:** Orchestrate multiple models as a coordinated team for tasks too large for single model pass

### The Three-Tier Model Team

```
┌─────────────────────────────────────────┐
│ ADVISOR (Strongest reasoning model)     │
│ └─ Reviews plans, guides workers        │
├─────────────────────────────────────────┤
│ ORCHESTRATOR (Hot path: you are here)   │
│ ├─ Plans work                           │
│ ├─ Delegates to workers                 │
│ ├─ Verifies results                     │
│ └─ Synthesizes output                   │
├─────────────────────────────────────────┤
│ WORKERS (Cheapest that pass verification)
│ ├─ Stateless generation units           │
│ ├─ Parallel subtask execution           │
│ └─ Tools available (web search, files)  │
└─────────────────────────────────────────┘
```

### Core Philosophy

**Models are knobs.** The tiers are durable; model IDs swap freely.

**One rule survives every generation:**
- **Advisor:** Strongest reasoning model you can reach
- **Workers:** Cheapest that pass verification

### When to Use

✅ **Task too large for one model pass**
✅ **Parallel research across subtasks**
✅ **Generation across many items** (e.g., researching 12 competitors at once)
✅ **User asks to orchestrate multiple models**
✅ **User says "fan this out" or "too big for one model"**

❌ **NOT for single-file edits**
❌ **NOT for tasks one model handles in one pass**

### For MULTIC Multi-Agent System

#### Scout Agent - Parallel Video Discovery
```
Advisor: Review discovery strategy
Workers (parallel): Research 5+ video sources simultaneously
Orchestrator: Coordinate, verify patterns, synthesize findings
```

#### Copywriter Agent - Content Variation Generation
```
Advisor: Review content strategy
Workers (parallel): Generate variations for 5+ content themes
Orchestrator: Verify quality, synthesize best variations
```

#### Promotion Agent - Multi-Platform Publishing
```
Advisor: Review publishing strategy
Workers (parallel): Prepare posts for 4+ platforms concurrently
Orchestrator: Verify platform compliance, coordinate timing
```

#### Master MULTIC System - Agent Coordination
```
Advisor: Review system health
Workers (parallel): Run 3 agents simultaneously
Orchestrator: Verify results, synthesize metrics, adapt strategy
```

### Workflow Example

```
1. PLAN
   ├─ Break task into subtasks
   ├─ Identify parallel work
   └─ Define verification criteria

2. DELEGATE TO WORKERS (Parallel)
   ├─ Worker 1: Research competitor A
   ├─ Worker 2: Research competitor B
   ├─ Worker 3: Research competitor C
   └─ All running simultaneously

3. VERIFY
   ├─ Check quality of each result
   ├─ Verify against criteria
   └─ Request re-work if needed

4. SYNTHESIZE
   ├─ Combine results
   ├─ Cross-reference patterns
   ├─ Extract key insights
   └─ Present to advisor for review

5. ADVISOR REVIEW
   └─ Sign-off on output or request changes

6. OUTPUT
   └─ Deliver synthesized result
```

### Model Configuration

**Current Setup (July 2026):**
- **Advisor:** Claude (strongest model)
- **Workers:** Gemini 3.8 Flash (via `agy` CLI, cheap but capable)
- **Fallback:** Anthropic/Google APIs if CLI unavailable

**Models are Swappable:**
```
# Change advisor strength
ADVISOR_MODEL="claude-opus-5"  # vs claude-sonnet-5

# Change worker cost
WORKER_MODEL="gemini-2-flash"  # vs gemini-3.8-flash
```

### Key Features

✅ **Parallel execution** — multiple workers simultaneously  
✅ **Cost optimization** — cheap workers, strong advisor  
✅ **Verification gates** — check output before using  
✅ **Synthesis** — combine parallel results  
✅ **Fallback routing** — API fallback if CLI unavailable  
✅ **Shell-based** — bash snippets, portable  

---

## 🧠 Self-Improving Agent Skills

**Purpose:** Enable agents to learn from feedback and improve over time

### What It Does

Agents that:
✅ **Learn from feedback** — improve based on results  
✅ **Track performance metrics** — measure quality over time  
✅ **Extract patterns** — identify what works  
✅ **Optimize strategies** — adapt to changing conditions  
✅ **Build knowledge base** — accumulate learnings  

### Self-Improvement Loop

```
1. EXECUTE
   ├─ Agent completes task
   └─ Collect results & metrics

2. MEASURE
   ├─ Quality score
   ├─ Engagement rate
   ├─ Success criteria met?
   └─ Performance trend

3. ANALYZE
   ├─ What worked?
   ├─ What failed?
   ├─ Pattern extraction
   └─ Root cause analysis

4. LEARN
   ├─ Update strategy
   ├─ Refine prompts
   ├─ Add to knowledge base
   └─ Adjust weights/priorities

5. ADAPT
   └─ Next execution uses learned improvements
```

### For MULTIC Self-Learning

#### Scout Agent Learning
```
Execute: Discover videos
Measure: Engagement metrics (views, engagement ratio)
Learn: What patterns predict viral success?
Adapt: Refine discovery algorithm with learnings
```

#### Copywriter Agent Learning
```
Execute: Generate content variations
Measure: A/B test results (CTR, engagement)
Learn: What copy patterns perform best?
Adapt: Optimize variation generation templates
```

#### Promotion Agent Learning
```
Execute: Publish to platforms
Measure: Platform-specific metrics
Learn: Best times, formats, hashtags per platform?
Adapt: Optimize publishing strategy per platform
```

#### Master MULTIC Learning
```
Execute: Full pipeline (Scout → Copywriter → Promotion)
Measure: End-to-end metrics (ROI, growth)
Learn: Optimization opportunities across all agents?
Adapt: System-wide improvements, resource allocation
```

### Key Features

✅ **Feedback integration** — explicit improvement signals  
✅ **Metric tracking** — quantified performance  
✅ **Pattern extraction** — ML-like learning without ML  
✅ **Strategy adaptation** — prompt/algorithm refinement  
✅ **Knowledge accumulation** — persistent learnings  
✅ **Drift prevention** — maintain core objectives while learning  

---

## 📊 Integration with MULTIC Architecture

### Tier 1: Requirements & Discovery
- **discovery-interview** — Deep requirements gathering
- **content-creator** — Content strategy routing

### Tier 2: Planning & Design  
- **Superpowers:brainstorming** — Design phase
- **gstack:autoplan** — Phase breakdown
- **frontend-design** — Distinctive UI

### Tier 3: Orchestration & Execution
- **advisor-orchestrator-worker** ← Coordinates multi-agent work
- **Superpowers:executing-plans** — TDD execution
- **gstack:review** — Code quality

### Tier 4: Learning & Adaptation
- **self-improving-agent-skills** ← Learns from results
- **gstack:health** — Monitor metrics
- **gstack:retro** — Weekly analysis

### Full Phase 2A Workflow

```
1. /discovery-interview
   └─ Detailed Scout Agent spec

2. /advisor-orchestrator-worker
   ├─ Parallel: Design, Architecture, Planning
   └─ Sync: Verification gates

3. /executing-plans (with TDD)
   ├─ Build Scout Agent
   └─ Track performance metrics

4. /self-improving-agent-skills
   ├─ Analyze results
   ├─ Extract patterns
   └─ Adapt for next iteration

5. /gstack:ship
   └─ Production release
```

---

## 🎯 Usage Examples

### Scout Agent with Orchestrator

```
/advisor-orchestrator-worker "Scout for viral videos:
 Worker 1: Analyze YouTube Shorts in tech niche
 Worker 2: Analyze YouTube Shorts in gaming niche  
 Worker 3: Analyze YouTube Shorts in finance niche
 Advisor: Synthesize patterns, identify commonalities"

→ Parallel discovery across niches
→ Advisor reviews patterns
→ Synthesized insights
```

### Copywriter Agent with Self-Improvement

```
/self-improving-agent-skills "Learn from copywriting results:
 Last run: Generated 15 variations
 Metrics: A/B test results from platform
 Learn: Which copy patterns performed best?
 Adapt: Update templates for next generation"

→ Analyze past performance
→ Extract successful patterns
→ Improve generation prompts
→ Better variations next time
```

### Promotion Agent Multi-Platform

```
/advisor-orchestrator-worker "Publish to 4 platforms:
 Worker 1: Prepare YouTube post
 Worker 2: Prepare Telegram post
 Worker 3: Prepare Twitter post
 Worker 4: Prepare Instagram post
 Advisor: Verify platform compliance
 Orchestrator: Coordinate timing"

→ Parallel platform preparation
→ Quality verification per platform
→ Synchronized publishing
```

---

## 🔧 Technical Details

### Advisor-Orchestrator-Worker

**Requirements:**
- bash shell
- jq (JSON processor)
- Claude CLI or API key
- Gemini/Anthropic API keys (for workers/advisor)

**Execution Model:**
- Worker invocation: `agy` CLI (Antigravity) or Gemini API
- Advisor invocation: `claude` CLI or Anthropic API
- All coordination: bash scripting

**Best For:**
- Parallel information gathering
- Multi-source analysis
- Large-scale content generation
- Distributed task execution

### Self-Improving-Agent-Skills

**Requirements:**
- Metric collection system
- Feedback mechanism
- Knowledge storage
- Prompt/strategy versioning

**Execution Model:**
- Capture execution results
- Measure against criteria
- Analyze patterns
- Update strategies
- Track improvements over time

**Best For:**
- Iterative refinement
- Learning-driven optimization
- Pattern-based adaptation
- Long-running agent improvement

---

## 📊 Project Skills Summary

### Now Installed (4 Project-Local Skills)

```
.claude/skills/
├── discovery-interview
│   └─ Transform vague ideas → detailed specs (7-phase interview)
│
├── content-creator  
│   └─ Content strategy routing (multi-content framework)
│
├── advisor-orchestrator-worker
│   └─ Coordinate multi-model teams (Advisor + Workers)
│
└── self-improving-agent-skills
    └─ Learn from feedback (self-optimization loops)
```

### Global Skills (251+)

```
Superpowers (13):     brainstorming, planning, TDD, debugging, etc.
gstack (55):          autoplan, design-review, qa, ship, health, etc.
awesome-skills (31):  mcp-builder, lead-research, twitter-optimizer
Anthropic (4):        frontend-design, skill-creator, discovery, banana
Others (147+):        video, content, marketing, technical tools
```

---

## 🚀 Phase 2A Execution Plan

### Step 1: Discover (discovery-interview)
```
/discovery-interview "Scout Agent detailed specification"
→ 10-15 questions across 7 phases
→ Complete specification
```

### Step 2: Orchestrate Design (advisor-orchestrator-worker)
```
/advisor-orchestrator-worker "Scout Agent design:
 Worker 1: Dashboard UI mockup
 Worker 2: API specification
 Worker 3: Database schema
 Advisor: Review for coherence"
```

### Step 3: Plan & Build
```
/writing-plans "Scout Agent implementation"
/executing-plans "Build with TDD"
```

### Step 4: Learn & Improve
```
/self-improving-agent-skills "Scout Agent first deployment:
 Metrics: 10 videos discovered
 Results: 5 reached 100K views
 Learn: What made those 5 successful?
 Adapt: Refine discovery algorithm"
```

### Step 5: Deploy
```
/gstack:ship "Scout Agent production release"
```

---

## ✅ Installation Verification

```bash
# Check installation
ls .claude/skills/

# Should show:
# advisor-orchestrator-worker/
# content-creator/
# discovery-interview/
# self-improving-agent-skills/

# Ready to use
/advisor-orchestrator-worker "Your task description"
/self-improving-agent-skills "Your learning task"
```

---

## 📖 References

**Advisor-Orchestrator-Worker:**
- Use for tasks requiring parallel execution
- Cost optimization through tier-based model selection
- Works with any model pair (swap freely)

**Self-Improving-Agent-Skills:**
- Track metrics over time
- Extract patterns from results
- Adapt strategies based on learnings
- Build persistent knowledge base

---

**Status:** ✅ **INSTALLED & READY FOR USE**

Enables multi-agent orchestration and self-learning capabilities for MULTIC Phase 2.

---

*Installed: 2026-09-13*  
*Source: github.com/Shubhamsaboo/awesome-llm-apps*  
*Author: Shubham Saboo*  
*Location: .claude/skills/ (PROJECT-LOCAL)*
