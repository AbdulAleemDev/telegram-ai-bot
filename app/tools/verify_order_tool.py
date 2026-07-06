from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy import func

from app.core.database import SessionLocal
from app.database.models import CustomerOrder


@tool
def verify_order_tool(
    name: str,
    order_id: str,
    date_purchased: str,
    city: str,
) -> str:
    """
    Verify a customer's order details before creating a support ticket.

    Returns:
    VERIFIED
    or
    NOT VERIFIED
    """

    db = SessionLocal()

    try:
        try:
            purchase_date = datetime.strptime(
                date_purchased.strip(),
                "%Y-%m-%d"
            ).date()

        except ValueError:
            return "NOT VERIFIED"

        order = (
            db.query(CustomerOrder)
            .filter(
                func.lower(CustomerOrder.name) == name.lower().strip(),
                func.lower(CustomerOrder.order_id) == order_id.lower().strip(),
                func.lower(CustomerOrder.city) == city.lower().strip(),
                func.date(CustomerOrder.date) == purchase_date,
            )
            .first()
        )

        if order:
            return "VERIFIED"

        return "NOT VERIFIED"

    finally:
        db.close()