"""LangGraph 流程编排"""

from langgraph.graph import StateGraph, END
from models import ActivityState
from agents import (
    command_center,
    plan_agent,
    finance_agent,
    execute_agent,
    promote_agent,
    risk_check_agent,
    feedback_agent,
)


def budget_route(state: ActivityState):
    if state["budget_feedback"] == "lack":
        return "plan_agent"
    return "execute_agent"


builder = StateGraph(ActivityState)
builder.add_node("command_center", command_center)
builder.add_node("plan_agent", plan_agent)
builder.add_node("finance_agent", finance_agent)
builder.add_node("execute_agent", execute_agent)
builder.add_node("promote_agent", promote_agent)
builder.add_node("risk_check_agent", risk_check_agent)
builder.add_node("feedback_agent", feedback_agent)

builder.set_entry_point("command_center")
builder.add_edge("command_center", "plan_agent")
builder.add_edge("plan_agent", "finance_agent")

builder.add_conditional_edges("finance_agent", budget_route, {
    "plan_agent": "plan_agent",
    "execute_agent": "execute_agent",
})

builder.add_edge("execute_agent", "promote_agent")
builder.add_edge("promote_agent", "risk_check_agent")
builder.add_edge("risk_check_agent", "feedback_agent")
builder.add_edge("feedback_agent", END)

graph = builder.compile()