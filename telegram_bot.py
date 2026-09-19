#!/usr/bin/env python3
"""
🤖 MULTIC Telegram Bot - Main Command Handler

Starts the Telegram bot and handles commands:
- /start: Bot initialization and greeting
- Other commands handled by Scout/Copywriter/Promotion agents
"""

import logging
import os
import sys

# Setup console logging FIRST (before any errors)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

print("=" * 80)
print("🤖 MULTIC TELEGRAM BOT - STARTUP")
print("=" * 80)

# Check and import dotenv
print("\n[1/5] Loading environment variables...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded")
except ImportError as e:
    print(f"❌ ERROR: python-dotenv not installed: {e}")
    print("   Fix: pip install python-dotenv==1.0.1")
    sys.exit(1)

# Load token from .env
print("[2/5] Reading TELEGRAM_BOT_TOKEN from .env...")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN not found in .env")
    print("   Fix: Add line to .env: TELEGRAM_BOT_TOKEN=<your_token>")
    sys.exit(1)
else:
    print(f"✅ Token loaded (first 20 chars): {TELEGRAM_BOT_TOKEN[:20]}...")

# Check and import telegram
print("[3/5] Importing python-telegram-bot...")
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    print("✅ python-telegram-bot imported successfully")
except ImportError as e:
    print(f"❌ ERROR: python-telegram-bot not installed: {e}")
    print("   Fix: pip install python-telegram-bot==20.7")
    sys.exit(1)

# Create logs directory if it doesn't exist
print("[4/5] Setting up logs directory...")
if not os.path.exists('logs'):
    os.makedirs('logs')
    print("✅ Created logs directory")
else:
    print("✅ Logs directory exists")

# Setup file logging
try:
    file_handler = logging.FileHandler('logs/telegram_bot.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    print("✅ File logging configured (logs/telegram_bot.log)")
except Exception as e:
    print(f"⚠️  WARNING: Could not setup file logging: {e}")

print("[5/5] Initialization complete")

class TelegramBot:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.app = None
        logger.info("TelegramBot class initialized")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        logger.info(f"[/start] User {user_id} ({user_name}) sent /start")
        print(f"📨 /start command received from {user_name} (ID: {user_id})")
        await update.message.reply_text("Я на связи.")
        logger.info(f"[/start] Replied to user {user_id}")

    def setup_handlers(self):
        """Setup command handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        logger.info("✅ Command handlers registered")
        print("✅ Command handlers registered")

    async def run(self):
        """Start the bot"""
        try:
            self.app = Application.builder().token(self.token).build()
            logger.info("Bot application created")
            print("✅ Bot application created")

            self.setup_handlers()

            logger.info("🚀 Bot is running and listening for commands...")
            print("\n" + "=" * 80)
            print("🚀 BOT IS READY - WAITING FOR COMMANDS")
            print("=" * 80)
            print("Listening for messages in Telegram...")
            print("Press Ctrl+C to stop\n")

            await self.app.run_polling()
        except Exception as e:
            logger.error(f"❌ Error in bot.run(): {str(e)}", exc_info=True)
            print(f"❌ ERROR in bot.run(): {str(e)}")
            raise

async def main():
    """Main entry point"""
    try:
        print("\n" + "=" * 80)
        print("✅ ALL CHECKS PASSED - STARTING BOT")
        print("=" * 80 + "\n")

        bot = TelegramBot()
        await bot.run()
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user (Ctrl+C)")
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ FATAL ERROR: {str(e)}")
        logger.error(f"FATAL ERROR: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ FATAL ERROR in main: {str(e)}")
        logger.error(f"FATAL ERROR in main: {str(e)}", exc_info=True)
        sys.exit(1)
