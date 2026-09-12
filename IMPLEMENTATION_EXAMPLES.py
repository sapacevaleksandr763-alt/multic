"""
MULTIC Architecture Implementation Examples
Based on CrewAI + LangGraph hybrid pattern with Zapier-style step execution

Author: Claude Code Agent
Date: September 12, 2026
Purpose: Production-ready code examples for MULTIC agents
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid
import logging
from abc import ABC, abstractmethod
import asyncio

# ============================================================================
# SECTION 1: STATE MODELS (Type-Safe)
# ============================================================================

class ContentRequestStatus(str, Enum):
    """Workflow status tracking"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESEARCH_COMPLETE = "research_complete"
    WRITING_COMPLETE = "writing_complete"
    REVIEW_COMPLETE = "review_complete"
    PUBLISHED = "published"
    FAILED = "failed"


class ContentPlatform(str, Enum):
    """Supported social platforms"""
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"


class ConfidenceLevel(float, Enum):
    """Confidence score ranges"""
    VERY_LOW = 0.3
    LOW = 0.5
    MEDIUM = 0.65
    HIGH = 0.8
    VERY_HIGH = 0.95


class ContentRequest(BaseModel):
    """Initial content request - IMMUTABLE"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    platforms: List[ContentPlatform]
    tone: str = "professional"
    urgency: str = "normal"
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True  # Immutable - prevents accidental mutation


class AgentExecutionLog(BaseModel):
    """Single agent execution record"""
    agent_id: str
    task_name: str
    step_number: int
    status: str  # "success", "failure", "skipped"
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    tokens_used: int
    duration_ms: int
    confidence_score: float = 0.0
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WorkflowState(BaseModel):
    """Complete workflow execution state"""
    request_id: str
    status: ContentRequestStatus

    # Step outputs (immutable once set)
    research_output: Optional[Dict[str, Any]] = None
    writing_output: Optional[Dict[str, Any]] = None
    review_output: Optional[Dict[str, Any]] = None

    # Tracking
    execution_logs: List[AgentExecutionLog] = []
    confidence_scores: Dict[str, float] = {}  # agent_id -> score
    total_tokens_used: int = 0

    # Review & Publishing
    requires_human_review: bool = True
    human_review_deadline: Optional[datetime] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    published_results: Dict[ContentPlatform, str] = {}  # platform -> post_id
    published_at: Optional[datetime] = None

    # Error tracking
    error_message: Optional[str] = None
    error_stack: Optional[str] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# SECTION 2: AGENT BASE CLASS (Framework-Agnostic)
# ============================================================================

class AgentBase(ABC):
    """
    Abstract base class for all agents.
    Implements core patterns:
    - Iteration limits (max_iter=3-5)
    - Token tracking
    - Confidence scoring
    - Comprehensive logging
    """

    def __init__(
        self,
        agent_id: str,
        role: str,
        max_iter: int = 3,
        max_tokens: int = 2000,
    ):
        self.agent_id = agent_id
        self.role = role
        self.max_iter = max_iter
        self.max_tokens = max_tokens
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.iteration_count = 0
        self.tokens_used = 0

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent task.
        Must return:
        {
            "output": {...},
            "confidence_score": 0.0-1.0,
            "tokens_used": int,
            "status": "success" | "failure"
        }
        """
        pass

    def _check_limits(self) -> bool:
        """Check if agent has exceeded limits"""
        if self.iteration_count >= self.max_iter:
            self.logger.warning(
                f"Agent {self.agent_id} exceeded max_iter ({self.max_iter})"
            )
            return False

        if self.tokens_used >= self.max_tokens:
            self.logger.warning(
                f"Agent {self.agent_id} exceeded max_tokens ({self.max_tokens})"
            )
            return False

        return True

    def _log_execution(
        self,
        task_name: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        tokens_used: int,
        confidence_score: float,
        status: str = "success",
        error: Optional[str] = None,
    ) -> AgentExecutionLog:
        """Log agent execution with complete state"""
        log = AgentExecutionLog(
            agent_id=self.agent_id,
            task_name=task_name,
            step_number=self.iteration_count,
            status=status,
            input_data=input_data,
            output_data=output_data,
            tokens_used=tokens_used,
            confidence_score=confidence_score,
            error_message=error,
            duration_ms=0,  # Calculate in real implementation
        )

        self.logger.info(
            f"Execution: {task_name} | "
            f"Tokens: {tokens_used} | "
            f"Confidence: {confidence_score:.2f} | "
            f"Status: {status}"
        )

        return log

    def _increment_iteration(self):
        """Safely increment iteration counter"""
        self.iteration_count += 1
        if not self._check_limits():
            raise RuntimeError(
                f"Agent {self.agent_id} exceeded iteration/token limits"
            )


# ============================================================================
# SECTION 3: CONCRETE AGENT IMPLEMENTATIONS
# ============================================================================

class ScoutAgent(AgentBase):
    """
    Research and discovery agent.
    Task: Research topic, find trending content, analyze competitors
    """

    def __init__(self):
        super().__init__(
            agent_id="scout_researcher",
            role="Researcher",
            max_iter=3,
            max_tokens=1500,
        )

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Research the topic.
        Input: {topic: str, platforms: List[str]}
        Output: {research_findings: str, sources: List[str], confidence: float}
        """
        if not self._check_limits():
            return {
                "output": {},
                "confidence_score": 0.0,
                "tokens_used": 0,
                "status": "failure",
                "error": "Agent iteration/token limits exceeded"
            }

        try:
            self._increment_iteration()
            topic = input_data.get("topic", "")

            # REAL IMPLEMENTATION: Call Claude API with research tools
            # For this example, we mock it
            research_findings = f"Research findings for: {topic}"
            sources = ["source1.com", "source2.com"]
            tokens_used = 800
            confidence = 0.87

            output = {
                "research_findings": research_findings,
                "sources": sources,
                "trending_topics": ["AI", "automation"],
                "competitor_analysis": "Key competitors doing X, Y, Z",
            }

            self._log_execution(
                task_name="research",
                input_data=input_data,
                output_data=output,
                tokens_used=tokens_used,
                confidence_score=confidence,
            )

            self.tokens_used += tokens_used

            return {
                "output": output,
                "confidence_score": confidence,
                "tokens_used": tokens_used,
                "status": "success",
            }

        except Exception as e:
            self.logger.error(f"Scout agent failed: {str(e)}", exc_info=True)
            return {
                "output": {},
                "confidence_score": 0.0,
                "tokens_used": 0,
                "status": "failure",
                "error": str(e),
            }


class WriterAgent(AgentBase):
    """
    Content creation agent.
    Task: Write engaging content based on research
    """

    def __init__(self):
        super().__init__(
            agent_id="writer_content",
            role="Content Writer",
            max_iter=5,
            max_tokens=2500,
        )

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Write content.
        Input: {research_findings: str, platforms: List[str], tone: str}
        Output: {content_by_platform: Dict[str, str], confidence: float}
        """
        if not self._check_limits():
            return {
                "output": {},
                "confidence_score": 0.0,
                "tokens_used": 0,
                "status": "failure",
            }

        try:
            self._increment_iteration()

            platforms = input_data.get("platforms", [])
            research = input_data.get("research_findings", "")
            tone = input_data.get("tone", "professional")

            # REAL IMPLEMENTATION: Call Claude API with writing tools
            # For example:
            content_by_platform = {
                "twitter": "Tweet version of content (280 chars)",
                "linkedin": "LinkedIn version of content (full article)",
                "instagram": "Instagram caption version",
            }

            tokens_used = 1200
            confidence = 0.82

            self._log_execution(
                task_name="writing",
                input_data=input_data,
                output_data=content_by_platform,
                tokens_used=tokens_used,
                confidence_score=confidence,
            )

            self.tokens_used += tokens_used

            return {
                "output": content_by_platform,
                "confidence_score": confidence,
                "tokens_used": tokens_used,
                "status": "success",
            }

        except Exception as e:
            self.logger.error(f"Writer agent failed: {str(e)}", exc_info=True)
            return {
                "output": {},
                "confidence_score": 0.0,
                "tokens_used": 0,
                "status": "failure",
                "error": str(e),
            }


class EditorAgent(AgentBase):
    """
    Quality review and approval agent.
    Task: Review content quality, brand fit, compliance
    """

    def __init__(self):
        super().__init__(
            agent_id="editor_review",
            role="Quality Editor",
            max_iter=2,
            max_tokens=1000,
        )

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review content.
        Input: {content_by_platform: Dict[str, str]}
        Output: {review_score: float, feedback: str, approved: bool}
        """
        if not self._check_limits():
            return {
                "output": {},
                "confidence_score": 0.0,
                "tokens_used": 0,
                "status": "failure",
            }

        try:
            self._increment_iteration()

            content = input_data.get("content_by_platform", {})

            # REAL IMPLEMENTATION: Quality checks
            # - Brand compliance
            # - Grammar/spelling
            # - Tone consistency
            # - Length constraints per platform

            review_score = 0.88
            approved = review_score >= 0.8
            feedback = "Content quality is good, minor tone adjustments for Twitter"

            tokens_used = 400

            self._log_execution(
                task_name="review",
                input_data=input_data,
                output_data={
                    "review_score": review_score,
                    "feedback": feedback,
                    "approved": approved,
                },
                tokens_used=tokens_used,
                confidence_score=review_score,
            )

            self.tokens_used += tokens_used

            return {
                "output": {
                    "review_score": review_score,
                    "feedback": feedback,
                    "approved": approved,
                },
                "confidence_score": review_score,
                "tokens_used": tokens_used,
                "status": "success",
            }

        except Exception as e:
            self.logger.error(f"Editor agent failed: {str(e)}", exc_info=True)
            return {
                "output": {},
                "confidence_score": 0.0,
                "tokens_used": 0,
                "status": "failure",
                "error": str(e),
            }


# ============================================================================
# SECTION 4: WORKFLOW ORCHESTRATOR (Manager Agent Pattern)
# ============================================================================

class WorkflowOrchestrator:
    """
    Central orchestrator that coordinates all agents.
    Implements Zapier's "step-based execution" pattern:
    - Each agent is independent
    - Orchestrator manages sequencing
    - Parallel execution where possible
    - Complete audit trail
    """

    def __init__(self):
        self.logger = logging.getLogger("orchestrator")
        self.agents = {
            "scout": ScoutAgent(),
            "writer": WriterAgent(),
            "editor": EditorAgent(),
        }
        # In production: use PostgreSQL instead of memory
        self.state_store: Dict[str, WorkflowState] = {}

    async def process_request(
        self,
        request: ContentRequest,
        state_persistence_fn=None,
    ) -> WorkflowState:
        """
        Process content request through full workflow.

        Workflow:
        1. Scout: Research topic
        2. Writer: Create content (parallel per platform is possible)
        3. Editor: Review and approve
        4. Publisher: Publish to platforms

        Args:
            request: ContentRequest object
            state_persistence_fn: Function to persist state (e.g., DB save)

        Returns:
            WorkflowState with complete execution log
        """

        # Initialize workflow state
        state = WorkflowState(
            request_id=request.request_id,
            status=ContentRequestStatus.PENDING,
        )
        self.state_store[request.request_id] = state

        self.logger.info(f"Starting workflow for request: {request.request_id}")

        try:
            # STEP 1: Scout Agent (Research)
            self.logger.info("Step 1: Scout agent researching topic")
            state.status = ContentRequestStatus.IN_PROGRESS

            scout_input = {
                "topic": request.topic,
                "platforms": request.platforms,
            }

            scout_result = self.agents["scout"].execute(scout_input)

            if scout_result["status"] == "failure":
                raise RuntimeError(f"Scout failed: {scout_result.get('error')}")

            state.research_output = scout_result["output"]
            state.confidence_scores["scout"] = scout_result["confidence_score"]
            state.total_tokens_used += scout_result["tokens_used"]
            state.status = ContentRequestStatus.RESEARCH_COMPLETE

            # STEP 2: Writer Agent (Create Content)
            self.logger.info("Step 2: Writer agent creating content")

            writer_input = {
                "research_findings": state.research_output.get("research_findings"),
                "platforms": request.platforms,
                "tone": request.tone,
            }

            writer_result = self.agents["writer"].execute(writer_input)

            if writer_result["status"] == "failure":
                raise RuntimeError(f"Writer failed: {writer_result.get('error')}")

            state.writing_output = writer_result["output"]
            state.confidence_scores["writer"] = writer_result["confidence_score"]
            state.total_tokens_used += writer_result["tokens_used"]
            state.status = ContentRequestStatus.WRITING_COMPLETE

            # STEP 3: Editor Agent (Review)
            self.logger.info("Step 3: Editor agent reviewing content")

            editor_input = {
                "content_by_platform": state.writing_output,
            }

            editor_result = self.agents["editor"].execute(editor_input)

            if editor_result["status"] == "failure":
                raise RuntimeError(f"Editor failed: {editor_result.get('error')}")

            state.review_output = editor_result["output"]
            state.confidence_scores["editor"] = editor_result["confidence_score"]
            state.total_tokens_used += editor_result["tokens_used"]
            state.status = ContentRequestStatus.REVIEW_COMPLETE

            # STEP 4: Determine human review requirement
            avg_confidence = sum(state.confidence_scores.values()) / len(state.confidence_scores)

            if avg_confidence >= 0.95:
                # Very high confidence - can auto-publish
                state.requires_human_review = False
                self.logger.info(
                    f"High confidence ({avg_confidence:.2f}) - auto-publish enabled"
                )
            elif avg_confidence >= 0.80:
                # High confidence - auto-publish with review after
                state.requires_human_review = False
                self.logger.info(
                    f"Medium-high confidence ({avg_confidence:.2f}) - auto-publish enabled"
                )
            else:
                # Lower confidence - require human review
                state.requires_human_review = True
                self.logger.info(
                    f"Lower confidence ({avg_confidence:.2f}) - human review required"
                )

            # Persist state
            if state_persistence_fn:
                await state_persistence_fn(state)
            else:
                self.state_store[request.request_id] = state

            self.logger.info(
                f"Workflow completed for {request.request_id}. "
                f"Tokens: {state.total_tokens_used}, "
                f"Confidence: {avg_confidence:.2f}, "
                f"Requires review: {state.requires_human_review}"
            )

            state.status = ContentRequestStatus.PUBLISHED
            return state

        except Exception as e:
            self.logger.error(
                f"Workflow failed for {request.request_id}: {str(e)}",
                exc_info=True
            )
            state.status = ContentRequestStatus.FAILED
            state.error_message = str(e)

            if state_persistence_fn:
                await state_persistence_fn(state)

            return state

    def get_workflow_state(self, request_id: str) -> Optional[WorkflowState]:
        """Retrieve workflow state"""
        return self.state_store.get(request_id)

    def human_review(
        self,
        request_id: str,
        approved: bool,
        reviewer_id: str,
    ) -> WorkflowState:
        """Record human review decision"""
        state = self.get_workflow_state(request_id)
        if not state:
            raise ValueError(f"Request {request_id} not found")

        state.approved_by = reviewer_id if approved else None
        state.approved_at = datetime.utcnow() if approved else None

        self.logger.info(
            f"Human review for {request_id}: "
            f"Approved={approved}, Reviewer={reviewer_id}"
        )

        return state


# ============================================================================
# SECTION 5: USAGE EXAMPLE
# ============================================================================

async def example_workflow():
    """
    Example of how to use the MULTIC architecture.
    """

    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create orchestrator
    orchestrator = WorkflowOrchestrator()

    # Create content request
    request = ContentRequest(
        topic="AI content automation in 2026",
        platforms=[ContentPlatform.LINKEDIN, ContentPlatform.TWITTER],
        tone="professional",
        user_id="user_123",
    )

    # Process through workflow
    state = await orchestrator.process_request(request)

    # Print results
    print(f"\n{'='*60}")
    print(f"Workflow Results for {request.request_id}")
    print(f"{'='*60}")
    print(f"Status: {state.status}")
    print(f"Total Tokens: {state.total_tokens_used}")
    print(f"Confidence Scores: {state.confidence_scores}")
    print(f"Requires Human Review: {state.requires_human_review}")
    print(f"\nGenerated Content:")
    for platform, content in state.writing_output.items():
        print(f"\n{platform.upper()}:")
        print(f"  {content[:100]}...")
    print(f"\nEditor Feedback: {state.review_output.get('feedback')}")
    print(f"{'='*60}\n")


# ============================================================================
# SECTION 6: INTEGRATION WITH FASTAPI
# ============================================================================

"""
Example FastAPI integration (not fully implemented here, but shows the pattern):

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI()
orchestrator = WorkflowOrchestrator()

@app.post("/api/v1/content/generate")
async def generate_content(request: ContentRequest):
    '''
    Async content generation endpoint.
    Returns 202 Accepted immediately, processes in background.
    '''

    # Check for duplicate (idempotency)
    cached = cache.get(f"request:{request.request_id}")
    if cached:
        return JSONResponse(
            status_code=200,
            content={"status": "already_processed", "result": cached}
        )

    # Queue async task
    asyncio.create_task(
        orchestrator.process_request(
            request,
            state_persistence_fn=save_to_db,
        )
    )

    return JSONResponse(
        status_code=202,
        content={
            "message": "Content generation started",
            "request_id": request.request_id,
            "status_url": f"/api/v1/status/{request.request_id}",
        }
    )

@app.get("/api/v1/status/{request_id}")
async def get_status(request_id: str):
    '''Get current workflow status'''
    state = orchestrator.get_workflow_state(request_id)
    if not state:
        raise HTTPException(status_code=404, detail="Request not found")

    return {
        "request_id": request_id,
        "status": state.status,
        "confidence_scores": state.confidence_scores,
        "requires_human_review": state.requires_human_review,
        "tokens_used": state.total_tokens_used,
    }
"""


if __name__ == "__main__":
    # Run example
    asyncio.run(example_workflow())
