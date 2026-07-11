"""执行节点：生成日程、主持稿、通知"""

from models import ActivityState
from config import llm
from tools import get_venue_info
from prompts import EXECUTE_SCHEDULE, EXECUTE_SCRIPT, EXECUTE_NOTICE


def execute_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    people = state["input_participants"]
    venue = get_venue_info(people)
    print(f"[执行] 正在生成活动日程...", flush=True)
    sch = llm.invoke(EXECUTE_SCHEDULE.format(plan=plan)).content
    print(f"[执行] 正在生成主持稿...", flush=True)
    script = llm.invoke(EXECUTE_SCRIPT.format(plan=plan)).content
    print(f"[执行] 正在生成通知文案...", flush=True)
    notice = llm.invoke(EXECUTE_NOTICE.format(plan=plan)).content
    state["schedule"] = sch
    state["host_script"] = script
    state["notice_text"] = notice
    state["log"].append("【执行】日程、主持稿、通知生成完成")
    return state