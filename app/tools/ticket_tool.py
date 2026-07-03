from datetime import datetime
import random

from langchain_core.tools import tool


@tool
def ticket_tool(customer_issue: str) -> str:
    """
    Create a customer support ticket.

    Use this tool whenever the customer:

    - reports a damaged product
    - wants to cancel an order
    - has a complaint
    - requests a refund because of an issue
    - asks to speak with a human agent
    - reports a missing or incorrect item
    - needs customer support that cannot be answered by the FAQ

    Do NOT use this tool for general business questions such as
    shipping, payment, warranty, delivery, tracking, or business hours.
    """

    ticket_number = f"TKT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"

    return f"""
✅ Your support ticket has been created successfully.

Ticket Number: {ticket_number}

Issue:
{customer_issue}

Our support team will review your request and contact you as soon as possible.

Please keep your ticket number for future reference.
""".strip()