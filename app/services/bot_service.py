import logging
import traceback

from app.core.telegram import send_telegram_message
from app.graph.agent import run_agent

logger = logging.getLogger("telegram-bot")


def handle_message(user_message: str, chat_id: int | str) -> str:
    logger.info("=" * 60)
    logger.info("BOT SERVICE STARTED")
    logger.info("User message: %s", user_message)

    try:
        logger.info("Running LangGraph agent...")
        reply = run_agent(user_message)
        logger.info("Agent reply: %s", reply)

        logger.info("Sending reply to Telegram...")
        telegram_response = send_telegram_message(chat_id, reply)
        logger.info("Telegram response: %s", telegram_response)

        logger.info("BOT SERVICE COMPLETED")
        logger.info("=" * 60)

        return reply

    except Exception:
        logger.error(traceback.format_exc())
        raise