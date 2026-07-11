"""通用工具函数"""

from db import search_history_case


def calc_budget(base_cost: int, people: int):
    return base_cost + people * 15


def get_venue_info(people: int):
    if people <= 50:
        return "小型活动室：容纳50人，配备话筒、投影，开放8:00-21:00"
    elif people <= 200:
        return "阶梯教室：容纳200人，多媒体全套设备"
    return "大礼堂：容纳500人"


def search_case_tool():
    return search_history_case()


def export_doc(content: str, filename: str):
    with open(f"./{filename}.txt", "w", encoding="utf-8") as f:
        f.write(content)
    return f"{filename}文档导出完成"