"""通用工具函数"""

from datetime import datetime
from pathlib import Path

from db import search_history_case
from venues import recommend_venues
from config import llm


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


# ── 海报渲染 ──────────────────────────────────────────────
POSTER_DIR = Path("output") / "海报输出"


def generate_poster_image(prompt: str) -> str:
    """通过 token-plan 兼容端点调用 qwen-image-2.0 生成海报图片，返回本地文件路径。"""
    import requests

    api_key = llm.openai_api_key.get_secret_value()
    url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
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
    # 若前端设置了 SESSION_DIR，优先使用集中输出目录
    from main import SESSION_DIR
    out = SESSION_DIR if SESSION_DIR is not None else POSTER_DIR
    out.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"海报_{timestamp}.png"
    path = out / filename

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    path.write_bytes(resp.content)
    return str(path)