import logging
import traceback

from app.core.telegram import send_telegram_message
from app.graph.agent import run_agent

logger = logging.getLogger("telegram-bot")


def handle_message(user_message: str, chat_id: int | str) -> str:
    """
    Process incoming Telegram messages using the LangGraph agent.
    """

    logger.info("=" * 70)
    logger.info("📩 NEW MESSAGE RECEIVED")
    logger.info("Chat ID      : %s", chat_id)
    logger.info("User Message : %s", user_message)

    try:
        logger.info("🤖 Running LangGraph Agent...")

        reply = run_agent(user_message)

        logger.info("✅ Agent Response:")
        logger.info("%s", reply)

        logger.info("📤 Sending response to Telegram...")

        telegram_response = send_telegram_message(chat_id, reply)

        logger.debug("Telegram API Response: %s", telegram_response)

        logger.info("✅ Message sent successfully.")
        logger.info("=" * 70)

        return reply

    except Exception:
        logger.error("❌ Error while processing message")
        logger.error(traceback.format_exc())
        raise