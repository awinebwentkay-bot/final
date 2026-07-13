"""通用工具函数"""

import os
import re
from datetime import datetime
from pathlib import Path

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


# ── 海报渲染 ──────────────────────────────────────────────
POSTER_DIR = Path("海报输出")


def _svgtag(tag: str, attrs: dict = None, content: str = "") -> str:
    """生成单个 SVG 标签字符串。"""
    attr_str = ""
    if attrs:
        attr_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<{tag}{attr_str}>{content}</{tag}>"


def _clean_svg(llm_output: str) -> str:
    """从 LLM 输出中提取纯净 SVG 代码。"""
    text = llm_output.strip()
    # 去掉 ```svg ... ``` 或 ``` ... ``` 包裹
    text = re.sub(r"^```(?:svg)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    # 确保以 <svg 开头
    if not text.startswith("<svg"):
        start = text.find("<svg")
        if start != -1:
            text = text[start:]
    # 确保以 </svg> 结尾
    end = text.rfind("</svg>")
    if end != -1:
        text = text[: end + 6]
    return text.strip()


def save_poster_svg(svg_code: str, template_name: str) -> str:
    """保存 SVG 海报到文件，返回文件路径。"""
    POSTER_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"海报_{template_name}_{timestamp}.svg"
    path = POSTER_DIR / filename
    path.write_text(svg_code, encoding="utf-8")
    return str(path)