import logging
from contextlib import asynccontextmanager
from app.core.telegram import register_webhook
from fastapi import FastAPI, Request

from app.api.webhook import router
from app.core.config import validate_config
from app.core.logging_config import setup_logging

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    errors = validate_config()
    if errors:
        logger.error("=" * 60)
        logger.error("CONFIGURATION ERRORS")
        for error in errors:
            logger.error("  - %s", error)
        logger.error("=" * 60)
        logger.error("Fix .env and restart the server.")
    else:
        logger.info("Configuration OK")

        # ✅ AUTO REGISTER TELEGRAM WEBHOOK ON STARTUP
        await register_webhook()
        logger.info("Webhook registered successfully")

        logger.info("Webhook mode: run uvicorn, expose HTTPS, then set webhook")
        logger.info("Local dev: use  python scripts/run_polling.py  instead")

    logger.info("Server started - waiting for requests...")

    yield
app = FastAPI(title="Telegram AI Bot", lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def health_check():
    return {"status": "running", "message": "Telegram AI Bot is alive"}


@app.middleware("http")
async def log_all_requests(request: Request, call_next):
    logger.info(">>> %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("<<< %s %s -> %s", request.method, request.url.path, response.status_code)
    return response
