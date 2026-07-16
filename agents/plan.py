"""策划节点：生成活动策划案"""

from models import ActivityState
from config import llm
from prompts import PLAN_MAIN, REGULATION_APPROVAL, REGULATION_FINANCE
from tools import get_venue_info


def plan_agent(state: ActivityState) -> ActivityState:
    cases = state["history_cases"]
    user_intent = state["user_intent"]
    regulations = REGULATION_APPROVAL + REGULATION_FINANCE
    budget_hint = ""
    budget_reimb = state["input_budget_reimbursable"]
    budget_non_reimb = state["input_budget_non_reimbursable"]
    budget_total = state["input_budget"]

    # 场地建议
    people = state["input_participants"]
    venue_hint = f"\n\n【参考场地】\n{get_venue_info(people)}\n"

    if state["budget_feedback"] == "lack":
        previous_estimate = state.get("total_budget", "未知")
        shortfall = previous_estimate - budget_total if isinstance(previous_estimate, int) else 0
        budget_hint = (
            f"\n注意：上次预算估算为{previous_estimate}元，超出预算。"
            f"用户可用经费：可报销{budget_reimb}元，不可报销（班费）{budget_non_reimb}元，合计{budget_total}元。"
            f"请务必缩减参与人数、简化活动流程，"
            f"将总费用控制在{budget_total}元以内，其中可报销部分不超过{budget_reimb}元。"
            f"经费使用须遵守实事求是、勤俭节约的原则，不得开支与学生活动无关的费用。"
        )
        print(f"[策划] 第{state['budget_retry']}次重试：预算估算{previous_estimate}元，需控制在{budget_total}元以内，正在缩减方案规模...", flush=True)
    elif state["budget_feedback"] == "surplus":
        previous_estimate = state.get("total_budget", 0)
        remaining = budget_total - previous_estimate
        budget_hint = (
            f"\n注意：上次预算估算为{previous_estimate}元，用户预算合计{budget_total}元"
            f"（可报销{budget_reimb}元，不可报销班费{budget_non_reimb}元），"
            f"尚有{remaining}元未使用。"
            f"请在合理范围内丰富活动内容（如增加优质奖品、宣传物料、场地布置等），"
            f"尽可能将{remaining}元预算用完，注意可报销部分不超过{budget_reimb}元。"
            f"须遵守实事求是、勤俭节约的原则，不得开支与学生活动无关的费用，不得购买零食/食品。"
        )
        print(f"[策划] 第{state['budget_retry']}次重试：预算估算{previous_estimate}元，低于预算{budget_total}元，正在丰富方案...", flush=True)

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
        budget_hint=budget_hint + reference_hint + venue_hint,
        regulations=regulations,
    )
    print(f"[策划] 正在调用大模型生成策划案...", flush=True)
    resp = llm.invoke(prompt)
    state["activity_plan"] = resp.content
    state["log"].append("【策划】生成活动策划案完成")
    print(f"[策划] 策划案生成完成", flush=True)
    return state