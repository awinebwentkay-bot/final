"""财务节点：预算评估与迭代"""

from models import ActivityState
from config import llm
from prompts import FINANCE_EXTRACT


def finance_agent(state: ActivityState) -> ActivityState:
    user_budget = state["input_budget"]
    plan = state["activity_plan"]

    # 首次使用用户输入的人数；重试时从新策划案提取（可能已缩减）
    if state["budget_retry"] > 0:
        prompt = FINANCE_EXTRACT.format(plan=plan)
        people = int(llm.invoke(prompt).content)
    else:
        people = state["input_participants"]

    print(f"[财务] 参与人数：{people}人，预算：{user_budget}元", flush=True)

    # 按人均消耗估算（无固定成本）
    estimated_cost = people * 15
    state["total_budget"] = estimated_cost

    if estimated_cost > user_budget and state["budget_retry"] < 2:
        state["budget_feedback"] = "lack"
        state["budget_retry"] += 1
        state["log"].append(
            f"【财务】估算成本{estimated_cost}元，超出预算{user_budget}元"
            f"（第{state['budget_retry']}次），退回策划修改"
        )
        print(f"[财务] 估算{estimated_cost}元超出预算{user_budget}元，退回策划调整", flush=True)
    else:
        state["budget_feedback"] = "enough"
        if estimated_cost > user_budget:
            state["log"].append(
                f"【财务】估算成本{estimated_cost}元超出预算{user_budget}元，"
                "已达最大重试次数，强制通过"
            )
        else:
            state["log"].append(
                f"【财务】估算成本{estimated_cost}元，预算{user_budget}元充足"
            )
    return state