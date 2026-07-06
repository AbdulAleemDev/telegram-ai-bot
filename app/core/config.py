import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Telegram Bot API credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)


def validate_config() -> list[str]:
    """Return a list of configuration problems."""
    errors: list[str] = []

    if not GROQ_API_KEY:
        errors.append("GROQ_API_KEY is missing from .env")

    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is missing from .env")
    elif ":" not in TELEGRAM_BOT_TOKEN:
        errors.append(
            "TELEGRAM_BOT_TOKEN looks invalid. It should look like "
            "123456789:ABCdefGHI... (copy the full token from @BotFather)"
        )

    if not DATABASE_URL:
        errors.append("DATABASE_URL is missing from .env")

    return errors