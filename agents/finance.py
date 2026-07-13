"""财务节点：预算评估与迭代"""

import re

from models import ActivityState
from config import llm
from prompts import FINANCE_EXTRACT, FINANCE_ESTIMATE, REGULATION_FINANCE


def _parse_two_budgets(text: str) -> tuple[int, int] | None:
    """从 LLM 输出中解析 可报销 和 不可报销 两个金额。"""
    reimbursable = None
    non_reimbursable = None
    for line in text.strip().split("\n"):
        line = line.strip()
        m = re.match(r"可报销[：:]\s*(\d+)", line)
        if m:
            reimbursable = int(m.group(1))
            continue
        m = re.match(r"不可报销[：:]\s*(\d+)", line)
        if m:
            non_reimbursable = int(m.group(1))
    if reimbursable is not None and non_reimbursable is not None:
        return reimbursable, non_reimbursable
    return None


def finance_agent(state: ActivityState) -> ActivityState:
    user_budget_reimb = state["input_budget_reimbursable"]
    user_budget_non_reimb = state["input_budget_non_reimbursable"]
    user_budget_total = state["input_budget"]
    plan = state["activity_plan"]

    # 根据策划案内容估算可报销和不可报销费用
    prompt = FINANCE_ESTIMATE.format(plan=plan, regulations=REGULATION_FINANCE)
    resp = llm.invoke(prompt).content

    parsed = _parse_two_budgets(resp)
    if parsed is not None:
        estimated_reimb, estimated_non_reimb = parsed
        estimated_total = estimated_reimb + estimated_non_reimb
    else:
        # LLM 输出格式异常时退回人数估算
        prompt = FINANCE_EXTRACT.format(plan=plan)
        people = int(llm.invoke(prompt).content)
        # 按 60% / 40% 拆分
        estimated_total = people * 15
        estimated_reimb = int(estimated_total * 0.6)
        estimated_non_reimb = estimated_total - estimated_reimb

    state["total_budget"] = estimated_total
    state["log"].append(
        f"【财务】估算：可报销{estimated_reimb}元，不可报销{estimated_non_reimb}元，合计{estimated_total}元"
    )

    print(
        f"[财务] 预算估算：可报销{estimated_reimb}元 + 不可报销{estimated_non_reimb}元 = {estimated_total}元，"
        f"用户预算：可报销{user_budget_reimb}元 + 不可报销{user_budget_non_reimb}元 = {user_budget_total}元",
        flush=True,
    )

    # 判断是否超预算（可报销或不可报销任一超出即触发）
    over_reimb = estimated_reimb > user_budget_reimb and user_budget_reimb > 0
    over_non_reimb = estimated_non_reimb > user_budget_non_reimb and user_budget_non_reimb > 0
    over_total = estimated_total > user_budget_total and user_budget_total > 0

    if user_budget_total == 0:
        # 用户未指定任何预算，直接通过
        state["budget_feedback"] = "enough"
        state["log"].append(f"【财务】估算合计{estimated_total}元，用户未指定预算")
    elif (over_reimb or over_non_reimb or over_total) and state["budget_retry"] < 3:
        state["budget_feedback"] = "lack"
        state["budget_retry"] += 1
        detail_parts = []
        if over_reimb:
            detail_parts.append(f"可报销超{estimated_reimb - user_budget_reimb}元")
        if over_non_reimb:
            detail_parts.append(f"不可报销超{estimated_non_reimb - user_budget_non_reimb}元")
        if over_total:
            detail_parts.append(f"合计超{estimated_total - user_budget_total}元")
        detail = "，".join(detail_parts)
        state["log"].append(
            f"【财务】估算{estimated_total}元，超出预算（{detail}），"
            f"第{state['budget_retry']}次，退回缩减"
        )
        print(f"[财务] 超出预算（{detail}），退回策划缩减", flush=True)
    elif estimated_total < user_budget_total and state["budget_retry"] < 3:
        # 预算有盈余，退回策划丰富方案
        state["budget_feedback"] = "surplus"
        state["budget_retry"] += 1
        shortfall = user_budget_total - estimated_total
        state["log"].append(
            f"【财务】估算{estimated_total}元，低于预算{user_budget_total}元"
            f"（剩余{shortfall}元，第{state['budget_retry']}次），退回丰富"
        )
        print(f"[财务] 估算{estimated_total}元低于预算{user_budget_total}元，退回策划丰富", flush=True)
    else:
        state["budget_feedback"] = "enough"
        if over_reimb or over_non_reimb or over_total:
            state["log"].append(
                f"【财务】估算{estimated_total}元超出预算，已达最大重试次数，强制通过"
            )
        else:
            diff = user_budget_total - estimated_total
            state["log"].append(
                f"【财务】估算{estimated_total}元，预算{user_budget_total}元"
                f"（剩余{diff}元），预算通过"
            )
    return state