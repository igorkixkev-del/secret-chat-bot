"""
Configuration module for Secret Chat Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///secret_chat.db")

# Encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Bot settings
COMMAND_PREFIX = "/"
MAX_MESSAGE_LENGTH = 4096
MESSAGE_RETENTION_DAYS = 30

# Security
SESSION_TIMEOUT = 3600  # 1 hour in seconds
MAX_LOGIN_ATTEMPTS = 5
RATE_LIMIT_MESSAGES = 30  # per minute

# Validation
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set!")
