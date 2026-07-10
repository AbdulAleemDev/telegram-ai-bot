from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.database.models import Order


STATUS_MESSAGES = {
    "pending": "⏳ Your order is pending confirmation. We'll update you once it's confirmed.",
    "confirmed": "✅ Your order has been confirmed and is being prepared for packing.",
    "packed": "📦 Your order has been packed and is ready for shipment.",
    "shipped": "🚚 Your order has been shipped! It's on its way to you.",
    "in_transit": "🛣️ Your order is in transit. It's moving through our delivery network.",
    "out_for_delivery": "📍 Your order is out for delivery today. Keep your phone handy!",
    "delivered": "✅ Your order has been delivered. Thank you for shopping with us!",
    "cancelled": "❌ Your order has been cancelled. Contact support if you need help.",
    "returned": "🔄 Your order has been returned. Our team will process the refund shortly.",
}


@tool
def track_order_tool(order_id: str) -> str:
    """
    Track the status and location of a customer's order.

    Use this tool when the customer:
    - Asks "where is my order"
    - Wants to track their order
    - Asks for order status or delivery status
    - Says "I haven't received my order"
    - Asks about shipping progress

    Do NOT use this tool for:
    - General questions about shipping policies or delivery timeframes (use faq_tool)
    - Complaints or refund requests (use ticket_tool after verification)
    """

    db = SessionLocal()

    try:
        order = db.query(Order).filter(
            Order.order_id == order_id.strip().upper()
        ).first()

        if not order:
            return (
                "❌ Order not found.\n\n"
                "Please double-check your Order ID and try again. "
                "Order IDs are case-insensitive. "
                "If you continue to have trouble, you can create a support ticket."
            )

        status_msg = STATUS_MESSAGES.get(
            order.status.lower(),
            f"📋 Order status: {order.status}"
        )

        lines = [
            f"📦 Order Tracking",
            f"",
            f"Order ID: {order.order_id}",
            f"Item: {order.item_name}",
            f"Customer: {order.customer_name}",
            f"City: {order.city}",
            f"",
            f"{status_msg}",
        ]

        if order.courier:
            lines.append(f"Courier: {order.courier}")

        if order.tracking_number:
            lines.append(f"Tracking #: {order.tracking_number}")

        if order.current_location:
            lines.append(f"Current Location: {order.current_location}")

        if order.estimated_delivery:
            est_date = order.estimated_delivery.strftime("%B %d, %Y")
            lines.append(f"Estimated Delivery: {est_date}")

        if order.notes:
            lines.append(f"")
            lines.append(f"📝 Note: {order.notes}")

        lines.append(f"")
        lines.append(f"Last Updated: {order.updated_at.strftime('%Y-%m-%d %H:%M')}")

        return "\n".join(lines)

    finally:
        db.close()