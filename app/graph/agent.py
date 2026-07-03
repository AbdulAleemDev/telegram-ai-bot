from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated, Sequence
import operator

from app.core.ai import llm
from app.tools.faq_tool import faq_tool
from app.tools.ticket_tool import ticket_tool


SYSTEM_PROMPT = """You are the official AI Customer Support Assistant for our company.

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
2. If the customer has a complaint, damaged product, refund issue, cancellation request, or requests a human — call ticket_tool.
3. Never make up company policies. Always use the available tools.
4. If no tool is needed but the question is still related to our business, answer politely.
5. If the user's question is NOT related to our business, politely redirect them.
6. Never say you are ChatGPT or an AI language model.

Always represent the company professionally."""


class AgentState(TypedDict):
    messages: Annotated[Sequence, operator.add]


tools = [faq_tool, ticket_tool]
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


def run_agent(user_message: str) -> str:
    result = agent.invoke({
        "messages": [HumanMessage(content=user_message)]
    })
    return result["messages"][-1].content