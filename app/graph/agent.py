from app.core.ai import llm
from app.tools.faq_tool import faq_tool
from app.tools.ticket_tool import ticket_tool


FAQ_KEYWORDS = [
    "return",
    "refund",
    "shipping",
    "delivery",
    "payment",
    "warranty",
    "track",
    "cod",
    "business hours",
    "lahore",
]


def run_agent(user_message: str) -> str:
    message = user_message.lower()

    # FAQ
    if any(keyword in message for keyword in FAQ_KEYWORDS):
        answer = faq_tool.invoke({"question": user_message})

        if "couldn't find" not in answer.lower():
            return answer

    # Human support
    if any(
        word in message
        for word in [
            "complaint",
            "broken",
            "damaged",
            "agent",
            "human",
            "support",
            "cancel",
        ]
    ):
        return ticket_tool.invoke({"customer_issue": user_message})

    # Otherwise use LLM
    response = llm.invoke(user_message)
    return response.content