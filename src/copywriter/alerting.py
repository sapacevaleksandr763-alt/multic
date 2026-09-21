"""Alerting system for Copywriter Agent escalations."""

import os
import logging
import requests
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class AlertManager:
    """Send alerts to Slack and PagerDuty when videos escalate."""

    def __init__(self):
        """Initialize alert manager with API credentials from .env."""
        self.slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        self.pagerduty_key = os.getenv('PAGERDUTY_INTEGRATION_KEY')

    def alert_video_escalation(
        self,
        video_id: str,
        retry_count: int,
        error: str,
        component: str
    ):
        """Alert when video escalates to manual review.

        Args:
            video_id: ID of the video
            retry_count: Number of retry attempts
            error: Last error message
            component: Component that failed (titles, descriptions, comments)
        """
        message = f"""
🔴 CRITICAL: Video Escalated to Manual Review
├─ Video ID: {video_id}
├─ Component: {component}
├─ Retry Count: {retry_count}/5
├─ Last Error: {error[:100]}
├─ Time: {datetime.now().isoformat()}
└─ Action Required: Review at /admin/videos/{video_id}
        """

        logger.critical(message)

        if self.slack_webhook:
            self._send_slack(message, severity='critical')

        if self.pagerduty_key:
            self._send_pagerduty(
                summary=f"Video {video_id} ({component}) escalated after {retry_count} retries",
                description=error,
                severity='critical'
            )

    def alert_rate_limit_exceeded(self, current_rate: float, limit: float):
        """Alert when rate limit is exceeded."""
        message = f"""
⚠️ WARNING: Rate Limit Exceeded
├─ Current Rate: {current_rate:.2f} calls/min
├─ Limit: {limit:.2f} calls/min
├─ Time: {datetime.now().isoformat()}
└─ Action: Reduce concurrent calls or increase rate limit
        """

        logger.warning(message)

        if self.slack_webhook:
            self._send_slack(message, severity='warning')

    def alert_database_error(self, error: str, video_id: Optional[str] = None):
        """Alert when database error occurs."""
        message = f"""
🔴 CRITICAL: Database Error
├─ Video ID: {video_id or 'unknown'}
├─ Error: {error[:200]}
├─ Time: {datetime.now().isoformat()}
└─ Action Required: Check database connection
        """

        logger.error(message)

        if self.slack_webhook:
            self._send_slack(message, severity='critical')

        if self.pagerduty_key:
            self._send_pagerduty(
                summary="Database error in Copywriter Agent",
                description=error,
                severity='critical'
            )

    def _send_slack(self, message: str, severity: str = 'info'):
        """Send alert to Slack.

        Args:
            message: Alert message
            severity: critical, warning, or info
        """
        if not self.slack_webhook:
            return

        color_map = {
            'critical': 'danger',
            'warning': 'warning',
            'info': 'good'
        }

        payload = {
            'attachments': [{
                'color': color_map.get(severity, 'good'),
                'text': message,
                'ts': int(datetime.now().timestamp())
            }]
        }

        try:
            response = requests.post(self.slack_webhook, json=payload, timeout=5)
            if response.status_code != 200:
                logger.error(f"Slack alert failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending Slack alert: {e}")

    def _send_pagerduty(
        self,
        summary: str,
        description: str,
        severity: str = 'error'
    ):
        """Send alert to PagerDuty.

        Args:
            summary: Alert summary
            description: Alert details
            severity: critical, error, warning, or info
        """
        if not self.pagerduty_key:
            return

        payload = {
            'routing_key': self.pagerduty_key,
            'event_action': 'trigger',
            'dedup_key': f"copywriter-{datetime.now().timestamp()}",
            'payload': {
                'summary': summary,
                'severity': severity,
                'source': 'copywriter-agent',
                'custom_details': {
                    'description': description,
                    'timestamp': datetime.now().isoformat()
                }
            }
        }

        try:
            response = requests.post(
                'https://events.pagerduty.com/v2/enqueue',
                json=payload,
                timeout=5
            )
            if response.status_code != 202:
                logger.error(f"PagerDuty alert failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending PagerDuty alert: {e}")


# Global alert manager instance
_alert_manager = None


def get_alert_manager() -> AlertManager:
    """Get or create alert manager instance."""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager
