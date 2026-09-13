# 🦸 Superpowers Plugin Installation Guide

**Date:** 2026-09-13  
**Status:** ✅ INSTALLED & VERIFIED  
**Version:** 6.3.0  
**Source:** https://github.com/obra/superpowers

---

## 📍 Installation Location

```
~/.claude/plugins/superpowers/
├── plugin.json              (Plugin metadata)
├── marketplace.json         (Marketplace entry)
├── hooks/                   (Session hooks)
├── .agents/                 (Agent definitions)
└── skills/                  (13 core skills)
    ├── brainstorming/
    ├── writing-plans/
    ├── executing-plans/
    ├── systematic-debugging/
    ├── test-driven-development/
    ├── dispatching-parallel-agents/
    ├── subagent-driven-development/
    ├── requesting-code-review/
    ├── receiving-code-review/
    ├── verification-before-completion/
    ├── finishing-a-development-branch/
    ├── using-git-worktrees/
    └── writing-skills/
```

---

## ✅ Installed Skills (13 Total)

### Core Development Workflow (3)
- **brainstorming** — Design phase, ask clarifying questions, propose approaches
- **writing-plans** — Create detailed implementation plans
- **executing-plans** — Execute plans step-by-step with verification

### Quality & Testing (3)
- **test-driven-development** — TDD workflow and test prioritization
- **systematic-debugging** — Structured debugging methodology
- **verification-before-completion** — Self-review before finishing tasks

### Collaboration & Code Review (3)
- **requesting-code-review** — Prepare and request reviews
- **receiving-code-review** — Handle feedback and iterations
- **finishing-a-development-branch** — Complete and merge work

### Advanced Techniques (4)
- **dispatching-parallel-agents** — Run multiple independent tasks
- **subagent-driven-development** — Orchestrate agent teams
- **using-git-worktrees** — Advanced git workflows
- **writing-skills** — Create custom skills

---

## 🎯 How These Skills Work

### Automatic Integration
Superpowers skills are **automatically triggered** based on context:

1. **When building something new:**
   - `brainstorming` activates → asks for spec
   - Waits for approval → `writing-plans` generates plan
   - After approval → `executing-plans` runs implementation

2. **When debugging:**
   - `systematic-debugging` guides investigation
   - Follows structured root-cause analysis

3. **When completing work:**
   - `verification-before-completion` self-reviews
   - Ensures quality gates passed

### Manual Triggers
You can also explicitly invoke:
```
/brainstorming "Build X feature"
/writing-plans "Implement Y based on spec"
/executing-plans "Follow the plan"
```

---

## 🔍 How to Verify Installation

### In Claude Code Terminal
```bash
# List installed Superpowers skills
ls ~/.claude/plugins/superpowers/skills/

# Check specific skill
cat ~/.claude/plugins/superpowers/skills/brainstorming/SKILL.md | head -20

# Verify plugin metadata
cat ~/.claude/plugins/superpowers/plugin.json
```

### In New Chat
The plugin is **automatically active** in any new session. You'll notice:
- Superpowers skills appear in available skills list
- When you describe building something, `brainstorming` activates automatically
- When you ask for help, contextual skills trigger

---

## 📋 Superpowers Methodology

The plugin implements the **Superpowers development methodology**:

```
1. BRAINSTORM (Design Phase)
   ↓
   Ask clarifying questions → Propose approaches → Get approval
   ↓

2. WRITE PLAN (Architecture Phase)
   ↓
   Break into tasks → Define success criteria → Set timeline
   ↓

3. EXECUTE PLAN (Implementation Phase)
   ↓
   Run subagents → Verify each task → Continue iterating
   ↓

4. VERIFY & COMPLETE (Quality Phase)
   ↓
   Self-review → Fix issues → Merge/deploy
```

---

## 🚀 Key Features

### Problem-First Approach
- Never jump to code without understanding the problem
- Design before implementation
- Specifications before coding

### TDD Integration
- Write tests first
- Red → Green → Refactor cycle
- Quality gates built-in

### Autonomous Development
- Subagents work independently
- Self-organizing task execution
- Minimal manual intervention needed

### Code Review Culture
- Request and receive reviews
- Structured feedback loops
- Collaborative improvement

---

## 💡 Using Superpowers with MULTIC

For your Phase 2 development:

### Scout Agent Implementation
```
/brainstorming "Scout Agent - discover viral videos"
→ Get spec
/writing-plans "Implement Scout Agent" 
→ Get plan
/executing-plans "Execute the plan"
→ Build with verification
```

### Copywriter Agent Implementation
```
/brainstorming "Copywriter Agent - content creation"
→ Define requirements
/writing-plans "Implement variations generator"
→ Break into tasks
/test-driven-development "Write tests first"
→ TDD approach
```

### Promotion Agent Implementation
```
/brainstorming "Promotion Agent - multi-platform publishing"
→ Design publishing flow
/writing-plans "Implement publishing pipeline"
→ Create tasks
/executing-plans "Build and verify"
→ Execute with quality gates
```

---

## 🔧 Plugin Configuration

The plugin activates automatically via:
- Session-start hooks (loaded when Claude Code starts)
- Context-aware skill triggers (activate when relevant)
- No manual configuration needed

---

## 📚 Superpowers Resources

- **Official GitHub:** https://github.com/obra/superpowers
- **Main Docs:** In the repository README.md
- **Skill Docs:** Each skill has SKILL.md with full documentation
- **Author:** Jesse Vincent (@obra)
- **License:** MIT

---

## ✨ Why Superpowers Matters for MULTIC

1. **Design-First:** Prevents building wrong thing
2. **Autonomous Work:** Agents execute long tasks independently
3. **Quality Built-In:** Testing and verification automatic
4. **Scalable:** Handles complex multi-phase projects
5. **Best Practices:** Implements proven engineering patterns

---

## 🎯 Next Steps

### In New Chat
1. Try `/brainstorming "Build Scout Agent"`
2. Watch it ask clarifying questions
3. Get approval on design
4. Use `/writing-plans` to break into tasks
5. Use `/executing-plans` to build autonomously

### Phase 2 Development
- Use brainstorming for each agent (Scout, Copywriter, Promotion)
- Use writing-plans to create implementation tasks
- Use executing-plans with subagent-driven-development for parallel work
- Use verification-before-completion to ensure quality

---

**Status:** ✅ **INSTALLED, VERIFIED, READY TO USE**

Superpowers are now active in Claude Code. Start building! 🚀

---

*Installation completed: 2026-09-13*  
*All 13 skills verified*  
*Ready for Phase 2 development*
