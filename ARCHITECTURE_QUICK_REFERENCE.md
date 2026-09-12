# MULTIC Architecture Quick Reference
## Implementation Checklist & Decision Framework

**Document Purpose:** Quick-lookup guide for architecture decisions without reading full analysis

---

## Quick Decision Tree

### Q: "Should we use CrewAI, LangGraph, or AutoGen?"
**Answer:** Use **CrewAI + LangGraph Hybrid**
- CrewAI for agent orchestration (intuitive, low friction)
- LangGraph for state management (persistence, observability)
- Both have proven production credentials

### Q: "How should agents communicate?"
**Answer:** Hub-and-spoke with Manager orchestrator
```
❌ Wrong: Agent A → Agent B → Agent C (peer-to-peer)
✓ Right: Agent A → Manager → Agent B → Manager → Agent C
```

### Q: "What data structure for agent state?"
**Answer:** Always Pydantic models, never dictionaries
```python
# ❌ Wrong
state = {"topic": "AI", "platforms": ["twitter"]}

# ✓ Right
class ContentRequest(BaseModel):
    topic: str
    platforms: List[str]
    urgency: str = "normal"
```

### Q: "When can we remove human review gates?"
**Answer:** Never, but you can reduce frequency:
```
Month 0-2: 100% human review (confidence: 0-50%)
Month 2-4: 50% auto-publish (confidence: 50-80%)
Month 4-6: 80% auto-publish (confidence: 80-95%)
Month 6+: 95% auto-publish (confidence: 95%+)
Always: Maintain human override capability
```

### Q: "How many turns should an agent take?"
**Answer:** `max_iter=3-5` (hard limit)
```python
# ❌ Wrong: No limit
agent = Agent(model="claude-3-5-sonnet")

# ✓ Right: Hard limits
agent = Agent(
    model="claude-3-5-sonnet",
    max_iter=5,  # Hard stop after 5 iterations
    max_tokens=2000  # Hard stop on tokens
)
```

### Q: "How do we handle async content publishing?"
**Answer:** Event-driven with Celery queues
```
Request → Return 202 (accepted) immediately
   ↓
Queue task in Celery
   ↓
Agent processes asynchronously
   ↓
Webhook callback when complete
   ↓
Client polls for status (don't block)
```

### Q: "How do we prevent duplicate posts?"
**Answer:** Request ID as deduplication key
```python
class ContentRequest(BaseModel):
    request_id: str  # UUID, must be unique
    topic: str
    platforms: List[str]

# Check before processing
if cache.exists(f"request:{request_id}"):
    return already_processed_result
```

---

## Pattern Library

### Pattern #1: Gradual Autonomy
```
Input Request
    ↓
Process with agent
    ↓
Calculate confidence score
    ↓
if confidence < 50%:
    → Human review required
elif confidence < 80%:
    → Auto-publish, human review after
elif confidence >= 80%:
    → Auto-publish, no review
    ↓
Always: Maintain override capability
```

### Pattern #2: Step-Based Execution (Zapier Model)
```
Agent 1 (Input) → Result 1
    ↓
Agent 2 (Process) → Result 2
    ↓
Agent 3 (Output) → Final Result
    
❌ Don't: Chain agents together (coupling)
✓ Do: Each agent is independent, orchestrator coordinates
```

### Pattern #3: Dual Memory
```
SHORT-TERM (Session):
    - Conversation within current workflow
    - Agent state for specific task
    - Tool outputs and decisions
    - Duration: ~24 hours

LONG-TERM (Cross-session):
    - User preferences and guidelines
    - Performance metrics per agent
    - Historical content archive
    - Brand voice specifications
    - Duration: Indefinite until purged
```

### Pattern #4: Error Handling
```
Try execution
    ↓
Catch specific errors
    ↓
If recoverable:
    → Implement retry with exponential backoff (2s, 4s, 8s, 16s, stop)
    ↓
If not recoverable:
    → Log full state
    → Route to human review
    → Create incident ticket
    ↓
Always: Log complete state at each step (don't just log exceptions)
```

### Pattern #5: Observability
```
Every significant action must log:
1. Timestamp (when)
2. Agent ID (who)
3. Task ID (what)
4. Input state (before)
5. Output state (after)
6. Duration (how long)
7. Cost (tokens used)
8. Confidence (internal score)

Structure:
{
    "timestamp": "2026-09-12T10:30:00Z",
    "agent_id": "writer_technical",
    "task_id": "task_123_abc",
    "step": "content_generation",
    "input": {...},
    "output": {...},
    "duration_ms": 2340,
    "tokens_used": 1240,
    "confidence_score": 0.87,
    "status": "success"
}
```

---

## Technology Stack (Recommended)

```
User Request
    ↓
    FastAPI (HTTP endpoint, handle webhooks)
    ↓
    CrewAI (orchestrate agents, define roles)
    ↓
    LangGraph (manage state, persistence)
    ↓
    PostgreSQL (store conversations, audit trail)
    ↓
    Redis (cache, message broker, Celery backend)
    ↓
    Celery (async task queue)
    ↓
    Social Platform APIs (Twitter, LinkedIn, etc.)
    ↓
    OpenTelemetry (instrumentation)
    ↓
    Prometheus (metrics)
    ↓
    ELK Stack (logs, dashboards)
```

**Rationale:**
- FastAPI: Modern async, auto-documentation, WebSocket support
- CrewAI: Intuitive, proven, minimal boilerplate
- LangGraph: State management, persistence, observability
- PostgreSQL: Reliable, scalable, ACID compliance
- Redis: Proven cache + message broker (dual use)
- Celery: Standard distributed task queue
- OpenTelemetry: Standard observability (not vendor lock-in)
- Prometheus: Battle-tested metrics (works with OT)
- ELK: Standard log aggregation (works with OT)

---

## Critical Metrics to Track

| Metric | Target | Frequency |
|--------|--------|-----------|
| **Agent Success Rate** | >95% | Per task |
| **Token Efficiency** | <3,000/workflow | Per execution |
| **Confidence Score** | >0.80 for auto-publish | Per piece of content |
| **Latency (sync)** | <2s for webhook response | Per request |
| **Latency (async)** | <30s to queue task | Per request |
| **Review Rate** | <5% (after month 4) | Per day |
| **Error Rate** | <0.5% | Per 1000 tasks |
| **Cost per Content** | <$0.15 (LLM cost) | Per piece |
| **Memory Usage** | <500MB per agent | Per process |
| **Queue Depth** | <100 tasks | Real-time |

---

## Configuration Templates

### Agent Definition Template (CrewAI)
```python
from crewai import Agent

researcher = Agent(
    role="Researcher",
    goal="Research trending topics and competitor content",
    backstory="You are an experienced market researcher...",
    tools=[web_search_tool, database_search_tool],
    max_iter=3,  # CRITICAL: Hard limit
    memory=True,  # Use unified memory (2025+)
    verbose=True,  # For debugging
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging, on-brand content",
    backstory="You are a professional copywriter...",
    tools=[formatting_tool, spell_check_tool],
    max_iter=5,
    memory=True,
)

editor = Agent(
    role="Quality Editor",
    goal="Review content before publication",
    backstory="You are a meticulous editor...",
    tools=[quality_check_tool, compliance_check_tool],
    max_iter=2,
    memory=True,
)
```

### Task Definition Template (CrewAI)
```python
from crewai import Task

research_task = Task(
    description="Research the topic: {topic}",
    expected_output="A detailed research report",
    agent=researcher,
    tools=[web_search_tool],
)

writing_task = Task(
    description="Write engaging content based on research",
    expected_output="A polished content piece",
    agent=writer,
    context=[research_task],  # Depends on research_task
    tools=[formatting_tool],
)

review_task = Task(
    description="Review content for quality and brand fit",
    expected_output="Approved or flagged for revisions",
    agent=editor,
    context=[writing_task],
    tools=[quality_check_tool],
)
```

### State Model Template (Pydantic + LangGraph)
```python
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ContentRequest(BaseModel):
    request_id: str  # UUID for idempotency
    topic: str
    platforms: List[str]  # ['twitter', 'linkedin', etc.]
    tone: str = "professional"
    urgency: str = "normal"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentOutput(BaseModel):
    agent_id: str
    step: str
    content: Optional[str]
    score: float
    tokens_used: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class WorkflowState(BaseModel):
    request_id: str
    status: str  # 'pending', 'in_progress', 'review', 'published', 'failed'
    steps: List[AgentOutput] = []
    final_content: Optional[Dict[str, str]] = None  # {platform: content}
    confidence_score: float = 0.0
    requires_human_review: bool = True
    approved_by: Optional[str] = None
    published_at: Optional[datetime] = None
    error: Optional[str] = None
```

### Observability Configuration (OpenTelemetry)
```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader

# Setup tracing
otlp_exporter = OTLPSpanExporter(
    endpoint="localhost:4317",  # Or your OTel collector
)
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(otlp_exporter))

# Setup metrics
prometheus_reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[prometheus_reader]))

# In your agent execution
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

with tracer.start_as_current_span("agent_execution") as span:
    span.set_attribute("agent_id", agent.id)
    span.set_attribute("task_id", task.id)
    # ... execution code ...
    span.set_attribute("tokens_used", 1240)
    span.set_attribute("status", "success")
```

---

## Deployment Checklist

### Pre-Production
- [ ] All state objects use Pydantic models
- [ ] All agents have `max_iter` and `max_tokens` set
- [ ] Audit logging implemented and tested
- [ ] Request ID deduplication working
- [ ] Human review gates in place (100%)
- [ ] Error handlers for all agent branches
- [ ] Monitoring and observability wired up
- [ ] Rate limiting configured on APIs
- [ ] Database backups automated
- [ ] Cache (Redis) failover tested

### Launch
- [ ] Load test with 10x expected traffic
- [ ] Smoke test all agent workflows
- [ ] Verify audit trails are complete
- [ ] Check token costs (should be <$0.15/content)
- [ ] Monitor first 100 requests for errors
- [ ] Verify human review queue works
- [ ] Test override mechanism (humans can stop publishing)
- [ ] Rollback plan documented

### Post-Launch (Week 1)
- [ ] Monitor error rates (should be <0.5%)
- [ ] Review confidence score distribution
- [ ] Analyze token usage per agent
- [ ] Identify slow agents (optimize if >10s)
- [ ] Review human review feedback
- [ ] Tune agent prompts based on mistakes
- [ ] Plan gradual autonomy increase (if ready)

---

## Red Flags: Stop and Review

### 🚩 Agent token usage > 5,000/execution
**Action:** Reduce max_iter, simplify tools, shorter prompts

### 🚩 Confidence score < 0.65
**Action:** Don't increase autonomy, review agent training

### 🚩 Error rate > 1%
**Action:** Investigate error patterns, improve error handling

### 🚩 Queue depth > 500 tasks
**Action:** Add Celery workers (scale horizontally)

### 🚩 Human review rate still > 20% (after month 4)
**Action:** Improve agent prompts, review rejection patterns

### 🚩 Latency > 5s for sync operations
**Action:** Profile code, optimize database queries

### 🚩 Cost per content > $0.25
**Action:** Reduce model complexity, use faster models

### 🚩 Missing audit trail for any operation
**Action:** Implement comprehensive logging immediately

---

## Troubleshooting Guide

### Problem: Agent keeps calling same tool repeatedly
**Solution:** Implement iteration counter
```python
if agent_state['iterations'] > max_iter:
    raise MaxIterationsExceeded()
```

### Problem: State inconsistency between agents
**Solution:** Use Pydantic validation on state mutations
```python
state = WorkflowState(**state_dict)  # Validates schema
state.status = "new_status"  # Type-safe
```

### Problem: Forgotten user preferences on new session
**Solution:** Load from LangGraph Store on session start
```python
user_prefs = store.get(f"user/{user_id}/preferences")
state.tone = user_prefs.get("tone", "default")
```

### Problem: Duplicate content published
**Solution:** Check request ID in cache before processing
```python
if cache.get(f"processed:{request_id}"):
    return cached_result
# ... process ...
cache.set(f"processed:{request_id}", result, ttl=3600)
```

### Problem: Agent takes too long (>10s)
**Solution:** Use async/parallel execution (LangGraph)
```python
# Parallel execution
results = await asyncio.gather(
    agent_a.run_async(state),
    agent_b.run_async(state),
    agent_c.run_async(state),
)
```

---

## Version Control & Documentation

### Per-Agent Versioning
```
agents/
├── writer_v1/
│   ├── prompt.md
│   ├── tools.yaml
│   └── README.md
├── writer_v2/  # Improved version
│   ├── prompt.md (updated)
│   ├── tools.yaml (updated)
│   └── CHANGELOG.md
└── writer_v3/  # Current
    ├── prompt.md
    ├── tools.yaml
    └── CHANGELOG.md
```

### Workflow Versioning
```
workflows/
├── linkedin_article_v1/
│   ├── agents.yaml
│   ├── tasks.yaml
│   └── CHANGELOG.md
├── linkedin_article_v2/  # Used in production (Aug 2026)
│   ├── agents.yaml
│   ├── tasks.yaml
│   └── CHANGELOG.md
└── linkedin_article_v3/  # Testing new agents
    ├── agents.yaml
    ├── tasks.yaml
    └── CHANGELOG.md
```

---

## Cost Management

### Per-Agent Cost Targets
```
Scout Agent (research):         $0.03 (400 tokens)
Writer Agent (content):         $0.05 (800 tokens)
Editor Agent (review):          $0.02 (400 tokens)
Publisher Agent (distribution): $0.01 (200 tokens)
────────────────────────────────────────────
TOTAL per content:            ~$0.11
Budget/day (100 contents):      ~$11
Budget/month (3000 contents):   ~$330
```

### Cost Tracking Query
```sql
SELECT
    agent_id,
    COUNT(*) as executions,
    SUM(tokens_used) as total_tokens,
    AVG(tokens_used) as avg_tokens,
    SUM(tokens_used) * 0.00003 as estimated_cost  -- GPT-3.5 rate
FROM agent_executions
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY agent_id
ORDER BY estimated_cost DESC;
```

---

**Last Updated:** September 12, 2026  
**For:** MULTIC Architecture Team  
**Confidence Level:** High (based on proven production systems)
