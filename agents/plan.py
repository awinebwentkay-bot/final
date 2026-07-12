"""策划节点：生成活动策划案"""

from models import ActivityState
from config import llm
from prompts import PLAN_MAIN, REGULATION_APPROVAL, REGULATION_FINANCE


def plan_agent(state: ActivityState) -> ActivityState:
    cases = state["history_cases"]
    user_intent = state["user_intent"]
    regulations = REGULATION_APPROVAL + REGULATION_FINANCE
    budget_hint = ""
    if state["budget_feedback"] == "lack":
        budget_limit = state["input_budget"]
        previous_estimate = state.get("total_budget", "未知")
        shortfall = previous_estimate - budget_limit if isinstance(previous_estimate, int) else 0
        budget_hint = (
            f"\n注意：上次预算估算为{previous_estimate}元，超出预算{shortfall}元。"
            f"请务必缩减参与人数、简化活动流程，"
            f"将总预算控制在{budget_limit}元以内。"
            f"经费使用须遵守实事求是、勤俭节约的原则，不得开支与学生活动无关的费用。"
        )
        print(f"[策划] 第{state['budget_retry']}次重试：预算估算{previous_estimate}元，需控制在{budget_limit}元以内，正在缩减方案规模...", flush=True)

    # 如果有互联网搜索到的参考案例，追加到提示中
    reference_hint = ""
    ref_cases = state.get("reference_cases")
    if ref_cases:
        reference_hint = (
            f"\n\n【以下是从互联网搜索到的优秀策划案例参考，可借鉴其创意和思路】\n"
            f"{ref_cases}\n"
            f"【参考案例结束】\n"
        )

    prompt = PLAN_MAIN.format(
        history_cases=cases,
        user_intent=user_intent,
        budget_hint=budget_hint + reference_hint,
        regulations=regulations,
    )
    print(f"[策划] 正在调用大模型生成策划案...", flush=True)
    resp = llm.invoke(prompt)
    state["activity_plan"] = resp.content
    state["log"].append("【策划】生成活动策划案完成")
    print(f"[策划] 策划案生成完成", flush=True)
    return state