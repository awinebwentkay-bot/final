"""财务节点：预算评估与迭代"""

from models import ActivityState
from config import llm
from tools import calc_budget
from prompts import FINANCE_EXTRACT


def finance_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    print(f"[财务] 正在提取参与人数...", flush=True)
    prompt = FINANCE_EXTRACT.format(plan=plan)
    people = int(llm.invoke(prompt).content)
    budget = calc_budget(base_cost=300, people=people)
    state["total_budget"] = budget
    if budget > 800 and state["budget_retry"] < 2:
        state["budget_feedback"] = "lack"
        state["budget_retry"] += 1
        state["log"].append(f"【财务】预算{budget}元，不足（第{state['budget_retry']}次），退回策划修改")
    else:
        state["budget_feedback"] = "enough"
        if budget > 800:
            state["log"].append(f"【财务】预算{budget}元，超限但已达最大重试次数，强制通过")
        else:
            state["log"].append(f"【财务】预算{budget}元，充足，进入执行环节")
    return state