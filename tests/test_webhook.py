import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_webhook_health(self):
        response = self.client.get("/webhook")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    @patch("app.api.webhook.handle_message")
    def test_receive_text_message(self, mock_handle_message):
        mock_handle_message.return_value = "Hello!"

        response = self.client.post(
            "/webhook",
            json={
                "update_id": 1,
                "message": {
                    "message_id": 1,
                    "chat": {"id": 12345, "type": "private"},
                    "text": "What are your business hours?",
                },
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        mock_handle_message.assert_called_once_with(
            "What are your business hours?", 12345
        )


if __name__ == "__main__":
    unittest.main()
