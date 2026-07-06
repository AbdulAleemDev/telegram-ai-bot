from langchain_core.tools import tool


FAQ_DATA = {
    "business hours": (
        "We are open Monday to Saturday from 9:00 AM to 6:00 PM."
    ),

    "return policy": (
        "You can return products within 7 days of delivery "
        "if they are unused and in their original packaging."
    ),

    "deliver to lahore": (
        "Yes, we deliver to Lahore and other major cities across Pakistan."
    ),

    "shipping": (
        "Standard shipping costs PKR 250. "
        "Orders above PKR 5,000 qualify for free shipping."
    ),

    "delivery": (
        "Delivery usually takes 2–5 business days "
        "depending on your location."
    ),

    "payment": (
        "We accept Cash on Delivery (COD), bank transfer, "
        "and major debit/credit cards."
    ),

    "track": (
        "Once your order is shipped, we will send you "
        "a tracking number via Telegram or SMS."
    ),

    "cod": (
        "Yes, Cash on Delivery (COD) is available "
        "in most cities across Pakistan."
    ),

    "warranty": (
        "Selected products include a 12-month manufacturer's warranty."
    ),
}

FAQ_KEYWORDS = {
    "business hours": ["hour", "hours", "open", "close", "timing", "timings", "schedule", "time"],
    "return policy": ["return", "returns", "policy", "exchange", "replace", "replacement"],
    "deliver to lahore": ["lahore", "karachi", "islamabad", "faisalabad", "multan", "rawalpindi", "peshawar", "quetta", "location", "locations", "city", "cities", "destination", "destinations", "where do you deliver", "deliver to"],
    "shipping": ["shipping", "ship", "charge", "charges", "fee", "fees", "cost", "costs", "price", "prices", "free"],
    "delivery": ["delivery", "deliveries", "deliver", "day", "days", "time", "duration", "how long", "arrive", "when will", "receive"],
    "payment": ["payment", "payments", "pay", "card", "cards", "bank", "transfer", "credit", "debit", "easypaisa", "jazzcash"],
    "track": ["track", "tracking", "status", "where is my order", "order status"],
    "cod": ["cod", "cash on delivery", "cash"],
    "warranty": ["warranty", "warranties", "guarantee", "guarantees", "warranty period"],
}


@tool
def faq_tool(question: str) -> str:
    """
    Retrieve the official company policy and accurate business information.

    MANDATORY: You MUST call this tool for ANY question about:
    - Shipping charges, costs, or fees
    - Delivery timeframes or locations
    - Payment methods (COD, cards, bank transfer, EasyPaisa, JazzCash)
    - Cash on Delivery availability
    - Return or exchange policies
    - Warranty information
    - Order tracking procedures
    - Business hours or operating schedule
    - Delivery coverage areas (cities, locations)

    CRITICAL: Do NOT answer these questions from your own knowledge.
    Company policies may change, and this tool provides the ONLY accurate,
    up-to-date information. Making up policies is strictly prohibited.

    Do NOT use this tool for:
    - Complaints or damaged product reports
    - Order cancellation requests
    - Human support escalation
    """

    question = question.lower().strip()

    best_key = None
    max_score = 0

    for key, keywords in FAQ_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in question:
                score += len(kw)  # Weight by keyword length
        if score > max_score:
            max_score = score
            best_key = key

    if best_key and max_score > 0:
        return FAQ_DATA[best_key]

    return (
        "Sorry, I couldn't find information about that in our business knowledge base."
    )