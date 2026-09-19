#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MULTIC Telegram Bot - Main Command Handler (API v22.8)

Starts the Telegram bot and handles commands:
- /start: Bot initialization and greeting
- Other commands handled by Scout/Copywriter/Promotion agents

Compatible with python-telegram-bot>=22.0
Uses synchronous run_polling() - NOT async/await pattern
"""

import logging
import os
import sys

# Fix terminal encoding for Windows PowerShell
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

# Setup console logging FIRST (before any errors)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

print("=" * 80)
print("[BOT] MULTIC TELEGRAM BOT - STARTUP")
print("=" * 80)

# Check and import dotenv
print("\n[1/5] Loading environment variables...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[OK] dotenv loaded")
except ImportError as e:
    print(f"[ERROR] python-dotenv not installed: {e}")
    print("   Fix: pip install python-dotenv")
    sys.exit(1)

# Load token from .env
print("[2/5] Reading TELEGRAM_BOT_TOKEN from .env...")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    print("[ERROR] ERROR: TELEGRAM_BOT_TOKEN not found in .env")
    print("   Fix: Add line to .env: TELEGRAM_BOT_TOKEN=<your_token>")
    sys.exit(1)
else:
    print(f"[OK] Token loaded (first 20 chars): {TELEGRAM_BOT_TOKEN[:20]}...")

# Check and import telegram
print("[3/5] Importing python-telegram-bot (v22.8+)...")
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    print("[OK] python-telegram-bot imported successfully")
except ImportError as e:
    print(f"[ERROR] ERROR: python-telegram-bot not installed: {e}")
    print("   Fix: pip install python-telegram-bot")
    sys.exit(1)

# Create logs directory if it doesn't exist
print("[4/5] Setting up logs directory...")
if not os.path.exists('logs'):
    os.makedirs('logs')
    print("[OK] Created logs directory")
else:
    print("[OK] Logs directory exists")

# Setup file logging
try:
    file_handler = logging.FileHandler('logs/telegram_bot.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    print("[OK] File logging configured (logs/telegram_bot.log)")
except Exception as e:
    print(f"[WARNING] Could not setup file logging: {e}")

print("[5/5] Initialization complete")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "User"
    logger.info(f"[/start] User {user_id} ({user_name}) sent /start")
    print(f"[CMD] /start command received from {user_name} (ID: {user_id})")
    await update.message.reply_text("Я на связи.")
    logger.info(f"[/start] Replied to user {user_id}")


def main() -> None:
    """Main entry point - Build and run the bot (python-telegram-bot v22.8+ API)

    IMPORTANT: This is synchronous - NOT async/await pattern.
    Uses app.run_polling() which manages its own event loop.
    DO NOT wrap this in asyncio.run() or use await.
    """
    try:
        print("\n" + "=" * 80)
        print("[OK] ALL CHECKS PASSED - STARTING BOT")
        print("=" * 80 + "\n")

        # Create the Application with token from .env
        logger.info("Creating bot application...")
        print("[OK] Creating bot application...")
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Add command handlers
        logger.info("Registering command handlers...")
        print("[OK] Registering command handlers...")
        app.add_handler(CommandHandler("start", start_command))

        logger.info("Bot setup complete, starting polling...")
        print("\n" + "=" * 80)
        print("[BOT] READY - LISTENING FOR COMMANDS")
        print("=" * 80)
        print("Listening for messages in Telegram...")
        print("Press Ctrl+C to stop\n")
        logger.info("Bot polling started")

        # Start the bot - SYNCHRONOUS method
        # run_polling() manages its own event loop - DO NOT use await or asyncio.run
        app.run_polling(allowed_updates=Update.ALL_TYPES)

    except KeyboardInterrupt:
        print("\n[STOP] Bot stopped by user (Ctrl+C)")
        logger.info("Bot stopped by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] FATAL ERROR: {str(e)}")
        logger.error(f"FATAL ERROR: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[STOP] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] FATAL ERROR in main: {str(e)}")
        logger.error(f"FATAL ERROR in main: {str(e)}", exc_info=True)
        sys.exit(1)
