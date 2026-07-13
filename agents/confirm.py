"""确认节点：展示策划案关键信息，让用户确认/修改/留待定，输出精确信息供海报和PPT使用"""

import json

from models import ActivityState
from config import llm
from prompts import POSTER_EXTRACT_INFO


def confirm_agent(state: ActivityState) -> ActivityState:
    """从策划案提取关键信息 → 展示给用户 → 确认/修改 → 存入 state。"""
    plan = state.get("activity_plan", "")

    # LLM 提取信息
    prompt = POSTER_EXTRACT_INFO.format(plan=plan)
    resp = llm.invoke(prompt).content.strip()
    if resp.startswith("```"):
        resp = resp.strip("`").strip()
        if resp.startswith("json"):
            resp = resp[4:].strip()
    try:
        info = json.loads(resp)
    except json.JSONDecodeError:
        info = {
            "title": "校园活动",
            "subtitle": "",
            "date": "待定",
            "time": "待定",
            "venue": "待定",
            "organizer": "待定",
            "description": "",
            "target_audience": "全校师生",
        }

    print(f"\n{'=' * 50}")
    print(f"  📋 请确认活动信息（用于海报和PPT生成）")
    print(f"{'=' * 50}")
    print(f"  直接 Enter 保持当前值，或输入新内容修改")
    print()

    # 逐字段确认
    fields = [
        ("title",          "活动标题"),
        ("subtitle",       "副标题/标语"),
        ("date",           "活动日期"),
        ("time",           "活动时间"),
        ("venue",          "活动地点"),
        ("organizer",      "主办单位"),
        ("description",    "一句话亮点"),
        ("target_audience","面向人群"),
    ]

    for key, label in fields:
        current = info.get(key, "待定")
        if not current:
            current = "待定"
        user_input = input(f"  {label} [{current}]：").strip()
        if user_input:
            info[key] = user_input
        else:
            info[key] = current  # 保持原值或"待定"

    # 确认汇总
    print(f"\n  📌 最终信息确认：")
    for key, label in fields:
        print(f"     {label}：{info.get(key, '待定')}")

    state["poster_info_confirmed"] = json.dumps(info, ensure_ascii=False)
    state["log"].append(
        f"【确认】活动信息已确认：{info.get('title')} | {info.get('date')} {info.get('time')} | {info.get('venue')}"
    )
    print(f"  ✅ 信息已确认，继续执行\n")

    return state