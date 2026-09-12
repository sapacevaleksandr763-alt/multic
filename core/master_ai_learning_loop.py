"""
🧠 MASTER AI - Self-Learning Feedback Loop (v4.0)
Core implementation of autonomous self-improving system
"""

import asyncio
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod


@dataclass
class SystemMetrics:
    """System performance metrics from one cycle"""
    cycle_number: int
    phase_started: str
    views: int
    engagement: float
    conversions: int
    revenue: float
    quality_score: float
    decision: str
    execution_time: float
    timestamp: datetime


class LearningMemory(ABC):
    """Abstract base for learning storage"""

    @abstractmethod
    async def save_metric(self, metric: SystemMetrics):
        pass

    @abstractmethod
    async def get_recent_metrics(self, limit: int = 100) -> List[SystemMetrics]:
        pass

    @abstractmethod
    async def identify_patterns(self) -> Dict:
        pass


class SQLiteLearningMemory(LearningMemory):
    """SQLite-based persistent learning memory"""

    def __init__(self, db_path: str = "multic_learning.db"):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        """Create database schema"""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS cycle_metrics (
                cycle_id INTEGER PRIMARY KEY,
                phase TEXT,
                views INTEGER,
                engagement REAL,
                conversions INTEGER,
                revenue REAL,
                quality_score REAL,
                decision TEXT,
                execution_time REAL,
                timestamp DATETIME,
                analyzed BOOLEAN DEFAULT 0
            )
        """)

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS identified_patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT,
                description TEXT,
                confidence REAL,
                data JSON,
                first_seen DATETIME,
                last_seen DATETIME,
                occurrence_count INTEGER
            )
        """)

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS strategy_decisions (
                decision_id TEXT PRIMARY KEY,
                decision_text TEXT,
                rationale TEXT,
                expected_result TEXT,
                actual_result TEXT,
                success BOOLEAN,
                cycle_number INTEGER,
                timestamp DATETIME
            )
        """)

        self.db.commit()

    async def save_metric(self, metric: SystemMetrics):
        """Save cycle metrics"""
        self.db.execute("""
            INSERT INTO cycle_metrics
            (phase, views, engagement, conversions, revenue, quality_score, decision, execution_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            metric.phase_started,
            metric.views,
            metric.engagement,
            metric.conversions,
            metric.revenue,
            metric.quality_score,
            metric.decision,
            metric.execution_time,
            metric.timestamp
        ))
        self.db.commit()

    async def get_recent_metrics(self, limit: int = 100) -> List[SystemMetrics]:
        """Get recent metrics for analysis"""
        cursor = self.db.execute("""
            SELECT cycle_id, phase, views, engagement, conversions, revenue,
                   quality_score, decision, execution_time, timestamp
            FROM cycle_metrics
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        metrics = []
        for row in cursor.fetchall():
            metrics.append(SystemMetrics(
                cycle_number=row[0],
                phase_started=row[1],
                views=row[2],
                engagement=row[3],
                conversions=row[4],
                revenue=row[5],
                quality_score=row[6],
                decision=row[7],
                execution_time=row[8],
                timestamp=row[9]
            ))

        return metrics

    async def identify_patterns(self) -> Dict:
        """Identify patterns in historical data"""
        cursor = self.db.execute("""
            SELECT phase, AVG(views) as avg_views, AVG(engagement) as avg_engagement,
                   AVG(quality_score) as avg_quality, COUNT(*) as count
            FROM cycle_metrics
            WHERE analyzed = 0
            GROUP BY phase
        """)

        patterns = {}
        for row in cursor.fetchall():
            phase, avg_views, avg_engagement, avg_quality, count = row

            if count >= 3:  # Only consider patterns with 3+ samples
                patterns[phase] = {
                    "avg_views": avg_views,
                    "avg_engagement": avg_engagement,
                    "avg_quality": avg_quality,
                    "sample_size": count,
                    "reliability": min(count / 10, 1.0)
                }

        # Mark as analyzed
        self.db.execute("UPDATE cycle_metrics SET analyzed = 1 WHERE analyzed = 0")
        self.db.commit()

        return patterns


class MasterAI:
    """
    Master AI - Autonomous self-learning system
    Implements continuous feedback loop: Decide → Execute → Measure → Learn → Adapt
    """

    def __init__(
        self,
        claude_client=None,
        youtube_client=None,
        telegram_client=None,
        email_agent=None,
        video_editor=None
    ):
        self.claude = claude_client
        self.youtube = youtube_client
        self.telegram = telegram_client
        self.email_agent = email_agent
        self.video_editor = video_editor

        self.memory = SQLiteLearningMemory()
        self.cycle_count = 0
        self.is_running = False

        # Performance tracking
        self.best_strategies = {}
        self.failed_strategies = []
        self.current_knowledge = {
            "top_topics": [],
            "best_formats": [],
            "optimal_posting_times": [],
            "successful_prompts": []
        }

    async def main_loop(self, cycles: Optional[int] = None):
        """
        Main autonomous loop - runs forever or for N cycles

        Each cycle: Decide → Execute → Measure → Learn → Adapt
        """
        self.is_running = True
        self.cycle_count = 0

        while self.is_running and (cycles is None or self.cycle_count < cycles):
            try:
                self.cycle_count += 1
                cycle_start = datetime.now()

                print(f"\n{'='*60}")
                print(f"🔄 CYCLE {self.cycle_count} START")
                print(f"{'='*60}")

                # PHASE 1: DECIDE
                decision = await self._phase_decide()
                print(f"📋 DECISION: {decision[:100]}...")

                # PHASE 2: EXECUTE
                execution_result = await self._phase_execute(decision)
                print(f"✅ EXECUTION: {execution_result['status']}")

                # PHASE 3: MEASURE
                metrics = await self._phase_measure(execution_result)
                print(f"📊 METRICS: {metrics.views} views, {metrics.conversions} conversions")

                # PHASE 4: LEARN
                patterns = await self._phase_learn(metrics)
                print(f"🧠 LEARNED: {len(patterns)} new patterns")

                # PHASE 5: ADAPT
                adaptations = await self._phase_adapt(patterns)
                print(f"⚡ ADAPTED: {len(adaptations)} strategy changes")

                cycle_duration = (datetime.now() - cycle_start).total_seconds()
                print(f"⏱️  Cycle time: {cycle_duration:.1f}s")

                # Wait before next cycle (e.g., 1 hour)
                wait_time = 3600 - cycle_duration
                if wait_time > 0:
                    print(f"⏳ Waiting {wait_time/60:.0f} minutes for next cycle...")
                    await asyncio.sleep(min(wait_time, 60))  # Cap wait to 1 min for testing

            except Exception as e:
                print(f"❌ Error in cycle {self.cycle_count}: {e}")
                await asyncio.sleep(300)  # Wait 5 min before retry

    async def _phase_decide(self) -> str:
        """
        PHASE 1: DECIDE - Ask Claude what to do next
        Uses knowledge base + recent metrics to make strategic decision
        """
        # Get context
        recent_metrics = await self.memory.get_recent_metrics(10)
        patterns = await self.memory.identify_patterns()

        context = self._build_decision_context(recent_metrics, patterns)

        # Ask Claude
        prompt = f"""
You are managing an AI-powered viral content system with self-learning capabilities.

CURRENT KNOWLEDGE:
{json.dumps(self.current_knowledge, indent=2)}

RECENT PERFORMANCE:
{json.dumps(context, indent=2)}

IDENTIFY PATTERNS AND DECIDE:

What should the system do in this cycle?

Choose one specific action:
1. Find more videos on best-performing topic
2. Try a new trending topic
3. Change content format/style
4. Adjust posting schedule
5. Optimize existing content for reposting
6. Test new marketing angle
7. Focus on email conversion optimization
8. Combine top 2 strategies from different categories

Provide decision in 1-2 sentences with specific parameters.
        """

        if self.claude:
            decision = await self.claude.ask(prompt)
        else:
            decision = "Find more videos on trending topics"

        return decision

    async def _phase_execute(self, decision: str) -> Dict:
        """
        PHASE 2: EXECUTE - Perform the decided action
        Uses agents to execute decision
        """
        # Simulate execution (in production, would use actual agents)
        await asyncio.sleep(0.5)

        result = {
            "status": "success",
            "decision": decision,
            "videos_found": 5,
            "content_created": 15,
            "content_published": 15,
            "platforms": ["telegram", "youtube"],
            "timestamp": datetime.now().isoformat()
        }

        return result

    async def _phase_measure(self, execution_result: Dict) -> SystemMetrics:
        """
        PHASE 3: MEASURE - Track results of actions
        Measures views, engagement, conversions, etc.
        """
        # Simulate measurement (in production, would query APIs)
        metrics = SystemMetrics(
            cycle_number=self.cycle_count,
            phase_started="execute",
            views=int(2000 + self.cycle_count * 100),  # Simulate growth
            engagement=0.08 + (self.cycle_count * 0.001),
            conversions=int(50 + self.cycle_count * 2),
            revenue=int(250 + self.cycle_count * 10),
            quality_score=85 + min(self.cycle_count * 0.5, 15),
            decision=execution_result["decision"][:50],
            execution_time=execution_result.get("execution_time", 45.0),
            timestamp=datetime.now()
        )

        # Save metrics
        await self.memory.save_metric(metrics)

        return metrics

    async def _phase_learn(self, metrics: SystemMetrics) -> Dict:
        """
        PHASE 4: LEARN - Analyze results and extract learnings
        Identifies patterns and updates knowledge base
        """
        # Identify patterns
        patterns = await self.memory.identify_patterns()

        learnings = {
            "identified_patterns": patterns,
            "quality_score": metrics.quality_score,
            "growth_rate": metrics.views / max(self.cycle_count, 1),
            "conversion_efficiency": metrics.conversions / max(metrics.views, 1)
        }

        # Update knowledge base
        if metrics.quality_score > 85:
            self.current_knowledge["successful_prompts"].append(metrics.decision)

        if metrics.conversions > 50:
            self.current_knowledge["best_formats"].append("video")

        return learnings

    async def _phase_adapt(self, patterns: Dict) -> List[str]:
        """
        PHASE 5: ADAPT - Modify strategy based on learnings
        Adjusts parameters and tries new approaches
        """
        adaptations = []

        # Adaptation 1: Increase investment in successful strategies
        if patterns and any(p["avg_quality"] > 85 for p in patterns.values()):
            adaptations.append("Increase frequency of high-quality strategies")

        # Adaptation 2: Reduce investment in poor strategies
        if patterns and any(p["avg_quality"] < 70 for p in patterns.values()):
            adaptations.append("Test alternatives to low-quality phases")

        # Adaptation 3: Expand proven topics
        if self.current_knowledge["top_topics"]:
            adaptations.append(f"Deep-dive into: {self.current_knowledge['top_topics'][0]}")

        # Adaptation 4: Personalization
        if len(patterns) > 0:
            adaptations.append("Customize parameters based on audience response")

        return adaptations

    def _build_decision_context(
        self,
        recent_metrics: List[SystemMetrics],
        patterns: Dict
    ) -> Dict:
        """Build context for Claude decision"""
        if not recent_metrics:
            return {"message": "Insufficient data for decision context"}

        avg_views = sum(m.views for m in recent_metrics) / len(recent_metrics)
        avg_conversions = sum(m.conversions for m in recent_metrics) / len(recent_metrics)
        avg_quality = sum(m.quality_score for m in recent_metrics) / len(recent_metrics)

        return {
            "cycles_completed": self.cycle_count,
            "avg_views_per_cycle": avg_views,
            "avg_conversions_per_cycle": avg_conversions,
            "avg_quality_score": avg_quality,
            "patterns_identified": patterns,
            "top_topics": self.current_knowledge["top_topics"][:3],
            "best_formats": self.current_knowledge["best_formats"][:3]
        }

    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            "cycle_count": self.cycle_count,
            "is_running": self.is_running,
            "knowledge_base": self.current_knowledge,
            "timestamp": datetime.now().isoformat()
        }

    def stop(self):
        """Stop the autonomous loop"""
        self.is_running = False


# Example usage
async def main():
    master_ai = MasterAI()

    # Run for 3 cycles (demo)
    await master_ai.main_loop(cycles=3)

    # Show status
    print(f"\n📊 Final Status: {master_ai.get_system_status()}")


if __name__ == "__main__":
    asyncio.run(main())
