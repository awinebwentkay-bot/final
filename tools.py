"""通用工具函数"""

import os
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

# 从 config 中复用 API key
DASHSCOPE_API_KEY = "sk-sp-D.LYDLY.6EOn.MEQCIHpNRoRQHs1/WP/nB55d/hoyxo18dW5WwGMxVNOkl2ZFAiA9T+mOdVbKCWWG+MR0R0nHLdfBgwIHRRcpUEK6QDbaTQ=="


def generate_poster_image(prompt: str) -> str:
    """通过 token-plan 兼容端点调用 qwen-image-2.0 生成海报图片，返回本地文件路径。"""
    import requests

    url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "qwen-image-2.0",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": prompt},
                ],
            }
        ],
    }
    resp = requests.post(url, headers=headers, json=body, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    image_url = data["output"]["choices"][0]["message"]["content"][0]["image"]
    return _download_image(image_url)


def _download_image(url: str) -> str:
    """下载图片到本地海报目录，返回文件路径。"""
    import requests

    POSTER_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = url.split(".")[-1].split("?")[0] or "png"
    filename = f"海报_{timestamp}.{ext}"
    path = POSTER_DIR / filename

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    path.write_bytes(resp.content)
    return str(path)