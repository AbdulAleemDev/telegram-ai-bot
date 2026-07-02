from langchain_core.tools import tool


FAQ_DATA = {
    "business hours": "We are open Monday to Saturday from 9:00 AM to 6:00 PM.",

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
        "Yes, selected products include a 12-month "
        "manufacturer's warranty."
    ),
}


@tool
def faq_tool(question: str) -> str:
    """
    Answer customer questions related to business policies,
    shipping, payment, delivery, warranty, and FAQs.
    """

    question = question.lower()

    for keyword, answer in FAQ_DATA.items():
        if keyword in question:
            return answer

    return (
        "Sorry, I couldn't find information related to that question "
        "in our knowledge base."
    )