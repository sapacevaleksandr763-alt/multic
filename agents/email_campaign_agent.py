"""
📧 EMAIL CAMPAIGN AGENT - v4.0
Self-learning email marketing automation with conversion tracking
"""

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sqlite3


@dataclass
class EmailTemplate:
    """Email template with personalization"""
    name: str
    subject: str
    body: str
    cta_text: str
    cta_link: str
    send_delay_hours: int = 0
    goal: str = "engagement"  # engagement, conversion, retention


@dataclass
class CampaignResult:
    """Campaign performance result"""
    campaign_id: str
    email_template: str
    sent_count: int
    open_rate: float
    click_rate: float
    conversion_rate: float
    revenue_per_email: float
    quality_score: float
    timestamp: datetime


class EmailCampaignAgent:
    """
    Email marketing agent with self-learning and A/B testing

    Features:
    - Automated email sequences
    - Personalization based on user behavior
    - A/B testing for continuous improvement
    - Conversion tracking
    - Self-learning optimization
    """

    def __init__(self, mailchimp_api_key: str = None):
        self.mailchimp_api_key = mailchimp_api_key
        self.templates = self._init_templates()
        self.learning_db = self._init_learning_db()
        self.active_campaigns = {}

    def _init_templates(self) -> Dict[str, EmailTemplate]:
        """Initialize email templates"""
        return {
            "welcome": EmailTemplate(
                name="welcome",
                subject="🎉 Welcome to {name}!",
                body="""Hi {first_name},

Thank you for joining our community! You've made an amazing choice.

Inside, you'll discover:
✨ Exclusive content and strategies
💰 Money-making opportunities
🚀 Success stories from our members

Get started now and see the results.

Best regards,
The Team""",
                cta_text="Get Started Now",
                cta_link="/onboard",
                send_delay_hours=0,
                goal="engagement"
            ),

            "social_proof": EmailTemplate(
                name="social_proof",
                subject="See how {count} people earned ${amount} this month",
                body="""Hi {first_name},

I wanted to share something exciting with you.

{count} people just like you have earned ${amount} this month using our proven system.

Here's what they're saying:

"{testimonial}"

You could be next. Click below to see how:""",
                cta_text="See Success Stories",
                cta_link="/testimonials",
                send_delay_hours=24,
                goal="conversion"
            ),

            "authority": EmailTemplate(
                name="authority",
                subject="The {industry} expert's guide to {benefit}",
                body="""Hi {first_name},

As a recognized authority in {industry}, I've helped thousands achieve {benefit}.

My proprietary system covers:
✓ Proven framework
✓ Advanced strategies
✓ Real case studies
✓ Personal mentorship

Download my free guide now (limited time):""",
                cta_text="Download Free Guide",
                cta_link="/guide",
                send_delay_hours=48,
                goal="engagement"
            ),

            "urgency": EmailTemplate(
                name="urgency",
                subject="⏰ Last chance: {offer} expires in {hours} hours",
                body="""Hi {first_name},

This special offer expires in {hours} hours.

{offer_details}

Spots are filling up fast. Only {spots_left} remaining.

Secure yours now:""",
                cta_text="Claim Your Spot",
                cta_link="/offer",
                send_delay_hours=72,
                goal="conversion"
            ),

            "retention": EmailTemplate(
                name="retention",
                subject="We miss you! Here's {incentive}",
                body="""Hi {first_name},

It's been a while. We wanted to reconnect with you.

As a valued member, we're offering:
🎁 {incentive}
💰 Exclusive early access to new features
🌟 VIP customer support

Come back and see what's new:""",
                cta_text="Explore New Features",
                cta_link="/dashboard",
                send_delay_hours=0,
                goal="retention"
            )
        }

    def _init_learning_db(self) -> sqlite3.Connection:
        """Initialize SQLite for campaign learning"""
        db = sqlite3.connect(":memory:")
        db.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                template_name TEXT,
                sent_count INTEGER,
                open_rate REAL,
                click_rate REAL,
                conversion_rate REAL,
                revenue REAL,
                quality_score REAL,
                timestamp DATETIME,
                learned BOOLEAN DEFAULT 0
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS ab_tests (
                id TEXT PRIMARY KEY,
                campaign_id TEXT,
                variant_a_template TEXT,
                variant_b_template TEXT,
                winner TEXT,
                lift REAL,
                timestamp DATETIME
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS template_improvements (
                id TEXT PRIMARY KEY,
                template_name TEXT,
                improvement_type TEXT,
                change TEXT,
                lift REAL,
                timestamp DATETIME
            )
        """)
        db.commit()
        return db

    async def create_campaign(
        self,
        campaign_id: str,
        audience_size: int,
        templates: List[str] = None
    ) -> str:
        """Create new email campaign"""
        if templates is None:
            templates = ["welcome", "social_proof", "authority", "urgency"]

        campaign_data = {
            "id": campaign_id,
            "audience_size": audience_size,
            "templates": templates,
            "created_at": datetime.now().isoformat(),
            "status": "scheduled"
        }

        self.active_campaigns[campaign_id] = campaign_data
        return campaign_id

    async def send_email_sequence(
        self,
        campaign_id: str,
        recipient_list: List[Dict],
        personalization: Dict = None
    ) -> Dict:
        """Send automated email sequence"""
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {"error": "Campaign not found"}

        results = {
            "campaign_id": campaign_id,
            "emails_sent": 0,
            "total_scheduled": 0,
            "sequence": []
        }

        for template_name in campaign["templates"]:
            template = self.templates.get(template_name)
            if not template:
                continue

            # Send with delay
            await asyncio.sleep(template.send_delay_hours * 0.1)  # Simulate delay

            sent_count = len(recipient_list)
            results["emails_sent"] += sent_count
            results["total_scheduled"] += sent_count

            # Simulate sending
            sequence_result = {
                "template": template_name,
                "sent": sent_count,
                "scheduled_time": (datetime.now() + timedelta(hours=template.send_delay_hours)).isoformat()
            }
            results["sequence"].append(sequence_result)

        return results

    async def track_campaign_results(
        self,
        campaign_id: str,
        open_count: int,
        click_count: int,
        conversion_count: int,
        revenue: float
    ) -> CampaignResult:
        """Track campaign performance"""
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return None

        sent_count = campaign["audience_size"]

        # Calculate metrics
        open_rate = open_count / sent_count if sent_count > 0 else 0
        click_rate = click_count / open_count if open_count > 0 else 0
        conversion_rate = conversion_count / click_count if click_count > 0 else 0
        revenue_per_email = revenue / sent_count if sent_count > 0 else 0

        # Quality score (0-100)
        quality_score = (
            open_rate * 100 * 0.3 +
            click_rate * 100 * 0.3 +
            conversion_rate * 100 * 0.4
        )

        result = CampaignResult(
            campaign_id=campaign_id,
            email_template=campaign["templates"][0],
            sent_count=sent_count,
            open_rate=open_rate,
            click_rate=click_rate,
            conversion_rate=conversion_rate,
            revenue_per_email=revenue_per_email,
            quality_score=quality_score,
            timestamp=datetime.now()
        )

        # Record for learning
        self._record_campaign_result(result)

        return result

    def _record_campaign_result(self, result: CampaignResult):
        """Record campaign results for learning"""
        self.learning_db.execute("""
            INSERT INTO campaigns
            (id, template_name, sent_count, open_rate, click_rate, conversion_rate, revenue, quality_score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.campaign_id,
            result.email_template,
            result.sent_count,
            result.open_rate,
            result.click_rate,
            result.conversion_rate,
            result.revenue_per_email * result.sent_count,
            result.quality_score,
            result.timestamp
        ))
        self.learning_db.commit()

    async def ab_test_templates(
        self,
        campaign_id: str,
        template_a: str,
        template_b: str,
        audience_split: float = 0.5
    ) -> Dict:
        """Run A/B test between two templates"""
        test_id = f"ab_test_{campaign_id}_{datetime.now().isoformat()}"

        return {
            "test_id": test_id,
            "campaign_id": campaign_id,
            "variant_a": template_a,
            "variant_b": template_b,
            "status": "running",
            "sample_size": 1000,
            "duration_hours": 72
        }

    async def learn_and_optimize(self):
        """Self-learning optimization of templates"""
        # Get all unlearned campaigns
        cursor = self.learning_db.execute("""
            SELECT template_name, AVG(quality_score) as avg_quality,
                   AVG(open_rate) as avg_open, AVG(conversion_rate) as avg_conversion,
                   COUNT(*) as count
            FROM campaigns
            WHERE learned = 0
            GROUP BY template_name
            ORDER BY avg_quality DESC
        """)

        results = cursor.fetchall()
        if not results:
            return

        best_template = results[0]  # Best performing template

        # Optimize underperforming templates
        for template_name, quality_score, open_rate, conversion_rate, count in results[1:]:
            if count >= 3:  # Only optimize if we have enough data
                improvement = self._calculate_improvements(
                    template_name,
                    best_template,
                    quality_score
                )

                if improvement:
                    self._apply_template_improvement(template_name, improvement)

        # Mark as learned
        self.learning_db.execute("""
            UPDATE campaigns SET learned = 1 WHERE learned = 0
        """)
        self.learning_db.commit()

    def _calculate_improvements(
        self,
        underperforming_template: str,
        best_template: tuple,
        current_quality: float
    ) -> Optional[Dict]:
        """Calculate what improvements could be made"""
        template = self.templates.get(underperforming_template)
        best_name = best_template[0]
        best_quality = best_template[1]

        if current_quality >= best_quality * 0.9:
            return None  # Close enough

        # Calculate what to improve
        quality_gap = best_quality - current_quality
        lift_potential = quality_gap / best_quality

        improvements = {
            "template_name": underperforming_template,
            "best_template": best_name,
            "current_quality": current_quality,
            "target_quality": best_quality,
            "lift_potential": lift_potential,
            "improvements": []
        }

        # Suggest improvements
        if lift_potential > 0.15:
            improvements["improvements"].extend([
                {"type": "subject_line", "recommendation": f"Study {best_name}'s subject line"},
                {"type": "cta", "recommendation": "Make CTA more urgent"},
                {"type": "body", "recommendation": "Add social proof"}
            ])

        return improvements if improvements["improvements"] else None

    def _apply_template_improvement(self, template_name: str, improvement: Dict):
        """Apply improvements to template"""
        template = self.templates.get(template_name)
        if not template:
            return

        for change in improvement["improvements"]:
            # Record improvement
            improvement_id = f"imp_{template_name}_{datetime.now().isoformat()}"

            self.learning_db.execute("""
                INSERT INTO template_improvements
                (id, template_name, improvement_type, change, lift, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                improvement_id,
                template_name,
                change["type"],
                change["recommendation"],
                improvement["lift_potential"],
                datetime.now()
            ))

        self.learning_db.commit()

    def get_template_stats(self) -> Dict:
        """Get performance stats for all templates"""
        cursor = self.learning_db.execute("""
            SELECT template_name, COUNT(*) as campaigns,
                   AVG(quality_score) as avg_quality,
                   AVG(open_rate) as avg_open,
                   AVG(conversion_rate) as avg_conversion
            FROM campaigns
            GROUP BY template_name
            ORDER BY avg_quality DESC
        """)

        stats = {}
        for row in cursor.fetchall():
            template_name, campaigns, avg_quality, avg_open, avg_conversion = row
            stats[template_name] = {
                "campaigns_sent": campaigns,
                "avg_quality_score": avg_quality,
                "avg_open_rate": avg_open,
                "avg_conversion_rate": avg_conversion
            }

        return stats

    async def generate_personalized_email(
        self,
        template_name: str,
        user_data: Dict
    ) -> str:
        """Generate personalized email from template"""
        template = self.templates.get(template_name)
        if not template:
            return ""

        body = template.body
        for key, value in user_data.items():
            body = body.replace(f"{{{key}}}", str(value))

        return body


# Example usage
async def main():
    agent = EmailCampaignAgent()

    # Create campaign
    campaign_id = await agent.create_campaign(
        campaign_id="campaign_001",
        audience_size=1000,
        templates=["welcome", "social_proof", "urgency"]
    )

    # Send emails
    recipients = [
        {"email": f"user{i}@example.com", "name": f"User {i}"}
        for i in range(100)
    ]

    send_result = await agent.send_email_sequence(
        campaign_id=campaign_id,
        recipient_list=recipients
    )

    print(f"Email sequence sent: {send_result}")

    # Simulate results
    result = await agent.track_campaign_results(
        campaign_id=campaign_id,
        open_count=450,
        click_count=95,
        conversion_count=38,
        revenue=1900
    )

    print(f"Campaign result: {result}")

    # Learn and optimize
    await agent.learn_and_optimize()

    # Show stats
    print(f"Template stats: {agent.get_template_stats()}")


if __name__ == "__main__":
    asyncio.run(main())
