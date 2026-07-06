from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy import func

from app.core.database import SessionLocal
from app.database.models import CustomerOrder


@tool
def verify_order_tool(
    name: str,
    order_id: str,
    item: str,
    date_purchased: str,
) -> str:
    """
    Verify a customer's order before creating a support ticket.

    Returns:
    VERIFIED
    or
    NOT VERIFIED
    """

    db = SessionLocal()

    try:
        try:
            purchase_date = datetime.strptime(
                date_purchased,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            return "NOT VERIFIED"

        order = (
            db.query(CustomerOrder)
            .filter(
                CustomerOrder.name == name,
                CustomerOrder.order_id == order_id,
                CustomerOrder.purchased_item == item,
                func.date(CustomerOrder.date) == purchase_date,
            )
            .first()
        )

        if order:
            return "VERIFIED"

        return "NOT VERIFIED"

    finally:
        db.close()