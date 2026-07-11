"""策划节点：生成活动策划案"""

from models import ActivityState
from config import llm
from prompts import PLAN_MAIN


def plan_agent(state: ActivityState) -> ActivityState:
    cases = state["history_cases"]
    user_intent = state["user_intent"]
    budget_hint = ""
    if state["budget_feedback"] == "lack":
        budget_limit = state["input_budget"]
        budget_hint = (
            f"\n注意：上次预算超支，请缩减参与人数、简化流程，"
            f"将总预算控制在{budget_limit}元以内。"
        )
        print(f"[策划] 第{state['budget_retry']}次重试：收到预算不足反馈，正在缩减方案规模...", flush=True)
    prompt = PLAN_MAIN.format(history_cases=cases, user_intent=user_intent, budget_hint=budget_hint)
    print(f"[策划] 正在调用大模型生成策划案...", flush=True)
    resp = llm.invoke(prompt)
    state["activity_plan"] = resp.content
    state["log"].append("【策划】生成活动策划案完成")
    print(f"[策划] 策划案生成完成", flush=True)
    return state