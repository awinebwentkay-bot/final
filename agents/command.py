"""中枢节点：接收用户需求，加载历史案例"""

from models import ActivityState
from tools import search_case_tool


def command_center(state: ActivityState) -> ActivityState:
    intent = state["user_intent"]
    print(f"[中枢] 接收用户需求：{intent}", flush=True)
    state["log"].append(f"【中枢】接收用户需求：{intent}")
    cases = search_case_tool()
    state["history_cases"] = cases
    state["short_memory"] = {"user_demand": intent}
    return state