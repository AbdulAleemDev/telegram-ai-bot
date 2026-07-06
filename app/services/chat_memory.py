from collections import defaultdict

from langchain_core.messages import BaseMessage

# Stores conversation history for each Telegram chat
chat_histories: dict[int | str, list[BaseMessage]] = defaultdict(list)


def get_history(chat_id: int | str) -> list[BaseMessage]:
    return chat_histories[chat_id]


def save_history(chat_id: int | str, messages: list[BaseMessage]) -> None:
    chat_histories[chat_id] = messages


def clear_history(chat_id: int | str) -> None:
    chat_histories.pop(chat_id, None)