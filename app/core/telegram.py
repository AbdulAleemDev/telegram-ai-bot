import logging
import requests
import traceback

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