from langchain_core.tools import tool
from datetime import datetime
import random


@tool
def ticket_tool(customer_issue: str) -> str:
    """
    Create a support ticket when the customer's issue
    requires assistance from a human agent.
    """

    ticket_id = f"TKT-{random.randint(1000,9999)}"

    created_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Later you can save this into a database.

    return (
        f"Your support ticket has been created successfully.\n\n"
        f"Ticket ID: {ticket_id}\n"
        f"Issue: {customer_issue}\n"
        f"Created At: {created_time}\n\n"
        f"Our support team will contact you shortly."
    )