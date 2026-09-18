import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Search Parameters
SEARCH_TOPIC = os.getenv("SEARCH_TOPIC", "Славяно-Арийская культура")
SEARCH_MIN_LIKES = int(os.getenv("SEARCH_MIN_LIKES", "100"))
SEARCH_MIN_COMMENTS = int(os.getenv("SEARCH_MIN_COMMENTS", "50"))
SEARCH_TOP_VIDEOS = int(os.getenv("SEARCH_TOP_VIDEOS", "5"))
SEARCH_FREQUENCY = os.getenv("SEARCH_FREQUENCY", "daily")

# Telegram Channel
TELEGRAM_CHANNEL_ID = "-1002123456789"  # Будет обновлен после получения токена

# Database
DATABASE_FILE = "scout_agent.db"

# Logging
LOG_DIR = "logs"
LOG_LEVEL = "INFO"

# Validation
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY не установлен в .env файле")
