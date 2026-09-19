#!/usr/bin/env python3
"""
🤖 MULTIC Telegram Bot - Main Command Handler

Starts the Telegram bot and handles commands:
- /start: Bot initialization and greeting
- Other commands handled by Scout/Copywriter/Promotion agents
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/telegram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Get token from .env (never hardcode it!)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env файле!")

class TelegramBot:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.app = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        logger.info(f"User {update.effective_user.id} started bot")
        await update.message.reply_text("Я на связи.")

    def setup_handlers(self):
        """Setup command handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        logger.info("✅ Command handlers registered")

    async def run(self):
        """Start the bot"""
        self.app = Application.builder().token(self.token).build()

        logger.info("🤖 Initializing MULTIC Telegram Bot...")
        logger.info(f"✅ Bot token loaded from .env")

        self.setup_handlers()

        logger.info("🚀 Starting bot polling...")
        await self.app.run_polling()

async def main():
    """Main entry point"""
    try:
        bot = TelegramBot()
        await bot.run()
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
