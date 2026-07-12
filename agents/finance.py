"""财务节点：预算评估与迭代"""

from models import ActivityState
from config import llm
from prompts import FINANCE_EXTRACT, FINANCE_ESTIMATE, REGULATION_FINANCE


def finance_agent(state: ActivityState) -> ActivityState:
    user_budget = state["input_budget"]
    plan = state["activity_plan"]

    # 首次使用用户输入的人数估算；重试时用 LLM 根据策划案内容精细化估算
    if state["budget_retry"] > 0:
        prompt = FINANCE_ESTIMATE.format(plan=plan, regulations=REGULATION_FINANCE)
        resp = llm.invoke(prompt)
        try:
            estimated_cost = int(resp.content.strip())
        except ValueError:
            # LLM 输出非数字时退回简单估算
            prompt = FINANCE_EXTRACT.format(plan=plan)
            people = int(llm.invoke(prompt).content)
            estimated_cost = people * 15
    else:
        people = state["input_participants"]
        estimated_cost = people * 15

    state["total_budget"] = estimated_cost

    print(f"[财务] 预算估算：{estimated_cost}元，用户预算：{user_budget}元", flush=True)

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