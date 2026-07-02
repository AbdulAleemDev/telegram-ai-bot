"""Register the Telegram webhook with Telegram's servers."""

import httpx
import os
import sys
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")
SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")


def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN is not set in .env")
        sys.exit(1)

    if not WEBHOOK_URL:
        print("Error: TELEGRAM_WEBHOOK_URL is not set in .env")
        print("Example: https://your-domain.com/webhook")
        sys.exit(1)

    params = {"url": WEBHOOK_URL}
    if SECRET:
        params["secret_token"] = SECRET

    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    response = httpx.get(url, params=params, timeout=30.0)
    print(response.json())

    if response.status_code != 200 or not response.json().get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
