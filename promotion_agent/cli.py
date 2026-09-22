"""Command-line interface for Promotion Agent workflow"""

import logging
import re
from promotion_agent.config import PromotionConfig
from promotion_agent.workflow import PromotionWorkflow

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PromotionCLI:
    """Interactive CLI for managing video promotion workflow"""

    def __init__(self, config: PromotionConfig = None):
        if config is None:
            config = PromotionConfig.from_env()

        self.config = config
        self.workflow = PromotionWorkflow(config)
        self.current_videos = []

        logger.info("PromotionCLI initialized")

    def print_welcome(self):
        """Print welcome message"""
        print("\n" + "="*70)
        print("🎬 MULTIC PROMOTION AGENT - Phase 2C")
        print("="*70)
        print("\nWORKFLOW PHASES:")
        print("  1️⃣  DISCOVER - Find videos (Wed/Sat)")
        print("  2️⃣  REVIEW - Approve/reject videos")
        print("  3️⃣  DOWNLOAD - Download & process")
        print("  4️⃣  PUBLISH - Publish to 7 platforms")
        print("  5️⃣  POSTS - Generate social posts (1 day later)")
        print("  6️⃣  REPUBLISH - Republish on demand")
        print("\nCOMMANDS:")
        print("  /discover - Find new videos")
        print("  /review - Generate review PDF/JSON")
        print("  /approve <index> - Approve video for publishing")
        print("  /reject <index> <reason> - Reject with feedback")
        print("  /download <video_id> <url> - Download video")
        print("  /publish <video_id> - Publish to all platforms")
        print("  /posts <video_id> - Generate social posts")
        print("  /republish <video_id> - Republish video")
        print("  /status - Show workflow status")
        print("  /help - Show this help")
        print("  /exit - Exit CLI")
        print("="*70 + "\n")

    def parse_command(self, user_input: str) -> tuple:
        """Parse user command"""
        parts = user_input.strip().split(maxsplit=1)
        if not parts:
            return None, None

        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        return command, args

    def run(self):
        """Main CLI loop"""
        self.print_welcome()

        while True:
            try:
                user_input = input("\n▶️  Enter command: ").strip()

                if not user_input:
                    continue

                command, args = self.parse_command(user_input)

                if command == "/discover":
                    self.cmd_discover()

                elif command == "/review":
                    self.cmd_review()

                elif command == "/approve":
                    self.cmd_approve(args)

                elif command == "/reject":
                    self.cmd_reject(args)

                elif command == "/download":
                    self.cmd_download(args)

                elif command == "/publish":
                    self.cmd_publish(args)

                elif command == "/posts":
                    self.cmd_posts(args)

                elif command == "/republish":
                    self.cmd_republish(args)

                elif command == "/status":
                    self.cmd_status()

                elif command == "/help":
                    self.print_welcome()

                elif command == "/exit":
                    print("\n👋 Goodbye!")
                    break

                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type /help for available commands")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in CLI: {e}")
                print(f"❌ Error: {e}")

    def cmd_discover(self):
        """Execute /discover command"""
        print("\n" + "="*70)
        videos = self.workflow.discover_videos()
        self.current_videos = videos

        if videos:
            print(f"\n📋 Found {len(videos)} videos")
            for i, v in enumerate(videos[:5], 1):
                print(f"  {i}. {v.title[:60]}")
            if len(videos) > 5:
                print(f"  ... and {len(videos) - 5} more")

    def cmd_review(self):
        """Execute /review command"""
        if not self.current_videos:
            print("❌ No videos found. Run /discover first")
            return

        self.workflow.generate_review(self.current_videos)

    def cmd_approve(self, args: str):
        """Execute /approve command"""
        if not args:
            print("❌ Usage: /approve <video_id>")
            return

        video_id = args.strip()
        self.workflow.process_user_command("approve", video_id)

    def cmd_reject(self, args: str):
        """Execute /reject command"""
        if not args:
            print("❌ Usage: /reject <video_id> 'reason'")
            return

        match = re.match(r'(\S+)\s+["\'](.+?)["\']', args)
        if not match:
            print("❌ Usage: /reject <video_id> 'reason'")
            return

        video_id = match.group(1)
        reason = match.group(2)
        self.workflow.process_user_command("reject", video_id, reason)

    def cmd_download(self, args: str):
        """Execute /download command"""
        if not args:
            print("❌ Usage: /download <video_id> <url>")
            return

        parts = args.split(maxsplit=1)
        if len(parts) != 2:
            print("❌ Usage: /download <video_id> <url>")
            return

        video_id, url = parts
        result = self.workflow.download_and_process(video_id, url)

        if result:
            print(f"✅ Download successful")

    def cmd_publish(self, args: str):
        """Execute /publish command"""
        if not args:
            print("❌ Usage: /publish <video_id>")
            return

        video_id = args.strip()
        video = self.workflow.db.get_video(video_id)

        if not video:
            print(f"❌ Video not found: {video_id}")
            return

        self.workflow.publish_to_all_platforms(video)

    def cmd_posts(self, args: str):
        """Execute /posts command"""
        if not args:
            print("❌ Usage: /posts <video_id>")
            return

        video_id = args.strip()
        video = self.workflow.db.get_video(video_id)

        if not video:
            print(f"❌ Video not found: {video_id}")
            return

        self.workflow.generate_and_publish_posts(video)

    def cmd_republish(self, args: str):
        """Execute /republish command"""
        if not args:
            print("❌ Usage: /republish <video_id>")
            return

        video_id = args.strip()
        self.workflow.republish_video(video_id)

    def cmd_status(self):
        """Execute /status command"""
        self.workflow.print_status()


def main():
    """Main entry point"""
    try:
        config = PromotionConfig.from_env()
        cli = PromotionCLI(config)
        cli.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
