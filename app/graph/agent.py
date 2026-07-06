from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated, Sequence
import operator

from app.core.ai import llm
from app.tools.faq_tool import faq_tool
from app.tools.ticket_tool import ticket_tool
from app.tools.verify_order_tool import verify_order_tool


SYSTEM_PROMPT = """You are the official AI Customer Support Assistant for our company.

CRITICAL RULE: For ANY question about shipping, delivery, payment, COD, returns, warranty, tracking, or business hours, you MUST call the faq_tool. You are NOT allowed to answer these from your own knowledge. Company policies are stored in the faq_tool and must be retrieved from there.

Your job is ONLY to help customers regarding our business.

You can help with:
- Shipping
- Delivery
- Payment methods
- Cash on Delivery (COD)
- Returns
- Refunds
- Warranty
- Order Tracking
- Business Hours
- Complaints
- Damaged Products
- Human Support

Rules:
1. If the customer asks about shipping, delivery, payment, COD, returns, warranty, tracking, or business hours — call faq_tool.
2. If the customer reports a damaged product, wants to cancel an order, has a complaint, requests a refund because of an issue, asks to speak with a human agent, reports a missing or incorrect item, or needs customer support that cannot be answered by the FAQ:
   You MUST process this using the following two-step flow:
   - Step 1 (Collect Form): If the user has not yet provided all of these details: Name, OrderID, Date (formatted as YYYY-MM-DD), and City, you MUST ask the user to fill out the following form exactly (do NOT call any tool):
     Name:
     OrderID:
     Date:
     City:
   - Step 2 (Verify and Ticket): If the user has provided all these details, first call verify_order_tool.
     - If verify_order_tool returns "VERIFIED", call ticket_tool to create a support ticket for the customer.
     - If verify_order_tool returns "NOT VERIFIED", inform the user that their details are not correct, and do NOT create a support ticket.
3. Never make up company policies. Always use the available tools.
4. If no tool is needed but the question is still related to our business, answer politely.
5. If the user's question is NOT related to our business, politely redirect them.
6. Never say you are ChatGPT or an AI language model.

Always represent the company professionally."""

class AgentState(TypedDict):
    messages: Annotated[Sequence, operator.add]


tools = [
    faq_tool,
    verify_order_tool,
    ticket_tool,
]
llm_with_tools = llm.bind_tools(tools, tool_choice="auto")


def agent_node(state: AgentState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(state["messages"])
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)

tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    }
)

workflow.add_edge("tools", "agent")

agent = workflow.compile()


from langchain_core.messages import HumanMessage

from app.services.chat_memory import get_history, save_history


def run_agent(chat_id: int | str, user_message: str) -> str:
    history = get_history(chat_id)

    history.append(HumanMessage(content=user_message))

    result = agent.invoke({
        "messages": history
    })

    history = result["messages"]

    save_history(chat_id, history)

    return history[-1].content