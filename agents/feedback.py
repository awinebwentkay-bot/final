"""反馈节点：生成评价内容和问卷模板"""

from models import ActivityState
from config import llm
from prompts import FEEDBACK_EVAL, FEEDBACK_SURVEY


def feedback_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    print(f"[反馈] 正在生成评价内容...", flush=True)
    eval_res = llm.invoke(FEEDBACK_EVAL.format(plan=plan)).content
    print(f"[反馈] 正在生成问卷模板...", flush=True)
    survey = llm.invoke(FEEDBACK_SURVEY).content
    state["eval_comment"] = eval_res
    state["survey_template"] = survey
    state["log"].append("【反馈】评价内容、问卷生成完成")
    return state