from datetime import datetime
import random

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.database.models import Ticket


@tool
def ticket_tool(order_id: str, customer_issue: str) -> str:
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

    db = SessionLocal()

    try:
        # Check if a ticket already exists for this order
        existing_ticket = db.query(Ticket).filter(
            Ticket.order_id == order_id.strip()
        ).first()

        if existing_ticket:
            return (
                f"⚠️ You already have a registered complaint for this order.\n\n"
                f"Ticket Number: {existing_ticket.ticket_number}\n"
                f"Issue: {existing_ticket.customer_issue}\n\n"
                f"Our support team will contact you soon. Please wait for their response."
            )

        # Generate new ticket
        ticket_number = f"TKT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

        new_ticket = Ticket(
            order_id=order_id.strip(),
            customer_issue=customer_issue.strip(),
            ticket_number=ticket_number,
        )

        db.add(new_ticket)
        db.commit()

        return f"""
✅ Your support ticket has been created successfully.

Ticket Number: {ticket_number}

Issue:
{customer_issue}

Our support team will review your request and contact you as soon as possible.

Please keep your ticket number for future reference.
""".strip()

    finally:
        db.close()