import asyncio
import json
from starlette.requests import Request
from app.api.webhook import receive_update


async def main():
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/webhook",
        "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
        "client": ("127.0.0.1", 1234),
        "server": ("testserver", 80),
        "http_version": "1.1",
    }
    body = json.dumps(
        {
            "update_id": 123456789,
            "message": {
                "message_id": 1,
                "from": {
                    "id": 987654321,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "testuser",
                },
                "chat": {"id": 987654321, "first_name": "Test", "type": "private"},
                "date": 1712345678,
                "text": "hello",
            },
        }
    ).encode("utf-8")

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    request = Request(scope, receive)
    response = await receive_update(request)
    print(response)


asyncio.run(main())
