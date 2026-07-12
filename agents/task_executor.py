"""任务执行 Agent（Task Executor）：策划案拆解 → 子任务 → 责任人分配 → 甘特图排期"""

import json
import re

from models import ActivityState
from config import llm
from prompts import TASK_EXECUTOR_PROMPT, TASK_ROLE_LIBRARY


def _parse_json_from_response(text: str) -> dict:
    """从 LLM 响应中提取第一个 JSON 对象。"""
    # 尝试解析整个响应
    text = text.strip()
    # 去掉可能的 ```json ... ``` 包裹
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # 尝试从大括号开始截取
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    raise ValueError("无法从 LLM 响应中解析 JSON")


def task_executor(state: ActivityState) -> ActivityState:
    """解析策划案 → 拆解任务 → 分配角色 → 输出结构化 JSON 甘特图数据。"""
    plan = state.get("activity_plan", "")
    if not plan:
        state["task_execution_plan"] = json.dumps(
            {"error": "策划案为空，无法执行任务拆解"}, ensure_ascii=False
        )
        state["log"].append("【任务执行】策划案为空，跳过拆解")
        return state

    print(f"[任务执行] 正在解析策划案并拆解任务...", flush=True)
    prompt = TASK_EXECUTOR_PROMPT.format(role_library=TASK_ROLE_LIBRARY, plan=plan)
    resp = llm.invoke(prompt).content

    try:
        parsed = _parse_json_from_response(resp)
        state["task_execution_plan"] = json.dumps(parsed, ensure_ascii=False, indent=2)
        task_count = len(parsed.get("tasks", []))
        role_count = len(parsed.get("role_assignment", []))
        print(
            f"[任务执行] 拆解完成：{task_count} 个任务，{role_count} 个角色分配",
            flush=True,
        )
        state["log"].append(
            f"【任务执行】策划案拆解为 {task_count} 个任务，涉及 {role_count} 个角色"
        )
    except (ValueError, json.JSONDecodeError) as e:
        error_msg = f"解析失败：{e}"
        print(f"[任务执行] {error_msg}", flush=True)
        state["task_execution_plan"] = json.dumps(
            {"error": error_msg, "raw_response": resp}, ensure_ascii=False
        )
        state["log"].append(f"【任务执行】{error_msg}")

    return state