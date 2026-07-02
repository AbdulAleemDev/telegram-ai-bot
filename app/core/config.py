import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Telegram Bot API credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")


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

    return errors
