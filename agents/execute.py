"""执行节点：生成日程、主持稿、通知 + 任务拆解（Task Executor）"""

import json
import re

from models import ActivityState
from config import llm
from tools import get_venue_info
from prompts import (
    EXECUTE_SCHEDULE,
    EXECUTE_SCRIPT,
    EXECUTE_NOTICE,
    REGULATION_APPROVAL,
    TASK_EXECUTOR_PROMPT,
    TASK_ROLE_LIBRARY,
)


def _parse_json_from_response(text: str) -> dict:
    """从 LLM 响应中提取第一个 JSON 对象。"""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    raise ValueError("无法从 LLM 响应中解析 JSON")


def execute_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    people = state["input_participants"]
    venue = get_venue_info(people)
    regulations = REGULATION_APPROVAL
    print(f"[执行] 正在生成活动日程...", flush=True)
    sch = llm.invoke(EXECUTE_SCHEDULE.format(plan=plan, venue=venue, regulations=regulations)).content
    state["schedule"] = sch

    # ── 是否需要主持人 ──────────────────────────────────────
    need_host = input("\n  🎤 是否需要主持人？（y/n，默认 y）：").strip().lower()
    if need_host not in ("n", "no", "否"):
        need_host = True
        print(f"[执行] 正在生成主持稿...", flush=True)
        script = llm.invoke(EXECUTE_SCRIPT.format(plan=plan)).content
        state["host_script"] = script
        state["need_host"] = True

        # ── 是否需要PPT ─────────────────────────────────────
        need_ppt = input("\n  📊 是否需要生成 PPT 演示文稿？（y/n，默认 y）：").strip().lower()
        if need_ppt in ("n", "no", "否"):
            state["need_ppt"] = False
            print("[执行] 跳过 PPT 生成", flush=True)
        else:
            state["need_ppt"] = True
    else:
        state["need_host"] = False
        state["need_ppt"] = False
        state["host_script"] = None
        print("[执行] 跳过主持稿和 PPT 生成", flush=True)

    print(f"[执行] 正在生成通知文案...", flush=True)
    # 获取海报已确认信息，确保时间地点一致
    import json
    confirmed = state.get("poster_info_confirmed", "{}")
    try:
        p_info = json.loads(confirmed)
    except (json.JSONDecodeError, TypeError):
        p_info = {"date": "待定", "time": "待定", "venue": "待定"}
    p_date = p_info.get("date", "待定")
    p_time = p_info.get("time", "待定")
    p_venue = p_info.get("venue", "待定")
    notice = llm.invoke(EXECUTE_NOTICE.format(plan=plan, regulations=regulations,
                       p_date=p_date, p_time=p_time, p_venue=p_venue)).content
    state["notice_text"] = notice
    state["log"].append("【执行】日程、通知生成完成")

    # ── 策划案拆解与任务排期 ────────────────────────────────
    print(f"[执行] 正在解析策划案并拆解任务...", flush=True)
    prompt = TASK_EXECUTOR_PROMPT.format(role_library=TASK_ROLE_LIBRARY, plan=plan)
    resp = llm.invoke(prompt).content

    try:
        parsed = _parse_json_from_response(resp)
        state["task_execution_plan"] = json.dumps(parsed, ensure_ascii=False, indent=2)
        task_count = len(parsed.get("tasks", []))
        role_count = len(parsed.get("role_assignment", []))
        print(f"[执行] 拆解完成：{task_count} 个任务，{role_count} 个角色分配", flush=True)
        state["log"].append(f"【执行】策划案拆解为 {task_count} 个任务，涉及 {role_count} 个角色")
    except (ValueError, json.JSONDecodeError) as e:
        error_msg = f"任务拆解解析失败：{e}"
        print(f"[执行] {error_msg}", flush=True)
        state["task_execution_plan"] = json.dumps(
            {"error": error_msg, "raw_response": resp}, ensure_ascii=False
        )
        state["log"].append(f"【执行】{error_msg}")

    return state