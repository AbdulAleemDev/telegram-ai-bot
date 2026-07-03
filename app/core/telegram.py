import logging
import requests
import traceback
import os
import httpx

from app.core.config import TELEGRAM_BOT_TOKEN

logger = logging.getLogger("telegram-bot")


def send_telegram_message(chat_id: int | str, message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    logger.info("POST %s", url)
    logger.info("Payload: %s", payload)

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30,
        )

        logger.info("Status Code: %s", response.status_code)
        logger.info("Response Text: %s", response.text)

        response.raise_for_status()

        return response.json()

    except Exception:
        logger.error(traceback.format_exc())
        raise


async def register_webhook():
    """
    Registers Telegram webhook on startup (runs from Railway server).
    """
    webhook_url = os.getenv("TELEGRAM_WEBHOOK_URL")

    if not TELEGRAM_BOT_TOKEN or not webhook_url:
        logger.warning(
            "Webhook registration skipped: missing TELEGRAM_BOT_TOKEN or TELEGRAM_WEBHOOK_URL"
        )
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data={"url": webhook_url},
                timeout=30,
            )

        logger.info("Webhook registration response: %s", response.text)

    except Exception:
        logger.error("Webhook registration failed:\n%s", traceback.format_exc())