"""风险节点：合规检查与风险评估"""

from models import ActivityState
from config import llm
from prompts import RISK_CHECK


def risk_check_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    print(f"[风险] 正在生成风险评估报告...", flush=True)
    risk = llm.invoke(RISK_CHECK.format(plan=plan)).content
    state["risk_report"] = risk
    state["log"].append("【风险】活动合规初审完成")
    return state