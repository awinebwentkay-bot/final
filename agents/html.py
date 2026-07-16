"""HTML 生成节点：生成微信公众号风格的活动总结推文"""

import base64
import json
import re
from datetime import datetime
from pathlib import Path

from models import ActivityState
from config import llm

HTML_DIR = Path("output") / "公众号推文"

REVIEW_PROMPT = """
你是一位校园公众号小编。请根据以下活动策划案，写一篇**活动回顾推文**。

要求：
- 这是一篇活动**结束后**的回顾总结，不是活动预告
- 纯活动内容回顾，**不要提**申请流程、审批规定、规章等前置内容
- 语气轻松活泼，面向校园读者
- 重点描述活动流程、亮点、现场氛围、参与者感受
- 按活动的实际先后顺序描述各个环节
- 3-5 个自然段，每段 2-4 句话
- 结尾加一句对参与者的感谢

策划案内容：
{plan}
"""

INTRO_PROMPT = """
你是一位校园活动小编。请根据以下策划案，写一段**活动简介**（2-3句话）。

要求：
- 简洁介绍本次活动是什么、有什么亮点
- 语气轻松活泼，适合公众号推文
- 不要出现"根据"、"作为"、"为您"等套话
- 直接描述活动本身

策划案内容：
{plan}
"""


def _css() -> str:
    return """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#F5F5F5;font-family:-apple-system,'Microsoft YaHei','PingFang SC',sans-serif;padding:20px 0}
.article{max-width:640px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06)}
.header{padding:30px 24px 20px;text-align:center}
.header h1{font-size:22px;font-weight:700;color:#1a1a1a;line-height:1.5;margin-bottom:12px}
.header .meta{font-size:13px;color:#999}
.section{padding:10px 24px 20px}
.section h2{font-size:17px;font-weight:700;color:#1a1a1a;margin-bottom:12px;padding-left:12px;border-left:3px solid #1A56DB}
.section p{font-size:15px;color:#333;line-height:1.8;margin-bottom:10px;text-align:justify}
.section .highlight{background:#F0F4FF;padding:16px;border-radius:8px;margin:12px 0}
.section .highlight p{font-size:14px;color:#555;margin-bottom:4px}
.timeline{padding:0 24px 20px}
.timeline-item{display:flex;margin-bottom:16px;align-items:flex-start}
.timeline-time{min-width:80px;font-size:14px;font-weight:600;color:#1A56DB;padding-top:2px}
.timeline-dot{width:10px;height:10px;border-radius:50%;background:#1A56DB;margin:6px 16px 0 0;flex-shrink:0}
.timeline-content{font-size:14px;color:#333;line-height:1.6}
.poster-box{padding:0 24px 20px;text-align:center}
.poster-box img{max-width:100%;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,0.1)}
.poster-box .caption{font-size:12px;color:#999;margin-top:8px}
.footer{padding:24px;text-align:center;background:#FAFAFA;border-top:1px solid #EEE}
.footer p{font-size:13px;color:#999;line-height:1.8}
.footer .org{font-size:14px;font-weight:600;color:#333;margin-bottom:4px}
.divider{height:1px;background:linear-gradient(90deg,transparent,#E0E0E0,transparent);margin:0 24px}
"""


def _image_to_base64(path: str) -> str:
    """将图片文件转为 base64 data URI。"""
    try:
        p = Path(path)
        if not p.exists():
            # 尝试从相对路径解析
            p = Path.cwd() / path
        if not p.exists():
            return ""
        data = p.read_bytes()
        ext = p.suffix.lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                 "svg": "image/svg+xml", "webp": "image/webp"}.get(ext.lstrip("."), "image/png")
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    except Exception:
        return ""


def _llm_generate(prompt: str, fallback: str = "") -> str:
    """调用 LLM 生成内容，失败时返回 fallback。"""
    try:
        resp = llm.invoke(prompt).content
        text = resp.strip()
        # 去掉可能的思考标记
        text = re.sub(r'^.*?思考', '', text, flags=re.DOTALL).strip()
        return text
    except Exception:
        return fallback


def _build_html(state: dict) -> str:
    plan = state.get("activity_plan") or ""
    poster_path = state.get("poster_image") or ""

    # 获取确认信息
    confirmed = state.get("poster_info_confirmed") or "{}"
    try:
        info = json.loads(confirmed)
    except (json.JSONDecodeError, TypeError):
        info = {}

    title = info.get("title", "校园活动")
    subtitle = info.get("subtitle", "")
    organizer = info.get("organizer", "")
    date_str = info.get("date", "")
    time_str = info.get("time", "")
    venue = info.get("venue", "")
    audience = info.get("target_audience", "")

    # ── LLM 生成活动简介 ──
    print(f"  [HTML] 正在生成活动简介...", flush=True)
    summary = _llm_generate(INTRO_PROMPT.format(plan=plan), "一场精彩的活动，等你来回顾。")

    # ── LLM 生成回顾正文 ──
    print(f"  [HTML] 正在生成活动回顾正文...", flush=True)
    review_text = _llm_generate(REVIEW_PROMPT.format(plan=plan), "活动圆满结束，感谢所有参与者！")
    review_paragraphs = [p.strip() for p in review_text.split("\n") if p.strip()]

    # ── 从策划案中提取活动流程 ──
    flow_lines = []
    in_flow = False
    for line in plan.split("\n"):
        s = line.strip()
        if re.search(r"活动流程|活动环节|活动安排|流程", s) and ("##" in s or "#" in s):
            in_flow = True
            continue
        if in_flow:
            if s.startswith("##") and "流程" not in s and "环节" not in s and "安排" not in s:
                break
            if s and not s.startswith("#"):
                # 去掉编号前缀和人数标记
                s = re.sub(r"^\d+[.、）)\)]\s*", "", s)
                s = re.sub(r"（\d+分钟）", "", s)
                s = re.sub(r"（需\d+人）", "", s)
                s = re.sub(r"\(需\d+人\)", "", s)
                if s:
                    flow_lines.append(s.strip())

    flow_html = ""
    if flow_lines:
        items = "".join(f'<li>{line}</li>' for line in flow_lines)
        flow_html = f'<div class="section"><h2>📋 活动流程</h2><ol style="padding-left:20px;font-size:15px;color:#333;line-height:2">{items}</ol></div>'

    # ── 海报图片（base64 嵌入，避免 file:// 跨域拦截） ──
    poster_img_tag = ""
    if poster_path:
        b64 = _image_to_base64(poster_path)
        if b64:
            poster_img_tag = f'<div class="poster-box"><img src="{b64}" alt="活动海报" loading="lazy"><p class="caption">📌 活动海报</p></div>'
        else:
            # 兜底：用相对路径
            poster_img_tag = f'<div class="poster-box"><img src="../{poster_path}" alt="活动海报" loading="lazy"><p class="caption">📌 活动海报</p></div>'

    # ── 组装 HTML ──
    meta_parts = []
    if date_str:
        meta_parts.append(date_str)
    if organizer:
        meta_parts.append(organizer)
    meta_str = " ｜ ".join(meta_parts)

    # 回顾正文
    body_html = ""
    if review_paragraphs:
        body_html = '<div class="section"><h2>📝 活动回顾</h2>'
        for p in review_paragraphs:
            body_html += f"<p>{p}</p>"
        body_html += "</div>"

    # 活动信息高亮
    info_lines = []
    if date_str and time_str:
        info_lines.append(f"📅 时间：{date_str} {time_str}")
    if venue:
        info_lines.append(f"📍 地点：{venue}")
    if audience:
        info_lines.append(f"👥 对象：{audience}")
    if organizer:
        info_lines.append(f"🏢 主办：{organizer}")

    info_html = ""
    if info_lines:
        info_html = '<div class="section"><div class="highlight">'
        for line in info_lines:
            info_html += f"<p>{line}</p>"
        info_html += "</div></div>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>{title} - 活动回顾</title>
<style>{_css()}</style>
</head>
<body>
<div class="article">
    <div class="header">
        <h1>{title}</h1>
        {f'<p style="font-size:15px;color:#666;margin-bottom:10px">{subtitle}</p>' if subtitle else ''}
        <div class="meta">{meta_str}</div>
    </div>

    {info_html}

    {f'<div class="section"><h2>📖 活动简介</h2><p>{summary}</p></div>' if summary else ''}

    {body_html}

    {flow_html}

    {poster_img_tag}

    <div class="divider"></div>

    <div class="footer">
        <p class="org">{organizer or '校园活动组委会'}</p>
        <p>感谢所有参与者的支持与付出</p>
        <p style="margin-top:6px;font-size:12px;color:#bbb">本文由校园活动策划助手自动生成 · {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
</div>
</body>
</html>"""

    return html


def html_agent(state: ActivityState) -> ActivityState:
    """生成微信公众号风格的 HTML 活动总结推文。"""
    from main import SESSION_DIR
    out = SESSION_DIR if SESSION_DIR is not None else HTML_DIR
    out.mkdir(parents=True, exist_ok=True)
    print(f"[HTML] 正在生成公众号推文...", flush=True)

    html = _build_html(state)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"活动回顾_{ts}.html"
    path = out / filename
    path.write_text(html, encoding="utf-8")

    state["html_path"] = str(path)
    state["log"].append(f"【HTML】公众号推文已生成：{path}")
    print(f"[HTML] 公众号推文已生成：{path}", flush=True)

    return state