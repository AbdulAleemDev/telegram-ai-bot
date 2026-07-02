"""
Run the bot locally using long polling (no ngrok/webhook needed).

Usage:
    python scripts/run_polling.py

Messages you send on Telegram will appear in this terminal immediately.
"""

import logging
import sys
import time
from pathlib import Path

import httpx

# Allow running as: python scripts/run_polling.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import TELEGRAM_BOT_TOKEN, validate_config
from app.core.logging_config import setup_logging
from app.services.bot_service import handle_message

logger = setup_logging()


def delete_webhook() -> None:
    """Polling and webhooks cannot run at the same time."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    response = httpx.get(url, params={"drop_pending_updates": True}, timeout=30.0)
    data = response.json()
    if data.get("ok"):
        logger.info("Webhook removed (polling mode enabled)")
    else:
        logger.warning("Could not remove webhook: %s", data)


def poll_updates() -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    offset = 0

    logger.info("Polling for Telegram messages... (Ctrl+C to stop)")

    while True:
        try:
            response = httpx.get(
                url,
                params={"offset": offset, "timeout": 30},
                timeout=35.0,
            )
            data = response.json()

            if not data.get("ok"):
                logger.error("getUpdates failed: %s", data)
                time.sleep(5)
                continue

            for update in data.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message")

                if not message:
                    logger.info("Skipped non-message update: %s", update.get("update_id"))
                    continue

                text = message.get("text")
                chat_id = message.get("chat", {}).get("id")

                if not text or not chat_id:
                    logger.warning("Skipped update with no text or chat_id")
                    continue

                logger.info("-" * 40)
                logger.info("New message from chat_id=%s: %s", chat_id, text)

                try:
                    reply = handle_message(text, chat_id)
                    logger.info("SUCCESS - replied: %s", reply[:200])
                except Exception:
                    logger.exception("FAILED to handle message")

        except httpx.HTTPError as exc:
            logger.error("Network error while polling: %s", exc)
            time.sleep(5)


def main() -> None:
    errors = validate_config()
    if errors:
        logger.error("Fix these issues in .env before running:")
        for error in errors:
            logger.error("  - %s", error)
        sys.exit(1)

    delete_webhook()
    poll_updates()


if __name__ == "__main__":
    main()
