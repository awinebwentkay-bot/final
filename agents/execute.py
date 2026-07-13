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
    print(f"[执行] 正在生成主持稿...", flush=True)
    script = llm.invoke(EXECUTE_SCRIPT.format(plan=plan)).content
    print(f"[执行] 正在生成通知文案...", flush=True)
    notice = llm.invoke(EXECUTE_NOTICE.format(plan=plan, regulations=regulations)).content
    state["schedule"] = sch
    state["host_script"] = script
    state["notice_text"] = notice
    state["log"].append("【执行】日程、主持稿、通知生成完成")

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