"""通用工具函数"""

from db import search_history_case
from venues import recommend_venues


def calc_budget(base_cost: int, people: int):
    return base_cost + people * 15


def get_venue_info(people: int) -> str:
    """根据参与人数推荐场地，以《场地资源.pdf》为唯一参考。"""
    venues = recommend_venues(people)
    if not venues:
        return "暂无匹配的场地信息，请联系学校相关部门咨询。"

    lines = ["根据《场地资源.pdf》，推荐以下场地（按容量排序）："]
    for v in venues:
        cap = v["capacity"]
        note = f"（{v['note']}）" if v["note"] else ""
        lines.append(
            f"  - {v['name']}：容量 {cap}，{v['facilities']}，"
            f"位于{v['location']}，管理部门：{v['manager']}{note}"
        )
    lines.append("\n预约方式：请通过对应管理部门的指定渠道进行预约。")
    return "\n".join(lines)


def search_case_tool():
    return search_history_case()


def export_doc(content: str, filename: str):
    with open(f"./{filename}.txt", "w", encoding="utf-8") as f:
        f.write(content)
    return f"{filename}文档导出完成"