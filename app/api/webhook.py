import json
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException, Request

from app.core.config import TELEGRAM_WEBHOOK_SECRET
from app.services.bot_service import handle_message

logger = logging.getLogger("telegram-bot")
router = APIRouter()
_executor = ThreadPoolExecutor(max_workers=4)


@router.get("/webhook")
async def webhook_health():
    """Health check for the Telegram webhook endpoint."""
    return {"status": "ok", "message": "Telegram webhook endpoint is ready"}


@router.post("/webhook")
async def receive_update(request: Request):
    if TELEGRAM_WEBHOOK_SECRET:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != TELEGRAM_WEBHOOK_SECRET:
            logger.warning("Rejected webhook request: invalid secret token")
            raise HTTPException(status_code=403, detail="Invalid webhook secret")

    body = await request.json()

    logger.info("=" * 60)
    logger.info("TELEGRAM UPDATE RECEIVED")
    logger.info("%s", json.dumps(body, indent=2))
    logger.info("=" * 60)

    message = body.get("message")
    if not message:
        logger.info("Update has no message (callback query, edit, etc.)")
        return {"status": "ok"}

    text = message.get("text")
    chat = message.get("chat", {})
    chat_id = chat.get("id")

    logger.info("Chat ID: %s | Text: %s", chat_id, text)

    if not chat_id or not text:
        logger.warning("Skipping update: missing chat_id or text")
        return {"status": "ok"}

    try:
        logger.info("Processing message...")
        loop = __import__("asyncio").get_running_loop()
        reply = await loop.run_in_executor(_executor, handle_message, text, chat_id)
        logger.info("Reply sent: %s", reply[:200] if len(reply) > 200 else reply)
    except Exception:
        logger.error("handle_message failed:\n%s", traceback.format_exc())

    return {"status": "ok"}
