# 🦸 Superpowers v6.3.0 - Global Installation

**Date:** 2026-09-13  
**Status:** ✅ INSTALLED GLOBALLY  
**Version:** 6.3.0  
**Author:** Jesse Vincent  
**Source:** https://github.com/obra/superpowers  
**Location:** `~/.claude/plugins/superpowers/` (GLOBAL)

---

## 📍 Installation Location

```
~/.claude/plugins/superpowers/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .agents/
│   └── skills/ (13 skills)
├── .codex-plugin/
├── .cursor-plugin/
├── docs/
├── README.md
└── RELEASE-NOTES.md
```

**Scope:** GLOBAL (available in all projects)  
**Installation Date:** 2026-09-13

---

## 🎯 What is Superpowers?

**Complete software development methodology for coding agents.**

Built on composable skills and proven techniques that make agents:
✅ Ask the right questions before coding  
✅ Design specs before implementation  
✅ Plan before building  
✅ Test as they code (TDD)  
✅ Collaborate effectively  
✅ Debug systematically  
✅ Deploy confidently

---

## 🔄 The Superpowers Workflow

### Phase 1: Brainstorming (Design)
```
/brainstorming "Build [feature/system]"

Agent:
  ✓ Asks clarifying questions
  ✓ Proposes 2-3 approaches
  ✓ Shows design spec
  ✓ Gets approval before proceeding
```

### Phase 2: Writing Plans (Planning)
```
/writing-plans "Implement [spec-name]"

Agent:
  ✓ Breaks into implementation tasks
  ✓ Defines success criteria
  ✓ Creates timeline
  ✓ Shows dependency graph
```

### Phase 3: Executing Plans (Implementation)
```
/executing-plans "Execute [plan-name]"

Agent:
  ✓ Builds with TDD (red → green → refactor)
  ✓ Tests as it codes
  ✓ Validates against spec
  ✓ Checkpoints every 5 edits
```

### Phase 4: Code Quality (Review)
```
/requesting-code-review "Review my implementation"

Agent:
  ✓ Checks code quality
  ✓ Finds edge cases
  ✓ Tests coverage
  ✓ Performance issues
  ✓ Security concerns
```

### Phase 5: Deployment (Finishing)
```
/finishing-a-development-branch "Ship this branch"

Agent:
  ✓ Final testing
  ✓ Documentation
  ✓ Merge strategy
  ✓ Deployment validation
```

---

## 🛠️ 13 Core Skills

### Design & Planning
- **brainstorming** — Turn ideas into specs through questions
- **writing-plans** — Break spec into implementation plan
- **spec** — Technical specification with gates

### Execution & Quality
- **executing-plans** — Autonomous TDD-driven building
- **test-driven-development** — Red → Green → Refactor cycle
- **systematic-debugging** — Root cause analysis
- **requesting-code-review** — Prepare for review
- **receiving-code-review** — Handle feedback

### Collaboration & Workflows
- **dispatching-parallel-agents** — Parallel subtask execution
- **subagent-driven-development** — Agent team orchestration
- **using-git-worktrees** — Advanced git workflows
- **verification-before-completion** — Quality gates before finish
- **finishing-a-development-branch** — Merge & deploy

### Extension
- **writing-skills** — Create custom skills

---

## 💡 Core Philosophy

### Red → Green → Refactor
TDD-driven development:
1. **Red:** Write test that fails
2. **Green:** Write minimal code to pass
3. **Refactor:** Improve without breaking test

### YAGNI (You Aren't Gonna Need It)
- Build only what's needed
- Avoid premature optimization
- Remove code that isn't used

### DRY (Don't Repeat Yourself)
- Eliminate duplication
- Extract common patterns
- Reuse tested code

### Fail Fast, Learn Quick
- Small iterations reveal problems early
- Regular checkpoints prevent divergence
- Testing catches issues before they compound

---

## 🚀 For MULTIC Phase 2A: Scout Agent

### Complete Workflow

```
1. BRAINSTORM
   /brainstorming "Scout Agent for YouTube discovery"
   
   Agent asks:
   - What problem are we solving?
   - Who will use this?
   - How will we measure success?
   - What are the risks?
   
   Outputs: Design specification

2. WRITE PLAN
   /writing-plans "Implement Scout Agent"
   
   Agent creates:
   - Task breakdown
   - Success criteria
   - Timeline
   - Dependencies
   
   Outputs: Implementation plan

3. EXECUTE
   /executing-plans "Build Scout Agent with TDD"
   
   Agent:
   - Writes tests first
   - Implements code
   - Validates against spec
   - Checkpoints every 5 edits
   
   Outputs: Working Scout Agent

4. REQUEST REVIEW
   /requesting-code-review "Review Scout Agent"
   
   Agent:
   - Analyzes code quality
   - Checks test coverage
   - Identifies issues
   - Suggests improvements
   
   Outputs: Review findings

5. VERIFY
   /verification-before-completion "Final checks"
   
   Agent:
   - Confirms against spec
   - Tests edge cases
   - Performance checks
   - Documentation review
   
   Outputs: Ready/not ready

6. FINISH
   /finishing-a-development-branch "Ship Scout Agent"
   
   Agent:
   - Final validation
   - Merge strategy
   - Deployment plan
   - Rollback procedure
   
   Outputs: Production ready
```

---

## 📊 Available Commands (Global)

All commands available in ANY project with `/ ` prefix:

### Design Phase
```
/brainstorming "Your idea description"
→ Questions → Proposals → Design spec → Approval
```

### Planning Phase
```
/writing-plans "Your implementation spec"
→ Task breakdown → Timeline → Dependencies → Approval
```

### Execution Phase
```
/executing-plans "Your plan name"
→ TDD red/green/refactor → Tests → Checkpoints → Validation
```

### Quality Assurance
```
/test-driven-development "Your code"
→ Test-first development → Coverage → Quality gates

/systematic-debugging "Your bug description"
→ Root cause analysis → Reproduction steps → Solution

/requesting-code-review "Your code"
→ Quality assessment → Issue detection → Suggestions
```

### Collaboration
```
/dispatching-parallel-agents "Your large task"
→ Parallel subtask execution → Synthesis

/subagent-driven-development "Your complex task"
→ Agent team orchestration → Result coordination
```

### Workflows
```
/using-git-worktrees "Your workflow"
→ Manage multiple worktrees safely

/verification-before-completion "Your code"
→ Quality gates → Readiness check

/finishing-a-development-branch "Your branch"
→ Merge strategy → Deployment → Validation
```

### Extension
```
/writing-skills "Your skill idea"
→ Create custom skills for specific tasks
```

---

## 🎯 Integration with MULTIC Ecosystem

### With Project Skills
```
Project Skills (.claude/skills/):
├── discovery-interview → generates requirements
├── content-creator → creates content
├── fullstack-developer → designs architecture
├── advisor-orchestrator-worker → coordinates work
├── self-improving-agent-skills → learns from results
└── frontend-design → designs UI

Superpowers (Global):
├── /brainstorming → Design phase
├── /writing-plans → Planning phase
├── /executing-plans → TDD implementation
├── /test-driven-development → Quality assurance
├── /requesting-code-review → Code review
└── /finishing-a-development-branch → Deployment
```

### Phase 2 Workflow Integration

```
1. /discovery-interview (project-local skill)
   ↓
2. /brainstorming (Superpowers global)
   ↓
3. /fullstack-developer (project-local skill)
   ↓
4. /writing-plans (Superpowers global)
   ↓
5. /executing-plans (Superpowers + TDD)
   ↓
6. /test-driven-development (Superpowers)
   ↓
7. /requesting-code-review (Superpowers)
   ↓
8. /verification-before-completion (Superpowers)
   ↓
9. /finishing-a-development-branch (Superpowers)
   ↓
10. /self-improving-agent-skills (project-local)
    ↓
    Learning loop → Next iteration
```

---

## ✅ Installation Verification

```bash
# Check installation
ls ~/.claude/plugins/superpowers/

# Should show:
# ✅ .claude-plugin/ (plugin configuration)
# ✅ .agents/ (skill definitions)
# ✅ docs/ (documentation)
# ✅ README.md
# ✅ RELEASE-NOTES.md

# Verify availability in any project
cd /any/project
/brainstorming "Test idea"
# Should work in ANY project
```

---

## 🎯 Quick Start

### For Scout Agent (Phase 2A)

**Step 1: Brainstorm Design**
```
/brainstorming "Scout Agent for YouTube discovery"
```

**Step 2: Get Specification from Project Skill**
```
/discovery-interview "Detailed Scout Agent requirements"
```

**Step 3: Plan Implementation**
```
/writing-plans "Implement Scout Agent from discovery spec"
```

**Step 4: Build with TDD**
```
/executing-plans "Build Scout Agent"
```

**Step 5: Ensure Quality**
```
/test-driven-development "Scout Agent testing"
/systematic-debugging "Any issues found"
/requesting-code-review "Scout Agent code review"
```

**Step 6: Ship**
```
/verification-before-completion "Final Scout Agent checks"
/finishing-a-development-branch "Ship Scout Agent"
```

---

## 📈 Success Metrics with Superpowers

### Productivity
- **Specification clarity** — Fewer implementation surprises
- **Development speed** — TDD catches issues early
- **Code quality** — Structured approach improves consistency
- **Review efficiency** — Preparation prevents back-and-forth

### Quality
- **Test coverage** — TDD ensures >80% coverage
- **Bug detection** — Early in cycle, before production
- **Design validation** — Approved before implementation
- **Deployment confidence** — Verified before shipping

---

## 🔄 The Complete Workflow Cycle

```
PLAN → DESIGN → ARCHITECT → BUILD → TEST → REVIEW → VERIFY → SHIP → LEARN → ADAPT

With Superpowers:

Plan
 ↓ /writing-plans
Design
 ↓ /brainstorming
Architect
 ↓ /fullstack-developer
Build
 ↓ /executing-plans (with TDD)
Test
 ↓ /test-driven-development
Review
 ↓ /requesting-code-review
Verify
 ↓ /verification-before-completion
Ship
 ↓ /finishing-a-development-branch
Learn
 ↓ /self-improving-agent-skills
Adapt
 ↓ Back to Plan...
```

---

## 📚 Resources

- **README:** https://github.com/obra/superpowers/blob/main/README.md
- **Release Notes:** 100K+ history of updates
- **Philosophy:** Built on proven development practices
- **Community:** Open source, MIT licensed

---

## 📊 Global Integration Status

```
✅ Superpowers v6.3.0
   Location: ~/.claude/plugins/superpowers/ (GLOBAL)
   Skills: 13 core + extensible
   Available: All projects, all contexts
   Commands: /brainstorming, /writing-plans, /executing-plans, etc.

✅ Project Skills (6)
   Location: .claude/skills/ (PROJECT-LOCAL)
   For: MULTIC-specific requirements

✅ Global Skills (251+)
   Location: ~/.claude/skills/ (GLOBAL)
   From: Superpowers, gstack, awesome-skills, etc.

✅ PHASE 2 READY
   All tools integrated
   Complete workflow available
   Quality gates in place
```

---

**Status:** ✅ **SUPERPOWERS GLOBALLY INSTALLED & READY**

Available in every project. Use `/brainstorming`, `/writing-plans`, `/executing-plans` across all contexts.

---

*Installed: 2026-09-13*  
*Version: 6.3.0*  
*Author: Jesse Vincent*  
*License: MIT*  
*Scope: Global (all projects)*
